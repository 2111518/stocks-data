import yfinance as yf
import pandas as pd
import datetime
import time

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

def get_tickers_and_names(filename):
    """從檔案讀取股票代碼與公司名稱（以第一個空格分隔）"""
    tickers = []
    ticker_name_map = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 1)  # 只分割第一個空格
                ticker = parts[0].strip().upper()
                name = parts[1].strip() if len(parts) > 1 else ticker
                tickers.append(ticker)
                ticker_name_map[ticker] = name
    except FileNotFoundError:
        print(f"❌ 檔案 '{filename}' 找不到，請確認檔案是否存在。")
    return tickers, ticker_name_map

# 讀取 data/out.txt 檔案內的股票代碼和公司名稱
filename = "./data/out.txt"
tickers, tickers_names = get_tickers_and_names(filename)

if not tickers:
    print("❌ 沒有讀取到任何股票代碼，程式結束。")
    exit()

# 讓使用者輸入開始和結束日期
start_date = get_valid_date("Enter start date (YYYY-MM-DD or 'today'): ")
end_date = get_valid_date("Enter end date (YYYY-MM-DD or 'today'): ")

if start_date > end_date:
    print("❌ 開始日期不能晚於結束日期，請重新輸入。")
    exit()

# 批量下載股票歷史收盤價
try:
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
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
            df['Company Name'] = tickers_names.get(ticker, ticker)
            stock_data_list.append(df)

# 組合數據
if stock_data_list:
    final_data = pd.concat(stock_data_list, ignore_index=True)
    final_data = final_data.pivot_table(index='Date', columns=['Ticker', 'Company Name'], values='Close')
    final_data.to_csv("stock-close.csv", index=True)
    print(f"✅ 股票數據已成功儲存至 stock-close.csv")
else:
    print(f"⚠️ 所有股票在 {start_date} - {end_date} 期間內沒有可用數據。")

