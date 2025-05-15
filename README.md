### Introduce
- `constituents.csv` 包含標普500的公司  
- `stock-specify.py` 可以取得指定日期的標普500公司的收盤價
- `scrape.py` 請參閱下方說明
- `data.py` 處理csv檔案中的資料
- `sp-simulate.py` 模擬計算標普500指數

### License
AGPL v3

### Thanks
[Google Gemini](http://gemini.google.com/) @Google
> 註：部分程式碼是由 Google Gemini 所產生  

[ChatGPT](https://chatgpt.com/) @OpenAI  
> 註：部分程式碼是由 ChatGPT 所產生

### 第三方程式碼與授權聲明

本專案使用了以下第三方開源程式碼，特此說明來源與授權內容：
- `scrape.py`
- 來源專案：[datasets/s-and-p-500-companies](https://github.com/datasets/s-and-p-500-companies)
- 原始檔案連結：[scripts/scrape.py](https://github.com/datasets/s-and-p-500-companies/blob/main/scripts/scrape.py)
- 授權方式：MIT License

### Archive
archive.tar.gz
- `less-data.py` 取得 constituents.csv 的股票代碼，可以搭配 `sp-simulate.py` 或其他程式使用
- `sp-simulate` 模擬計算標普500指數
- `stock-period.py` 可以取得指定時間內標普500公司的收盤價  
- `stock-latest.py` 可以取得最近一次的標普500公司的收盤價
- `link-data.c` 可以把股票代碼、公司名稱以及GICS放到 `out.txt` 中  
- `info.c` 可以將資料行數，最長的資料字元數，以及個別資料的最長字元數放入`info.txt`   
- `sort.c` 會把 `out.txt` 的內容進行排序(根據字母以及GICS)，將結果放入`sort.txt`
- `gics-sort.c` 大部分和 sort.c 一樣，但會根據使用者的輸入進行篩選，將結果放入`gics-sort.txt`
