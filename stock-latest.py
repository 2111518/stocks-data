import yfinance as yf
import pandas as pd

def get_tickers_from_file(filename):
    """從檔案讀取股票代碼"""
    try:
        with open(filename, "r") as f:
            tickers = [line.strip().upper() for line in f if line.strip()]
        return tickers
    except FileNotFoundError:
        print(f"❌ 檔案 '{filename}' 找不到，請確認檔案是否存在。")
        return []

# 讀取 out.txt 檔案內的股票代碼
filename = "./data/out.txt"
tickers = get_tickers_from_file(filename)

if not tickers:
    print("❌ 沒有讀取到任何股票代碼，程式結束。")
    exit()

# 取得股票的公司名稱
tickers_names = {}
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if "longName" in info:
            tickers_names[ticker] = info["longName"]
        else:
            tickers_names[ticker] = ticker  # 若無法獲取公司名稱，則使用代碼
        time.sleep(0.001)  # 讓間隔為 1 毫秒
    except Exception as e:
        print(f"⚠️ 無法獲取 {ticker} 的公司名稱，使用默認名稱。")

# 創建一個空的 DataFrame 來儲存股票數據
stock_data = pd.DataFrame(columns=["Ticker", "Company Name", "Price"])

# 迴圈遍歷股票代碼列表
for ticker, name in tickers_names.items():
    try:
        # 使用 yfinance 獲取股票數據
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")  # 獲取最近一天的數據 (可以根據需要調整時間範圍)

        # 獲取收盤價
        price = hist['Close'].iloc[-1]  # 獲取最後一個收盤價

        # TODO:加上收盤價的時間
 
        # 將股票數據添加到 DataFrame
        stock_data.loc[len(stock_data)] = [ticker, name, price]

    except Exception as e:
        print(f"無法取得 {name} ({ticker}) 的數據: {e}")

# 如果需要，可以將數據儲存到 CSV 檔案 
stock_data.to_csv("stock-close-latest.csv", index=False)  # 不儲存索引
print("資料已儲存到 stock-close-latest.csv")
