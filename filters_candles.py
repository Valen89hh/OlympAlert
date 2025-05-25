from datetime import datetime

def filtrar_candles_completas(candles):
    # Obtener el inicio del minuto actual
    ahora = datetime.now()
    inicio_minuto_actual = datetime(ahora.year, ahora.month, ahora.day, ahora.hour, ahora.minute)
    timestamp_minuto_actual = int(inicio_minuto_actual.timestamp())
    
    # Filtrar las candles que sean anteriores al inicio del minuto actual
    candles_filtradas = [candle for candle in candles if candle[0] < timestamp_minuto_actual]
    return candles_filtradas