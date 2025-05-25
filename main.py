# main.py
import asyncio
import numpy as np
from broker_client import BrokerClient
import sys
import signal
import pandas as pd
from config import TOKEN
from signals import candles_received
from filters_candles import filtrar_candles_completas
from indicators import calculata_bollinger
from telgrama_utils import send_telegram_message

ACTIVOS = ["LATAM_X", "CRYPTO_X", "EUROPE_X"]

async def manejar_broker(pair, duration):
    async def handle_candles_received(candles, volume):
        print(f"[{pair}] Entrando a handle_candles_received")
        if candles and volume:
            volume_dict = {v["t"]: v["value"] for v in volume}
            combined_data = [
                [candle["t"], candle["open"], candle["high"], candle["low"], candle["close"], volume_dict.get(candle["t"], 0)]
                for candle in candles
            ]
            ohlc_history = combined_data[:100]
            data_np = np.array(list(reversed(filtrar_candles_completas(ohlc_history))))
            ohlcv_df = pd.DataFrame(data_np, columns=["timestamp", "open", "high", "low", "close", "volume"])
            bb = calculata_bollinger(ohlcv_df)

            close = ohlcv_df.iloc[-1]["close"]
            upper = bb.iloc[-1]["upper"]
            lower = bb.iloc[-1]["lower"]
            print(f"[{pair}] Close -> {close} Upper -> {upper} Lower -> {lower}")

            if close > upper:
                msg = f"📈 [{pair}] ¡Rompió la banda superior de Bollinger!\nClose: {close:.2f} > Upper: {upper:.2f}"
                print(msg)
                await send_telegram_message(msg)

            elif close < lower:
                msg = f"📉 [{pair}] ¡Rompió la banda inferior de Bollinger!\nClose: {close:.2f} < Lower: {lower:.2f}"
                print(msg)
                await send_telegram_message(msg)

    broker = BrokerClient(TOKEN, pair, duration, handle_candles_received)

    try:
        task_connection = asyncio.create_task(broker.manage_connection())
        task_periodic = asyncio.create_task(broker.periodic_get_candles(pair, duration))
        await asyncio.gather(task_connection, task_periodic)
    finally:
        await broker.close()




async def main():
    tareas = [manejar_broker(pair, 60) for pair in ACTIVOS]
    await asyncio.gather(*tareas)

if __name__ == "__main__":
     # Manejo de señales (opcional) para asegurar la salida controlada
    def signal_handler(sig, frame):
        print("Señal recibida, finalizando...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    asyncio.run(main())
