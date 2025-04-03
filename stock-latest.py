import yfinance as yf
import pandas as pd
import os

def get_tickers_from_file(filename):
    """從檔案讀取股票代碼"""
    if not os.path.exists(filename):
        print(f"❌ 檔案 '{filename}' 找不到，請確認檔案是否存在。")
        return []
    
    with open(filename, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]

# 讀取 out.txt 檔案內的股票代碼
filename = "./data/out.txt"
tickers = get_tickers_from_file(filename)

if not tickers:
    print("❌ 沒有讀取到任何股票代碼，程式結束。")
    exit()

# 使用 yfinance 一次性獲取多個股票數據
stocks = yf.Tickers(" ".join(tickers))

# 創建 DataFrame 來儲存數據
stock_data = []

for ticker in tickers:
    try:
        stock = stocks.tickers[ticker]
        info = stock.info
        name = info.get("longName", ticker)  # 預設使用代碼
        hist = stock.history(period="1d")  # 獲取最近一天的數據

        if not hist.empty:
            price = hist["Close"].iloc[-1]  # 取得最近收盤價
            date = hist.index[-1].strftime("%Y-%m-%d")  # 取得日期
            stock_data.append([ticker, name, price, date])
        else:
            print(f"⚠️ 無法獲取 {ticker} ({name}) 的歷史數據。")

    except Exception as e:
        print(f"❌ 取得 {ticker} 的數據時發生錯誤: {e}")

# 建立 DataFrame 並儲存
df = pd.DataFrame(stock_data, columns=["Ticker", "Company Name", "Price", "Date"])
df.to_csv("stock-close-latest.csv", index=False)

print("📄 資料已儲存到 stock-close-latest.csv")

