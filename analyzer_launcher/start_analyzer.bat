@echo off
cd /d "D:\ITstuff\Projects\PDF_Contract_Analyzer"
call .venv\Scripts\activate
start http://127.0.0.1:8000
python run.py
pause
