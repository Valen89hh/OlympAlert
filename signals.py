# signals.py
from blinker import signal

# Señal para notificar que se han recibido candles del broker.
candles_received = signal('candles_received')

