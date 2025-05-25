import ta
import pandas as pd
import ta.volatility

def calculata_bollinger(ohlcv):
    bb_indicator = ta.volatility.BollingerBands(close=ohlcv["close"], window=20, window_dev=2)
    result = pd.DataFrame({
        "medium": bb_indicator.bollinger_mavg(),  # Banda media
        "upper": bb_indicator.bollinger_hband(), # Banda superior
        "lower": bb_indicator.bollinger_lband(), # Banda inferior
    })

    return result