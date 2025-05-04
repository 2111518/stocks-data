import yfinance as yf
import numpy as np
from numba import njit

# 模擬用除數（實際 S&P 的除數由 S&P 公司維護，這裡只是舉例）
SIMULATED_DIVISOR = 10_000_000_000

# 讀取股票代碼
with open('out.txt', 'r') as f:
    tickers = [line.strip() for line in f if line.strip()]

# 取得市值資料（用 yfinance 批次抓取）
data = yf.Tickers(' '.join(tickers))

market_caps = []
valid_tickers = []

for ticker in tickers:
    try:
        cap = data.tickers[ticker].info.get("marketCap", 0)
        if cap and cap > 0:
            market_caps.append(cap)
            valid_tickers.append(ticker)
    except Exception as e:
        print(f"無法取得 {ticker} 的資料：{e}")

# 用 numba 加速市值加總
@njit(cache=True)
def compute_index(market_caps_array, divisor):
    total_market_cap = 0.0
    for cap in market_caps_array:
        total_market_cap += cap
    return total_market_cap / divisor

# 計算模擬的 S&P 500 指數
market_caps_np = np.array(market_caps, dtype=np.float64)
sp500_index = compute_index(market_caps_np, SIMULATED_DIVISOR)

# print(f"已成功取得 {len(valid_tickers)} 支股票的市值")
print(f"模擬 S&P 500 指數為：{sp500_index:.2f}")

