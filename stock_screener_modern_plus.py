# stock_screener_modern_plus.py

import sys
import pandas as pd
import numpy as np
import yfinance as yf
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

# --- Helper functions ---

def compute_rsi(series, period=14):
    delta = series.diff().dropna()
    up, down = delta.clip(lower=0), -1 * delta.clip(upper=0)
    ma_up, ma_down = up.rolling(period).mean(), down.rolling(period).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not rsi.empty else float("nan")


def make_reason_text(codes):
    mapping = {
        "price>50MA": "Price above 50-day average",
        "price>200MA": "Price above 200-day average",
        "low PE": "Low P/E ratio",
        "reasonable PE": "Reasonable P/E ratio",
        "high PE": "High P/E ratio",
        "RSI<30": "RSI indicates oversold",
        "RSI>70": "RSI indicates overbought"
    }
    return "\n".join(mapping.get(c.strip(), c) for c in codes.split(";") if c)


def make_recommendation(score, leverage=False):
    if score >= 2:
        return "Strong Buy (consider leverage)" if leverage else "Strong Buy"
    elif score >= 1:
        return "Buy / Hold"
    elif score >= 0:
        return "Neutral"
    else:
        return "Avoid / Risky"


def calculate_growth(hist):
    if hist.empty:
        return (np.nan, np.nan, np.nan, np.nan)
    last_close = hist["Close"].iloc[-1]
    one_day = (last_close - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2] * 100 if len(hist) > 1 else np.nan
    one_week = (last_close - hist["Close"].iloc[-5]) / hist["Close"].iloc[-5] * 100 if len(hist) >= 5 else np.nan
    one_year = (last_close - hist["Close"].iloc[-252]) / hist["Close"].iloc[-252] * 100 if len(hist) >= 252 else np.nan
    alltime = (last_close - hist["Close"].iloc[0]) / hist["Close"].iloc[0] * 100
    return (one_day, one_week, one_year, alltime)


def score_ticker(ticker):
    try:
        tk = yf.Ticker(ticker)
        hist = tk.history(period="max", interval="1d")
        info = tk.info if hasattr(tk, "info") else {}
        last = hist["Close"].iloc[-1] if not hist.empty else np.nan
        score, reasons = 0, []

        if not hist.empty:
            ma50 = hist["Close"].rolling(50, min_periods=20).mean().iloc[-1]
            if last > ma50:
                score += 1
                reasons.append("price>50MA")
            ma200 = hist["Close"].rolling(200, min_periods=50).mean().iloc[-1]
            if last > ma200:
                score += 1
                reasons.append("price>200MA")
            rsi = compute_rsi(hist["Close"])
            if rsi < 30:
                score += 1
                reasons.append("RSI<30")
            elif rsi > 70:
                score -= 1
                reasons.append("RSI>70")
        else:
            rsi = np.nan

        pe = info.get("trailingPE") or info.get("forwardPE")
        if pe:
            if pe < 10:
                score += 1
                reasons.append("low PE")
            elif pe < 25:
                score += 0.5
                reasons.append("reasonable PE")
            elif pe > 70:
                score -= 1
                reasons.append("high PE")

        growth_1d, growth_1w, growth_1y, growth_all = calculate_growth(hist)

        return {
            "ticker": ticker,
            "score": score,
            "price": last,
            "pe": pe,
            "rsi": rsi,
            "reasons": ";".join(reasons),
            "growth_1d": growth_1d,
            "growth_1w": growth_1w,
            "growth_1y": growth_1y,
            "growth_all": growth_all
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "score": -99,
            "price": "-",
            "pe": "-",
            "rsi": "-",
            "reasons": str(e),
            "growth_1d": np.nan,
            "growth_1w": np.nan,
            "growth_1y": np.nan,
            "growth_all": np.nan
        }


# --- Worker Thread ---

class Worker(QtCore.QThread):
    progress_signal = QtCore.pyqtSignal(int)
    result_signal = QtCore.pyqtSignal(list)

    def __init__(self, tickers):
        super().__init__()
        self.tickers = tickers

    def run(self):
        results = []
        total = len(self.tickers)
        for idx, t in enumerate(self.tickers, start=1):
            results.append(score_ticker(t))
            self.progress_signal.emit(int(idx / total * 100))
        self.result_signal.emit(results)


# --- GUI ---

