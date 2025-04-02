import yfinance as yf
import pandas as pd
import datetime
import time

def get_valid_date(prompt):
    #取得有效的日期，允許使用 'today' 作為當前日期
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

# 讓使用者輸入開始和結束日期
start_date = get_valid_date("Enter start date (YYYY-MM-DD or 'today'): ")
end_date = get_valid_date("Enter end date (YYYY-MM-DD or 'today'): ")

if start_date > end_date:
    print("❌ 開始日期不能晚於結束日期，請重新輸入。")
    exit()

# 下載數據（批量處理，提高效率）
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
            df['Company Name'] = tickers_names.get(ticker, ticker)  # 預防某些股票找不到名稱
            stock_data_list.append(df)

# 組合數據
if stock_data_list:
    final_data = pd.concat(stock_data_list, ignore_index=True)
    
    # 轉換數據結構，使日期為行，Ticker 和 Company Name 為列
    final_data = final_data.pivot_table(index='Date', columns=['Ticker', 'Company Name'], values='Close')
    
    # 將數據寫入 CSV 檔案
    final_data.to_csv("stock-close.csv", index=True)
    print(f"✅ 股票數據已成功儲存至 stock-close.csv")
    # print(f"共 {len(tickers)} 檔股票")
else:
    print(f"⚠️ 所有股票在 {start_date} - {end_date} 期間內沒有可用數據。")

