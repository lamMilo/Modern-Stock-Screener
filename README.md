# 💹 Modern Stock Screener

A **modern, interactive stock screener desktop application** built with **Python** and **PyQt5**. Analyze stocks with key indicators, get recommendations, and view growth metrics in a beautiful, responsive GUI.

> ⚠️ This tool is for **educational purposes only**. Always do your own research before investing.

---

## 🧠 Overview

| Feature | Details |
|---------|---------|
| **Platform** | Desktop (Windows / macOS / Linux) |
| **GUI** | PyQt5 |
| **Stock Data** | Yahoo Finance via `yfinance` |
| **Python Version** | 3.8+ |
| **Indicators** | 50/200-day Moving Average, P/E ratio, RSI |
| **Recommendations** | Buy / Hold / Strong Buy / Avoid (Optional Leverage) |
| **Themes** | Light & Dark Mode |

---

## 📊 Key Features

| Feature | Description |
|---------|-------------|
| **Automated Analysis** | Calculate scores based on price, moving averages, P/E, RSI |
| **Growth Tracking** | 1D / 1W / 1Y / All-time % growth displayed with colors |
| **Recommendations** | Personalized advice with optional leverage guidance |
| **Progress Bar** | Shows scanning progress without freezing GUI |
| **Real-time Search/Filter** | Filter stocks by ticker or reason |
| **Export to CSV** | Save results for later review |
| **Dark / Light Mode** | Switch themes anytime for better visibility |

---

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/lAmMilo/Modern-Stock-Screener.git
cd Modern-Stock-Screener
Install dependencies:

bash
Code kopieren
pip install -r requirements.txt
Dependencies: PyQt5, pandas, numpy, yfinance

⚙️ Usage
Run the application:

bash
Code kopieren
python stock_screener_modern_plus.py
Click Run Screener to start scanning stocks.

Toggle Light / Dark Mode with the checkbox.

Filter stocks using the search bar.

Optionally enable Leverage for recommendations.

Export results via the Export CSV button.

🛠️ Tickers Included
Ticker	Company
AAPL	Apple Inc.
MSFT	Microsoft Corp.
TSLA	Tesla Inc.
NVDA	NVIDIA Corp.
AMD	Advanced Micro Devices
INTC	Intel Corp.
F	Ford Motor Co.
NIO	NIO Inc.
XOM	Exxon Mobil
PFE	Pfizer Inc.
KO	Coca-Cola Co.
PLTR	Palantir
SHOP	Shopify
SQ	Block Inc.
BYND	Beyond Meat

You can add or modify tickers directly in the script.

🖥️ Screenshots

Dark theme with colored growth indicators.


Light theme with filtered stocks.

🧾 Contributing
Contributions are welcome!

Fork the repository.

Create a new branch (git checkout -b feature/your-feature).

Make your changes and commit (git commit -m "Add feature").

Push to your branch (git push origin feature/your-feature).

Open a Pull Request.

⚠️ Disclaimer
This tool is provided as-is without any warranty.
Use at your own risk. Always verify stock information and comply with financial regulations.

⭐ Credits
PyQt5 – GUI framework

yfinance – Stock data source

pandas & numpy – Data processing

Open-source contributors for UI inspiration and stock analysis logic
