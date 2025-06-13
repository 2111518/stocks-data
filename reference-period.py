import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime

def get_tickers_info_from_file(filepath: Path) -> list[tuple[str, str, str]]:
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
        ticker = str(row["Symbol"]).strip().upper().replace(".", "-")
        name = str(row["Security"]).strip()
        gics = str(row["GICS Sector"]).strip()
        tickers_info.append((ticker, name, gics))

    return sorted(tickers_info, key=lambda x: (x[2], x[0]))  # 先以 GICS，再以 Symbol 排序

def fetch_prices_by_range(tickers_info: list[tuple[str, str, str]], start_date: str, end_date: str) -> pd.DataFrame:
    try:
        start_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("X 日期格式錯誤，請使用 YYYY-MM-DD")
        return pd.DataFrame()

    tickers = [t[0] for t in tickers_info]
    info_lookup = {t[0]: (t[1], t[2]) for t in tickers_info}  # ticker -> (name, gics)
    stocks = yf.Tickers(" ".join(tickers))

    all_results = []

    for ticker in tickers:
        try:
            stock = stocks.tickers[ticker]
            hist = stock.history(start=start_date, end=end_date)
            if not hist.empty:
                name, gics = info_lookup.get(ticker, (ticker, ""))
                for date, row in hist.iterrows():
                    all_results.append([
                        ticker,
                        name,
                        gics,
                        date.strftime("%Y-%m-%d"),
                        row["Close"]
                    ])
            else:
                print(f"! {ticker} 在區間 {start_date} 到 {end_date} 沒有資料")
        except Exception as e:
            print(f"X 取得 {ticker} 的資料時發生錯誤: {e}")

    df = pd.DataFrame(all_results, columns=["Ticker", "Company Name", "GICS", "Date", "Close"])
    return df.sort_values(by=["GICS", "Ticker", "Date"])

def main():
    filepath = Path("./constituents.csv")
    tickers_info = get_tickers_info_from_file(filepath)

    if not tickers_info:
        print("X 沒有讀取到任何股票資訊，程式結束")
        return

    start_date = input("請輸入起始日期 (YYYY-MM-DD): ").strip()
    end_date = input("請輸入結束日期 (YYYY-MM-DD): ").strip()

    df = fetch_prices_by_range(tickers_info, start_date, end_date)

    if not df.empty:
        output_file = f"stock-range-{start_date}_to_{end_date}.csv"
        df.to_csv(output_file, index=False)
        print(f"📄 資料已儲存到 {output_file}")
    else:
        print("! 沒有任何收盤資料可供儲存(可能是假日或代碼錯誤)")

if __name__ == "__main__":
    main()

