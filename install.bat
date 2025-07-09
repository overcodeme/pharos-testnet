@echo off

echo Virtual environment creating...
python -m venv venv

echo Virtual environment activating...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Successsfully completed installation
pause