class StockScreenerGUI(QtWidgets.QWidget):
    def __init__(self, tickers):
        super().__init__()
        self.tickers = tickers
        self.df_results = pd.DataFrame()
        self.dark_mode = True
        self.setWindowTitle("📊 Modern Stock Screener Plus")
        self.setGeometry(150, 100, 1550, 750)

        layout = QtWidgets.QVBoxLayout()

        # Title
        self.title = QtWidgets.QLabel("📊 Stock Screener Dashboard")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title)

        # Controls
        controls = QtWidgets.QHBoxLayout()
        self.run_button = QtWidgets.QPushButton("▶ Run Screener")
        self.run_button.setFixedWidth(130)
        self.run_button.clicked.connect(self.run_screener)

        self.leverage_checkbox = QtWidgets.QCheckBox("Enable Leverage")
        self.light_mode_checkbox = QtWidgets.QCheckBox("Light Mode")
        self.light_mode_checkbox.stateChanged.connect(self.toggle_theme)

        self.export_button = QtWidgets.QPushButton("💾 Export CSV")
        self.export_button.clicked.connect(self.export_csv)
        self.export_button.setFixedWidth(120)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Filter by ticker or name...")
        self.search_input.textChanged.connect(self.filter_table)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.progress.setFixedHeight(20)

        controls.addWidget(self.run_button)
        controls.addWidget(self.leverage_checkbox)
        controls.addWidget(self.light_mode_checkbox)
        controls.addWidget(self.export_button)
        controls.addWidget(self.search_input)
        controls.addWidget(self.progress)
        controls.addStretch()
        layout.addLayout(controls)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
            ["Ticker", "Score", "Price", "PE", "RSI", "1D %", "1W %", "1Y %", "AllTime %", "Reasons", "Recommendation"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg_color = "#2c3e50"
            alt_bg = "#34495e"
            text_color = "#ecf0f1"
            header_bg = "#1abc9c"
        else:
            bg_color = "#ecf0f1"
            alt_bg = "#bdc3c7"
            text_color = "#2c3e50"
            header_bg = "#3498db"

        self.setStyleSheet(f"background-color: {bg_color};")
        self.title.setStyleSheet(f"font-size:20px; font-weight:bold; color:{text_color}; padding:10px;")
        self.table.setStyleSheet(f"""
            QTableWidget {{
                gridline-color: #7f8c8d;
                font-size: 13px;
                background-color: {bg_color};
                color: {text_color};
                alternate-background-color: {alt_bg};
            }}
            QHeaderView::section {{
                background-color: {header_bg};
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }}
            QTableWidget::item:selected {{
                background-color: #16a085;
            }}
        """)

    def toggle_theme(self):
        self.dark_mode = not self.light_mode_checkbox.isChecked()
        self.apply_theme()

    def run_screener(self):
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.worker = Worker(self.tickers)
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.result_signal.connect(self.on_results_ready)
        self.worker.start()

    def on_results_ready(self, results):
        self.df_results = pd.DataFrame(results).sort_values("score", ascending=False)
        self.populate_table(self.df_results)
        self.progress.setVisible(False)

    def populate_table(self, df):
        self.table.setRowCount(len(df))
        leverage = self.leverage_checkbox.isChecked()

        for i, row in df.iterrows():
            vals = [
                str(row["ticker"]),
                f"{row['score']:.2f}",
                f"${row['price']:.2f}" if not pd.isna(row["price"]) else "-",
                f"{row['pe']:.1f}" if row["pe"] else "-",
                f"{row['rsi']:.1f}" if not pd.isna(row["rsi"]) else "-",
                f"{row['growth_1d']:.2f}%" if not pd.isna(row["growth_1d"]) else "-",
                f"{row['growth_1w']:.2f}%" if not pd.isna(row["growth_1w"]) else "-",
                f"{row['growth_1y']:.2f}%" if not pd.isna(row["growth_1y"]) else "-",
                f"{row['growth_all']:.2f}%" if not pd.isna(row["growth_all"]) else "-",
                make_reason_text(row["reasons"]),
                make_recommendation(row["score"], leverage=leverage)
            ]
            for j, val in enumerate(vals):
                item = QtWidgets.QTableWidgetItem(val)
                if j != 9:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                else:
                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

                if j == 1:
                    sc = row["score"]
                    if sc > 0:
                        item.setBackground(QtGui.QColor(46, 204, 113, 160))
                    elif sc < 0:
                        item.setBackground(QtGui.QColor(231, 76, 60, 160))

                if j in [5,6,7,8] and "%" in val:
                    try:
                        num = float(val.strip("%"))
                        if num > 0:
                            item.setForeground(QtGui.QBrush(QtGui.QColor("#2ecc71")))
                        elif num < 0:
                            item.setForeground(QtGui.QBrush(QtGui.QColor("#e74c3c")))
                        else:
                            item.setForeground(QtGui.QBrush(QtGui.QColor("#7f8c8d")))
                    except:
                        pass

                self.table.setItem(i, j, item)
        self.table.resizeRowsToContents()

    def filter_table(self):
        text = self.search_input.text().upper()
        for i in range(self.table.rowCount()):
            ticker_item = self.table.item(i, 0)
            reason_item = self.table.item(i, 9)
            if ticker_item and text in ticker_item.text().upper() or (reason_item and text in reason_item.text().upper()):
                self.table.setRowHidden(i, False)
            else:
                self.table.setRowHidden(i, True)

    def export_csv(self):
        if self.df_results.empty:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            self.df_results.to_csv(path, index=False)


# --- Main ---

if __name__ == "__main__":
    tickers = [
        "AAPL", "MSFT", "TSLA", "NVDA", "AMD", "INTC",
        "F", "NIO", "XOM", "PFE", "KO",
        "PLTR", "SHOP", "SQ", "BYND"
    ]
    app = QtWidgets.QApplication(sys.argv)
    window = StockScreenerGUI(tickers)
    window.show()
    sys.exit(app.exec_())
