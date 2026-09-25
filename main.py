import time

from bot.execution import place_trade
from bot.mt5_connector import connect_to_mt5, get_latest_tick, get_recent_bars, shutdown_mt5, ensure_symbol
from bot.strategy import generate_signal
from config.settings import SYMBOL, TIMEFRAME


def main():
    if not connect_to_mt5():
        return

    try:
        ensure_symbol(SYMBOL)
        tick = get_latest_tick(SYMBOL)
        bars = get_recent_bars(SYMBOL, TIMEFRAME, count=200)

        signal = generate_signal(bars)
        print(f"Current signal: {signal}")
        print(f"Current price: {tick.ask}")

        if signal == "BUY":
            place_trade(SYMBOL, "BUY", tick.ask)
        elif signal == "SELL":
            place_trade(SYMBOL, "SELL", tick.bid)
        else:
            print("No trade signal right now.")

        while True:
            time.sleep(5)

    finally:
        shutdown_mt5()


if __name__ == "__main__":
    main()
