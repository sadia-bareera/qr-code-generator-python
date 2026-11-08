# QR Code Generator

A simple desktop app built with Python and Tkinter that turns any text or link into a QR code you can save as an image.

## Features
- Generate a QR code from any text, URL, phone number or Wi-Fi string
- Custom QR and background colors
- Adjustable size slider
- Optional logo in the center of the QR
- Live preview and Save as PNG
- Press Enter as a shortcut for Generate

## Tech Used
- Python 3
- Tkinter (GUI)
- qrcode (QR generation)
- Pillow (image handling)

## How to Run
1. Clone the repo
   ```
   git clone https://github.com/sadia-bareera/qr-generator.git
   cd qr-generator
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the app
   ```
   python qr_app.py
   ```

## Usage
1. Type or paste text or a link into the box
2. Optional: pick colors, move the size slider, add a logo
3. Click **Generate QR**
4. Click **Save as PNG** to download it

## Build a Windows .exe
Double-click `build_exe.bat` (or run `pyinstaller --onefile --noconsole --name QRGenerator qr_app.py`).
Your app will be in the `dist` folder as `QRGenerator.exe`.

## Author
Sadia Bareera
