from __future__ import annotations

import numpy as np
import pandas as pd

from config.settings import FAST_EMA, RSI_PERIOD, SLOW_EMA


def calculate_rsi(series: pd.Series, period: int = RSI_PERIOD) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)

    roll_up = up.ewm(com=period - 1, adjust=False).mean()
    roll_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = roll_up / roll_down.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def prepare_market_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    prepared = df.copy()
    prepared["ema_fast"] = prepared["close"].ewm(span=FAST_EMA, adjust=False).mean()
    prepared["ema_slow"] = prepared["close"].ewm(span=SLOW_EMA, adjust=False).mean()
    prepared["rsi"] = calculate_rsi(prepared["close"], RSI_PERIOD)
    return prepared


def generate_signal(df: pd.DataFrame) -> str:
    if df.empty or len(df) < 2:
        return "HOLD"

    prepared = prepare_market_data(df)
    latest = prepared.iloc[-1]

    ema_fast = float(latest["ema_fast"])
    ema_slow = float(latest["ema_slow"])
    rsi_value = float(latest["rsi"])

    if ema_fast > ema_slow and rsi_value > 50:
        return "BUY"
    if ema_fast < ema_slow and rsi_value < 50:
        return "SELL"
    return "HOLD"
