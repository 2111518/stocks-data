import csv

def sort_data(data):
    return sorted(data, key=lambda row: (row[2], row[0]))  # Symbol, Security, GICS Sector

def load_sector_list(sector_file):
    with open(sector_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def process_csv(filename, output_file, sort=False, filter_by_sector=False, sector_file='sector.txt'):
    processed_data = []

    # 如果啟用篩選，就讀取 sector.txt
    allowed_sectors = set()
    if filter_by_sector:
        allowed_sectors = load_sector_list(sector_file)

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        headers = next(reader)  # 跳過標題列
        for row in reader:
            # 只針對 Symbol (row[0]) 進行字元替換
            symbol = row[0].replace('.', '-')
            trimmed = [symbol, row[1], row[2]]
            if filter_by_sector:
                if trimmed[2] not in allowed_sectors:
                    continue
            processed_data.append(trimmed)

    if sort:
        processed_data = sort_data(processed_data)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for row in processed_data:
            outfile.write('@'.join(row) + '\n')

if __name__ == "__main__":
    # 你可以調整這些參數
    process_csv(
        filename='constituents.csv',
        output_file='out.txt',
        sort=True,                # 是否排序
        filter_by_sector=False,   # 是否根據 sector.txt 過濾
        sector_file='sector.txt'  # GICS Sector 清單檔案
    )

