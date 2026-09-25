from __future__ import annotations


def calculate_position_size(balance: float, risk_per_trade_pct: float, stop_loss_points: int, point_value: float = 1.0) -> float:
    if balance <= 0 or stop_loss_points <= 0:
        return 0.01

    risk_amount = balance * (risk_per_trade_pct / 100.0)
    calculated_lot = risk_amount / (stop_loss_points * point_value)
    return max(0.01, calculated_lot)


def get_order_levels(current_price: float, direction: str, stop_loss_points: int, take_profit_points: int, point_value: float):
    if direction == "BUY":
        stop_loss = current_price - stop_loss_points * point_value
        take_profit = current_price + take_profit_points * point_value
    elif direction == "SELL":
        stop_loss = current_price + stop_loss_points * point_value
        take_profit = current_price - take_profit_points * point_value
    else:
        raise ValueError(f"Unsupported direction: {direction}")

    return stop_loss, take_profit
