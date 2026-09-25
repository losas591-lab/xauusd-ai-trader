from __future__ import annotations

import MetaTrader5 as mt5

from config.settings import MAGIC_NUMBER, LOT_SIZE, STOP_LOSS_POINTS, TAKE_PROFIT_POINTS


def place_trade(symbol: str, direction: str, price: float):
    if direction == "BUY":
        trade_type = mt5.ORDER_TYPE_BUY
    elif direction == "SELL":
        trade_type = mt5.ORDER_TYPE_SELL
    else:
        raise ValueError(f"Unsupported direction: {direction}")

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise RuntimeError(f"Symbol info not found: {symbol}")

    stop_loss = price - STOP_LOSS_POINTS * symbol_info.point if direction == "BUY" else price + STOP_LOSS_POINTS * symbol_info.point
    take_profit = price + TAKE_PROFIT_POINTS * symbol_info.point if direction == "BUY" else price - TAKE_PROFIT_POINTS * symbol_info.point

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": LOT_SIZE,
        "type": trade_type,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": MAGIC_NUMBER,
        "comment": "AurumBot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Trade failed:", result)
        return None

    print(f"{direction} order placed at {price} for {symbol}")
    return result
