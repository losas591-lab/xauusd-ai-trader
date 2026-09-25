import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_LOGIN = int(os.getenv("MT5_LOGIN", "12345678"))
ACCOUNT_PASSWORD = os.getenv("MT5_PASSWORD", "your_password")
ACCOUNT_SERVER = os.getenv("MT5_SERVER", "Exness-MT5")

SYMBOL = os.getenv("SYMBOL", "XAUUSD")
TIMEFRAME = os.getenv("TIMEFRAME", "M15")

FAST_EMA = int(os.getenv("FAST_EMA", "20"))
SLOW_EMA = int(os.getenv("SLOW_EMA", "50"))
RSI_PERIOD = int(os.getenv("RSI_PERIOD", "14"))

LOT_SIZE = float(os.getenv("LOT_SIZE", "0.01"))
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "1.0"))
STOP_LOSS_POINTS = int(os.getenv("STOP_LOSS_POINTS", "100"))
TAKE_PROFIT_POINTS = int(os.getenv("TAKE_PROFIT_POINTS", "200"))
MAGIC_NUMBER = int(os.getenv("MAGIC_NUMBER", "123456"))
