import yfinance as yf
import pandas as pd
import datetime
import os

def get_valid_date(prompt):
    """取得有效的日期，允許使用 'today' 作為當前日期"""
    while True:
        date_str = input(prompt).strip()
        if date_str.lower() == "today":
            return datetime.datetime.today().strftime('%Y-%m-%d')
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("❌ 日期格式錯誤，請使用 YYYY-MM-DD 格式，或輸入 'today' 使用當前日期。")

def get_tickers_from_file(filename):
    """從檔案讀取股票代碼"""
    if not os.path.exists(filename):
        print(f"❌ 檔案 '{filename}' 找不到，請確認檔案是否存在。")
        return []
    
    print(f"📢 檢查 '{filename}' 檔案內容...")
    with open(filename, "r") as f:
        tickers = [line.strip().upper() for line in f if line.strip()]
    
    if not tickers:
        print("⚠️ 檔案為空，請確認是否有輸入股票代碼！")
    else:
        print(f"✅ 成功讀取 {len(tickers)} 檔股票: {tickers}")
    
    return tickers

# 讀取 out.txt 檔案內的股票代碼
filename = "../data/out.txt"
tickers = get_tickers_from_file(filename)

if not tickers:
    print("❌ 沒有讀取到任何股票代碼，程式結束。")
    exit()

# 取得股票的公司名稱
tickers_names = {}
for ticker in tickers:
    print(f"📢 嘗試獲取 {ticker} 的公司名稱...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if "longName" in info:
            tickers_names[ticker] = info["longName"]
            print(f"✅ {ticker} 對應公司名稱: {tickers_names[ticker]}")
        else:
            tickers_names[ticker] = ticker  # 若無法獲取公司名稱，則使用代碼
            print(f"⚠️ 無法獲取 {ticker} 的公司名稱，使用默認名稱。")
    except Exception as e:
        print(f"❌ 獲取 {ticker} 公司名稱失敗: {e}")

# 讓使用者輸入開始和結束日期
'''start_date = get_valid_date("Enter start date (YYYY-MM-DD or 'today'): ")
end_date = get_valid_date("Enter end date (YYYY-MM-DD or 'today'): ")
'''
start_date = "2025-02-01"
end_date = "2025-02-11"
if start_date > end_date:
    print("❌ 開始日期不能晚於結束日期，請重新輸入。")
    exit()

# 測試 yfinance 是否可以下載數據
print("📢 測試 yfinance 下載股票數據...")
try:
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    print("✅ 下載完成，前幾行數據:")
    print(data.head())
except Exception as e:
    print(f"❌ 無法下載數據: {e}")
    exit()

# 檢查數據是否為空
if data.empty:
    print(f"⚠️ 找不到 {start_date} - {end_date} 的任何股票資料。")
    exit()

# 整理數據
stock_data_list = []
for ticker in tickers:
    if ticker in data.columns:
        df = data[[ticker]].dropna().reset_index()
        if not df.empty:
            df.rename(columns={'Date': 'Date', ticker: 'Close'}, inplace=True)
            df['Ticker'] = ticker
            df['Company Name'] = tickers_names.get(ticker, ticker)  # 預防某些股票找不到名稱
            stock_data_list.append(df)

if stock_data_list:
    final_data = pd.concat(stock_data_list, ignore_index=True)
    final_data.to_csv("data.csv", index=False)
    print(f"✅ 股票數據已成功儲存至 data.csv（共 {len(tickers)} 檔股票）")
else:
    print(f"⚠️ 所有股票在 {start_date} - {end_date} 期間內沒有可用數據。")

