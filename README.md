# stegx

🔒 **stegx** is a simple Python tool for hiding messages or files inside images using **LSB steganography** with optional password protection (AES encryption).  

---

## ✨ Features
- Hide **text messages** or **files** inside PNG images.
- AES-256 encryption with a password.
- Preserves original filenames when extracting.
- CLI interface with intuitive commands.
- Supports both **binary data** and **UTF-8 text**.

---

## 📦 Installation

```bash
git clone https://github.com/<your-username>/stegx.git
cd stegx
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)
pip install -r requirements.txt

🚀 Usage

Hide a text message
python -m stegx.cli hide examples/test.png examples/stego.png --message "Hello World!" --password mypass

Hide a file
python -m stegx.cli hide examples/test.png examples/stego.png --file examples/secret.pdf --password mypass

Reveal hidden data
# Restore into original filename
python -m stegx.cli reveal examples/stego.png --password mypass

# Save to a custom output file
python -m stegx.cli reveal examples/stego.png --password mypass --out examples/revealed.pdf

📂 Project Structure
stegx/
│── stegx/              # Core library
│   ├── cli.py          # Command-line interface
│   ├── crypto_utils.py # AES encryption helpers
│   ├── image_lsb.py    # LSB steganography logic
│
│── examples/           # Example files
│── tests/              # Unit tests
│── requirements.txt    # Dependencies
│── README.md           # Documentation
│── LICENSE             # MIT License

🛠 Requirements

Python 3.8+
Pillow
Cryptography

Install dependencies:
pip install -r requirements.txt

📜 License
This project is licensed under the MIT License
.
© 2025 Rachit Patel