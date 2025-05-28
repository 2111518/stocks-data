import pandas as pd
import os

def sort_csv_by_gics_and_ticker(input_file: str, output_file: str):
    # 讀取 CSV 檔案
    df = pd.read_csv(input_file)

    # 確保必要欄位存在
    required_columns = {"Ticker", "Company Name", "GICS", "Price", "Date"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"輸入檔案缺少必要欄位: {required_columns - set(df.columns)}")

    # 根據 GICS 和 Ticker 排序
    df_sorted = df.sort_values(by=["GICS", "Ticker"])

    # 寫入排序後的 CSV
    df_sorted.to_csv(output_file, index=False)

# === 範例使用 ===
file = input("path to file: ")

# 拆出路徑與檔名
dir_name = os.path.dirname(file)
base_name = os.path.basename(file)
name_only, ext = os.path.splitext(base_name)

# 新的輸出檔案名稱
sorted_file = os.path.join(dir_name, f"sorted_{name_only}{ext}")

# 執行排序
sort_csv_by_gics_and_ticker(file, sorted_file)

