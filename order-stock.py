import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def normalize_ticker(symbol: str) -> str:
    # 將股票代碼標準化：主代碼與後綴都大寫
    if "." in symbol:
        base, suffix = symbol.split(".", 1)
        return f"{base.upper()}.{suffix.upper()}"
    else:
        return symbol.upper()

def main():
    # 1. 使用者輸入股票代碼
    raw_input = input("請輸入股票代碼: ").strip()
    ticker_input = normalize_ticker(raw_input)
    price = "Close"
    # 2. 使用者輸入開始與結束日期
    start_date_input = input("請輸入開始日期(YYYY-MM-DD): ").strip()
    end_date_input = input("請輸入結束日期(YYYY-MM-DD): ").strip()

    # 3. 驗證日期格式與時間差
    try:
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
        if end_date - start_date < timedelta(days=1):
            print("X 結束日期需晚於開始日期至少一天")
            return
    except ValueError:
        print("X 日期格式錯誤，請使用 YYYY-MM-DD")
        return

    # 4. 抓取股票資料
    ticker = yf.Ticker(ticker_input)
    company_name = ticker.info.get("longName", "N/A")

    # 5. 抓取歷史收盤價
    hist = ticker.history(start=start_date_input, end=end_date_input)
    if hist.empty:
        print("X 查無資料，請確認股票代碼與時間區間")
        return

    # 6. 整理成 CSV 格式
    df = pd.DataFrame({
        "股票名": ticker_input,
        "公司名": company_name,
        "股價": hist[price].values,
        "日期": hist.index.strftime("%Y-%m-%d")
    })
    code = ticker_input.replace(".", "-")
    price_lower = price.lower()
    filename = f"{code}-{price_lower}-{start_date_input}-{end_date_input}.csv"
    df.to_csv(filename, index=False)
    print(f"V 資料已保存")
    # print(f"V 資料已保存至 {filename}")

if __name__ == "__main__":
    main()

