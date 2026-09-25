from __future__ import annotations

import pandas as pd
import MetaTrader5 as mt5

from config.settings import ACCOUNT_LOGIN, ACCOUNT_PASSWORD, ACCOUNT_SERVER


def resolve_timeframe(timeframe_name: str):
    mapping = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    return mapping.get(timeframe_name.upper(), mt5.TIMEFRAME_M15)


def connect_to_mt5() -> bool:
    if not mt5.initialize(login=ACCOUNT_LOGIN, password=ACCOUNT_PASSWORD, server=ACCOUNT_SERVER):
        print("MT5 initialize failed:", mt5.last_error())
        return False
    print(f"Connected to MT5 account {ACCOUNT_LOGIN}")
    return True


def shutdown_mt5() -> None:
    mt5.shutdown()
    print("MT5 connection closed.")


def ensure_symbol(symbol: str):
    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"Failed to select symbol: {symbol}")

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise RuntimeError(f"Symbol info not found: {symbol}")
    return symbol_info


def get_latest_tick(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"No tick data for symbol: {symbol}")
    return tick


def get_recent_bars(symbol: str, timeframe_name: str, count: int = 200):
    timeframe = resolve_timeframe(timeframe_name)
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"No candles available for {symbol} on {timeframe_name}")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df[["time", "open", "high", "low", "close", "tick_volume"]]
    return df.rename(columns={"tick_volume": "volume"})
