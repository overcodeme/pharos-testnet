cls

cd /d "%~dp0"

echo Virtual environment activating...
call .venv\Scripts\activate

echo Script running...
python main.py

echo Script has finished
pause