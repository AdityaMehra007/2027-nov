from typing import List, Dict, Any
import math

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculates Relative Strength Index (RSI)."""
    if len(prices) < period + 1:
        return 50.0

    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(rsi, 2)

def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Calculates Exponential Moving Average (EMA)."""
    if not prices:
        return []
    k = 2.0 / (period + 1.0)
    ema = [prices[0]]
    for p in prices[1:]:
        ema.append(p * k + ema[-1] * (1.0 - k))
    return ema

def calculate_macd(
    prices: List[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
) -> Dict[str, float]:
    """Calculates MACD Line, Signal Line, and MACD Histogram."""
    if len(prices) < slow_period:
        return {"macd_line": 0.0, "signal_line": 0.0, "histogram": 0.0}

    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)
    macd_series = [f - s for f, s in zip(fast_ema, slow_ema)]
    signal_series = calculate_ema(macd_series, signal_period)

    current_macd = macd_series[-1]
    current_signal = signal_series[-1]
    histogram = current_macd - current_signal

    return {
        "macd_line": round(current_macd, 2),
        "signal_line": round(current_signal, 2),
        "histogram": round(histogram, 2)
    }

def calculate_bollinger_bands(
    prices: List[float],
    period: int = 20,
    num_std: float = 2.0
) -> Dict[str, float]:
    """Calculates Bollinger Upper, Middle (SMA), and Lower Bands."""
    if len(prices) < period:
        period = len(prices)

    sub = prices[-period:]
    sma = sum(sub) / period
    variance = sum((p - sma) ** 2 for p in sub) / period
    std_dev = math.sqrt(variance)

    upper = sma + (num_std * std_dev)
    lower = sma - (num_std * std_dev)

    return {
        "upper_band": round(upper, 2),
        "middle_band": round(sma, 2),
        "lower_band": round(lower, 2),
        "bandwidth_pct": round(((upper - lower) / sma) * 100.0, 2) if sma > 0 else 0.0
    }

def calculate_atr(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14
) -> float:
    """Calculates Average True Range (ATR) for volatility and stop-loss sizing."""
    if len(closes) < 2:
        return 0.0

    tr_list = []
    for i in range(1, len(closes)):
        h = highs[i]
        l = lows[i]
        prev_c = closes[i - 1]
        tr = max(h - l, abs(h - prev_c), abs(l - prev_c))
        tr_list.append(tr)

    effective_period = min(period, len(tr_list))
    atr = sum(tr_list[-effective_period:]) / effective_period
    return round(atr, 2)
