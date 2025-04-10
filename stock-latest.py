import yfinance as yf
import pandas as pd
import os

def get_tickers_and_names_from_file(filename):
    """從檔案讀取股票代碼及對應公司名稱（以第一個空格分隔）"""
    if not os.path.exists(filename):
        print(f"❌ 檔案 '{filename}' 找不到，請確認檔案是否存在。")
        return []

    tickers_info = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(" ", 1)
                ticker = parts[0].upper()
                name = parts[1].strip() if len(parts) > 1 else ticker
                tickers_info.append((ticker, name))
    return tickers_info

# 讀取 out.txt 檔案
filename = "./data/out.txt"
tickers_info = get_tickers_and_names_from_file(filename)

if not tickers_info:
    print("❌ 沒有讀取到任何股票代碼，程式結束。")
    exit()

tickers = [item[0] for item in tickers_info]
ticker_name_dict = dict(tickers_info)

# 使用 yfinance 批次抓取歷史價格（不使用 info）
stocks = yf.Tickers(" ".join(tickers))
stock_data = []

for ticker in tickers:
    try:
        stock = stocks.tickers[ticker]
        hist = stock.history(period="1d")

        if not hist.empty:
            price = hist["Close"].iloc[-1]
            date = hist.index[-1].strftime("%Y-%m-%d")
            name = ticker_name_dict.get(ticker, ticker)
            stock_data.append([ticker, name, price, date])
        else:
            print(f"⚠️ 無法獲取 {ticker} 的歷史數據。")
    except Exception as e:
        print(f"❌ 取得 {ticker} 的數據時發生錯誤: {e}")

# 輸出 CSV
df = pd.DataFrame(stock_data, columns=["Ticker", "Company Name", "Price", "Date"])
df.to_csv("stock-close-latest.csv", index=False)

print("📄 資料已儲存到 stock-close-latest.csv")

