import yfinance as yf
import pandas as pd
from pathlib import Path

def get_tickers_and_names_from_file(filepath: Path) -> list[tuple[str, str]]:
    """從檔案讀取股票代碼與公司名稱（以第一個空格分隔）"""
    if not filepath.exists():
        print(f"❌ 檔案 '{filepath}' 找不到，請確認檔案是否存在。")
        return []

    tickers_info = []
    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(" ", 1)
                ticker = parts[0].upper()
                name = parts[1].strip() if len(parts) > 1 else ticker
                tickers_info.append((ticker, name))
    return tickers_info

def fetch_latest_prices(tickers_info: list[tuple[str, str]]) -> pd.DataFrame:
    """使用 yfinance 抓取股票最新收盤價"""
    tickers = [t[0] for t in tickers_info]
    name_lookup = dict(tickers_info)
    stocks = yf.Tickers(" ".join(tickers))

    results = []
    for ticker in tickers:
        try:
            stock = stocks.tickers[ticker]
            hist = stock.history(period="1d")

            if not hist.empty:
                price = hist["Close"].iloc[-1]
                date = hist.index[-1].strftime("%Y-%m-%d")
                results.append([ticker, name_lookup.get(ticker, ticker), price, date])
            else:
                print(f"⚠️ 無法獲取 {ticker} 的歷史數據。")
        except Exception as e:
            print(f"❌ 取得 {ticker} 的數據時發生錯誤: {e}")
    return pd.DataFrame(results, columns=["Ticker", "Company Name", "Price", "Date"])

def main():
    filepath = Path("./data/out.txt")
    tickers_info = get_tickers_and_names_from_file(filepath)

    if not tickers_info:
        print("❌ 沒有讀取到任何股票代碼，程式結束。")
        return

    df = fetch_latest_prices(tickers_info)
    df.to_csv("stock-close-latest.csv", index=False)
    print("📄 資料已儲存到 stock-close-latest.csv")

if __name__ == "__main__":
    main()

