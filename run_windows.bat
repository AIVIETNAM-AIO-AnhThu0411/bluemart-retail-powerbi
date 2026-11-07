@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
    echo Khong tim thay Python launcher 'py'. Hay cai Python 3.11/3.12 tu python.org.
    pause
    exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
    echo Tao moi truong Python...
    py -3 -m venv .venv
    if errorlevel 1 (pause & exit /b 1)
)
echo Cai dat thu vien, can Internet lan dau...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (pause & exit /b 1)
echo Mo http://localhost:8501 khi Streamlit san sang...
".venv\Scripts\python.exe" -m streamlit run app.py
pause
