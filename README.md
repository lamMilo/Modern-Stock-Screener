# 📊 Modern Stock Screener Plus

A **modern, interactive stock screener** built entirely in **Python** with **PyQt5** and **yFinance**.  
This desktop app analyzes multiple stocks and ranks them based on technical and fundamental signals — all displayed in a sleek GUI with dark and light mode support.

---

## 🧠 Overview

| Key Info | Details |
|-----------|----------|
| **Language** | Python 3 |
| **Interface** | PyQt5 (Desktop GUI) |
| **Data Source** | Yahoo Finance via `yfinance` |
| **File** | `stock_screener_modern_plus.py` |
| **Platform** | Cross-platform (Windows / macOS / Linux) |

This app allows traders, investors, and analysts to screen popular stocks and quickly identify **buy**, **hold**, or **avoid** opportunities.

---

## ✨ Features

- 🧮 Real-time stock data from Yahoo Finance  
- 💹 50-day & 200-day moving average analysis  
- 📈 RSI-based momentum scoring  
- 💰 P/E ratio valuation checks  
- 📊 Growth analysis (1D / 1W / 1Y / All-Time)  
- 🌙 Dark / Light mode toggle  
- 💾 Export results to CSV  
- 🔍 Search filter for tickers or reasons  
- ⚡ Multithreaded scanning for smooth performance  
- 📊 Auto recommendations: **Strong Buy**, **Neutral**, **Avoid**  

---

## ⚙️ Requirements

Before running, install the dependencies below:

```bash
pip install pandas numpy yfinance PyQt5
```

You’ll need **Python 3.8+**.

---

## 🚀 How to Run

1. Save the file as `stock_screener_modern_plus.py`  
2. Open a terminal or command prompt in that directory  
3. Run:

```bash
python stock_screener_modern_plus.py
```

4. The graphical dashboard will launch — click **▶ Run Screener** to start analyzing default tickers (AAPL, TSLA, NVDA, etc.)

---

## 📊 Scoring System

| Factor | Condition | Score |
|---------|------------|--------|
| Price > 50MA | Trend confirmation | +1 |
| Price > 200MA | Long-term trend | +1 |
| RSI < 30 | Oversold | +1 |
| RSI > 70 | Overbought | -1 |
| P/E < 10 | Undervalued | +1 |
| P/E < 25 | Reasonable | +0.5 |
| P/E > 70 | Overvalued | -1 |

Higher total scores indicate stronger buying signals.

---

## 🧠 Recommendation Logic

| Score | Recommendation |
|--------|----------------|
| ≥ 2 | 🟢 Strong Buy |
| ≥ 1 | 🟡 Buy / Hold |
| ≥ 0 | ⚪ Neutral |
| < 0 | 🔴 Avoid / Risky |

> Enable **Leverage Mode** for more aggressive recommendations.

---

## 🧩 Example Output

| Ticker | Score | Price | P/E | RSI | 1D % | 1W % | 1Y % | Reasons | Recommendation |
|---------|--------|--------|------|------|--------|--------|--------|----------|----------------|
| AAPL | 2.5 | \$175.30 | 28.4 | 45.2 | 1.12% | 2.45% | 35.80% | Price above 50MA; Reasonable PE | Strong Buy |
| TSLA | 0.5 | \$240.12 | 75.6 | 73.8 | -1.2% | -3.4% | 12.0% | High PE; RSI indicates overbought | Neutral |

---

## 💡 Quick Reference

| Key | Description |
|-----|--------------|
| ▶ Run Screener | Starts stock analysis |
| 💾 Export CSV | Save results to file |
| 🔍 Search | Filter by ticker or reason |
| 🌙 Light Mode | Toggle theme |
| 📈 Score Colors | Green = Positive, Red = Negative |

---

## 🧱 How It Works

1. Fetches stock data via `yfinance`  
2. Calculates indicators:
   - Moving Averages (50 & 200-day)
   - RSI (Relative Strength Index)
   - P/E Ratio (from Yahoo Finance info)
3. Computes growth rates (1D / 1W / 1Y / All-Time)
4. Scores each stock numerically
5. Displays in an interactive table with filters and export options

---

## 📁 File Overview

Everything is contained in **one Python file**:

```
stock_screener_modern_plus.py
```

No other modules or assets are required. The script handles GUI creation, data fetching, and scoring all within this single file.

---

## ⚡ Technologies Used

- **PyQt5** – GUI framework  
- **yFinance** – Market data API  
- **Pandas / NumPy** – Data manipulation and calculations  
- **Multithreading** – To keep the UI responsive while fetching data  

---

## 🧠 Default Tickers

When first launched, the app analyzes:

```
AAPL, MSFT, TSLA, NVDA, AMD, INTC, F, NIO, XOM, PFE, KO, PLTR, SHOP, SQ, BYND
```

You can modify this list in the `if __name__ == "__main__":` section.

---

## 🧮 Example Usage in Code

You can also call parts of this script directly in Python:

```python
from stock_screener_modern_plus import score_ticker

result = score_ticker("AAPL")
print(result)
```

Output:

```python
{
  'ticker': 'AAPL',
  'score': 2.5,
  'price': 175.30,
  'pe': 28.4,
  'rsi': 45.2,
  'reasons': 'price>50MA;reasonable PE',
  'growth_1d': 1.12,
  'growth_1w': 2.45,
  'growth_1y': 35.8
}
```

---

## 🧠 Architecture

### Main Components

- **Helper Functions** – RSI, MA, scoring, growth  
- **Worker Thread** – Background stock scanning  
- **PyQt5 GUI** – Table view, search, progress bar, theme switch  
- **Export System** – Saves filtered results to CSV  

---

## 🧾 License

This project is released under the **MIT License**.  
You may use, modify, or distribute freely with attribution.

---

## 🙌 Credits

- **PyQt5 Community** – GUI framework support  
- **Yahoo Finance (yFinance)** – Market data provider  
- **NumPy / Pandas** – Data analysis libraries  

---

## ⭐ Support

If you enjoy this project, please consider **starring the repository ⭐** —  
it helps others find it and supports future improvements.

## ⚖️ Disclaimer

 This software is provided for **educational and informational purposes only**.  
 It does **not constitute financial, investment, or trading advice**.  
 All stock data and analysis results are retrieved from **third-party sources (Yahoo Finance)**, and accuracy is **not guaranteed**.  
  
 Always perform your own due diligence and consult a **licensed financial advisor** before making investment decisions.  
  
 The author(s) assume **no liability or responsibility** for any losses, damages, or consequences resulting from the use of this software.  
  
 Use this application at your **own risk**.
