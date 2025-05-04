import pandas as pd

def load_tickers(filepath="constituents.csv"):
    """
    從 constituents.csv 載入所有股票代碼。
    回傳：股票代碼的字串清單。
    """
    df = pd.read_csv(filepath)
    
    # 僅取出 Symbol 欄位（股票代碼），並轉為清單
    tickers = df["Symbol"].dropna().astype(str).tolist()
    
    return tickers

