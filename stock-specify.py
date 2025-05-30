import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def get_tickers_info_from_file(filepath: Path) -> list[tuple[str, str, str]]:
    """從 constituents.csv 讀取股票代碼、公司名稱與 GICS"""
    if not filepath.exists():
        print(f"X 檔案 '{filepath}' 找不到，請確認檔案是否存在。")
        return []

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"X 讀取 CSV 檔案時發生錯誤: {e}")
        return []

    required_columns = {"Symbol", "Security", "GICS Sector"}
    if not required_columns.issubset(df.columns):
        print(f"X 檔案缺少必要欄位: {required_columns - set(df.columns)}")
        return []

    tickers_info = []
    for _, row in df.iterrows():
        ticker = str(row["Symbol"]).strip().upper().replace(".", "-")  # 處理如 BRK.B -> BRK-B
        name = str(row["Security"]).strip()
        gics = str(row["GICS Sector"]).strip()
        tickers_info.append((ticker, name, gics))

    return tickers_info

def fetch_prices_by_date(tickers_info: list[tuple[str, str, str]], target_date: str) -> pd.DataFrame:
    """使用 yfinance 抓取指定日期的股票收盤價，並依 GICS 與 Ticker 排序"""
    try:
        date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print(f"X 日期格式錯誤，請使用 YYYY-MM-DD。收到: {target_date}")
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
        except Exception as e:
            print(f"X 取得 {ticker} 的數據時發生錯誤: {e}")

    df = pd.DataFrame(results, columns=["Ticker", "Company Name", "GICS", "Price", "Date"])

    # 排序：先 GICS，再 Ticker
    df.sort_values(by=["GICS", "Ticker"], inplace=True)

    return df

def main():
    filepath = Path("./constituents.csv")
    tickers_info = get_tickers_info_from_file(filepath)

    if not tickers_info:
        print("X 沒有讀取到任何股票資訊，程式結束")
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
        print("! 沒有任何收盤資料可供儲存(可能是假日)")

if __name__ == "__main__":
    main()

