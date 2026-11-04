import pytest
from omniverse.modules.intelligence.indicators import (
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_atr
)

def test_calculate_rsi():
    # 14 price points with upwards trend
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 112, 115, 114, 118, 120]
    rsi = calculate_rsi(prices, period=14)
    assert 0.0 <= rsi <= 100.0
    assert rsi > 50.0 # Bullish upward trend should have RSI > 50

def test_calculate_macd():
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 115, 118, 120, 122, 125, 128, 130, 132, 135]
    macd_res = calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9)
    assert "macd_line" in macd_res
    assert "signal_line" in macd_res
    assert "histogram" in macd_res

def test_calculate_bollinger_bands():
    prices = [100, 102, 101, 103, 102, 104, 105, 103, 106, 107, 108, 107, 109, 110, 112, 111, 113, 115, 114, 116]
    bb = calculate_bollinger_bands(prices, period=20, num_std=2.0)
    assert "upper_band" in bb
    assert "middle_band" in bb
    assert "lower_band" in bb
    assert bb["upper_band"] >= bb["middle_band"] >= bb["lower_band"]

def test_calculate_atr():
    highs = [105, 108, 107, 110, 112, 115, 118]
    lows = [100, 102, 101, 104, 106, 109, 112]
    closes = [102, 104, 105, 109, 111, 114, 116]
    atr = calculate_atr(highs, lows, closes, period=5)
    assert atr > 0.0
