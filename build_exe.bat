@echo off
echo Installing tools...
pip install -r requirements.txt pyinstaller
echo Building exe...
pyinstaller --onefile --noconsole --name QRGenerator qr_app.py
echo.
echo Done! Your app is in the "dist" folder: dist\QRGenerator.exe
pause
