import asyncio
import json
import time
import websockets
from signals import candles_received
from request_factory import RequestFactory
import traceback

class BrokerClient: 
    def __init__(self, token, pair, duration, on_candles):
        self.token = token
        self.ws = None
        self.candles_temp = None
        self.volume_temp = None
        self.on_candles = on_candles
        self.url_ws = (
            "wss://ws.olymptrade.com/otp?cid_ver=1&cid_app=web%40OlympTrade%402025.1.25798"
            "%4025798&cid_device=%40%40desktop&cid_os=windows%4010"
        )
        self.pair = pair
        self.duration = duration

    async def close(self):
        if self.ws:
            await self.ws.close()
            print("BrokerClient: Conexión cerrada.")

    async def manage_connection(self):
        """Se encarga de gestionar la conexión y reconexión."""
        headers = RequestFactory.request_headers_websocket(self.token)
        while True:
            try:
                self.ws = await websockets.connect(
                    self.url_ws,
                    origin="https://olymptrade.com",  # Simula el header Origin del navegador
                    additional_headers=headers,
                    user_agent_header="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
                )
                print("BrokerClient: Conectado al WebSocket de Olymp Trade")
                # Al conectarse, podemos enviar candles de inmediato
                await self.get_candles(self.pair, self.duration)
                # Inicia la tarea de escucha; cuando se cierre, se lanzará una excepción
                await self.listen_messages()
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"BrokerClient: Conexión cerrada: {e}. Reintentando en 5 segundos...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"BrokerClient: Error inesperado: {e}. Reintentando en 5 segundos...")
                await asyncio.sleep(5)

    async def listen_messages(self):
        """Escucha de forma indefinida los mensajes del WebSocket."""
        try:
            while True:
                message = await self.ws.recv()
                self.process_message(message)
        except websockets.exceptions.ConnectionClosedError as e:
            print("BrokerClient: WebSocket se cerró en listen_messages.")
            # Propagar la excepción para que manage_connection intente reconectar.
            raise e

    async def get_candles(self, pair, duration):
        print("LLamando get_candles()")
        request_messages = RequestFactory.request_candles(pair, duration)
        if self.ws:
            try:
                for request in request_messages:
                    data = json.dumps(request)
                    await self.ws.send(data)
            except Exception as e:
                print("BrokerClient: Error al enviar get_candles:", e)
        else:
            print("BrokerClient: ws_olymptrade aún no está conectado.")

    def process_message(self, message):
        try:
            data = json.loads(message)
            if len(data) > 0 and 'd' in data[0] and isinstance(data[0]['d'], list):
                for item in data[0]['d']:
                    
                    if isinstance(item, dict) and 'candles' in item:
                        candles = item['candles']
                        print(f"BrokerClient: Se recibieron candles: {time.time()}")
                        self.candles_temp = candles
                    
                    if isinstance(item, dict) and 'volume' in item:
                        volume = item['volume']
                        print(f"BrokerClient: Se recibieron volume: {time.time()}")
                        self.volume_temp = volume
            if self.candles_temp and self.volume_temp:
                print("----- ENVIANDO DATOS ----")
                #candles_received.send(self, candles=self.candles_temp, volume=self.volume_temp, pair=self.pair)
                if self.on_candles:
                    asyncio.create_task(self.on_candles(self.candles_temp, self.volume_temp))
                self.candles_temp = None
                self.volume_temp = None

        except Exception as e:
            traceback.print_exc()
            print(f"BrokerClient: Error en el WebSocket: {e}")

    async def periodic_get_candles(self, pair, duration):
        """Tarea que llama a get_candles() cada minuto exacto."""
        while True:
            now = time.time()
            next_minute = (int(now / 60) + 1) * duration
            await asyncio.sleep(next_minute - now)
            if self.ws:
                await self.get_candles(pair, duration)
                print("Periodic: get_candles() llamado a las", time.strftime("%H:%M:%S"))
            else:
                print("Periodic: No hay conexión activa para get_candles().")
