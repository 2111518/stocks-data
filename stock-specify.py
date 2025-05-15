import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def get_tickers_info_from_file(filepath: Path) -> list[tuple[str, str, str]]:
    """從 constituents.csv 讀取 Symbol, Security, GICS Sector，處理特殊符號與格式"""
    if not filepath.exists():
        print(f"❌ 檔案 '{filepath}' 找不到，請確認檔案是否存在。")
        return []

    try:
        df = pd.read_csv(filepath, usecols=["Symbol", "Security", "GICS Sector"])
    except Exception as e:
        print(f"❌ 讀取 CSV 檔時發生錯誤: {e}")
        return []

    # 處理 Symbol 中的 "." 改為 "-"
    df["Symbol"] = df["Symbol"].str.replace(".", "-", regex=False)

    tickers_info = list(df.itertuples(index=False, name=None))
    return tickers_info

def fetch_prices_by_date(tickers_info: list[tuple[str, str, str]], target_date: str) -> pd.DataFrame:
    """使用 yfinance 抓取指定日期的股票收盤價"""
    try:
        date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print(f"❌ 日期格式錯誤，請使用 YYYY-MM-DD。收到: {target_date}")
        return pd.DataFrame()

    tickers = [t[0] for t in tickers_info]
    info_lookup = {t[0]: (t[1], t[2]) for t in tickers_info}  # ticker -> (name, gics)
    stocks = yf.Tickers(" ".join(tickers))

    results = []
    for ticker in tickers:
        try:
            stock = stocks.tickers[ticker]
            hist = stock.history(start=target_date, end=(date_obj + timedelta(days=1)).strftime("%Y-%m-%d"))

            if not hist.empty:
                price = hist["Close"].iloc[0]
                date = hist.index[0].strftime("%Y-%m-%d")
                name, gics = info_lookup.get(ticker, (ticker, ""))
                results.append([ticker, name, gics, price, date])
            else:
                print(f"⚠️ {ticker} 在 {target_date} 沒有交易紀錄（可能為假日）。")
        except Exception as e:
            print(f"❌ 取得 {ticker} 的數據時發生錯誤: {e}")

    return pd.DataFrame(results, columns=["Ticker", "Company Name", "GICS", "Price", "Date"])

def main():
    filepath = Path("./constituents.csv")
    tickers_info = get_tickers_info_from_file(filepath)

    if not tickers_info:
        print("❌ 沒有讀取到任何股票資訊，程式結束。")
        return

    target_date = input("請輸入欲查詢的日期 (YYYY-MM-DD)，直接 Enter 則使用今天: ").strip()
    if not target_date:
        target_date = datetime.today().strftime("%Y-%m-%d")

    df = fetch_prices_by_date(tickers_info, target_date)
    if not df.empty:
        output_file = f"stock-close-{target_date}.csv"
        df.to_csv(output_file, index=False)
        print(f"📄 資料已儲存到 {output_file}")
    else:
        print("⚠️ 沒有任何收盤資料可供儲存。")

if __name__ == "__main__":
    main()

