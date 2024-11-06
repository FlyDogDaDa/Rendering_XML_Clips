@echo off

cd .\Data
rem 檢查是否已下載 Python 檔案
if exist python.exe (
    echo Python has been downloaded
    goto dependencies
)

rem 下載 Python 檔案
echo Downloading Python
curl "https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe" -O python.exe
rem 安裝 Python
echo Install Python
python.exe


rem 跳轉到安裝依賴套件
:dependencies

rem 安裝依賴套件
echo Install dependency packages
pip install -r requirements.txt

rem 安裝結束
echo The installation is complete

rem 離開Data資料夾
cd ..

rem 交換執行檔位置
MOVE .\Data\Start.py .\Start.py
MOVE .\Install.cmd .\Data\Install.cmd