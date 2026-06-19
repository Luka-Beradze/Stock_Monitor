## Simple Python Stock Monitor

A lightweight, customizable Python script that monitors real-time stock prices using Yahoo Finance and sends native desktop notifications when stocks hit your specific high or low target prices.

### Features
* **Track Multiple Stocks:** Add as many tickers as you want.
* **Dual-Direction Alerts:** Set alerts for when a stock *drops below* a certain price, *rises above* a certain price, or both.
* **Native Desktop Notifications:** Pops up directly on Windows, Mac, or Linux without needing a third-party app.
* **Silent Monitoring:** Option to just print prices to the terminal without triggering alarms.
* **Crash Resistant:** Safely handles dropped internet connections or missing data from Yahoo Finance.

### Prerequisites
You will need standard **Python 3.x** installed on your computer. 
*(Note: Ensure you are using standard Windows Python, not MSYS2/MinGW Python).*

### Installation

1. **Clone the repository** (or download the script directly):
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

2. **Install required libraries:**
   ```bash
   pip install yfinance plyer
   ```
   *(Windows users can use `py -m pip install yfinance plyer` if `pip` is not recognized).*

### Configuration

Open the script in any text editor and look for the `STOCKS_TO_MONITOR` list. 

The system uses a **3-tuple format**: `("TICKER", LOW_TARGET, HIGH_TARGET)`

* Set a target to `0` if you do not want an alarm for that direction.
* Set both targets to `0` if you just want to monitor the price silently in the terminal.

**Examples:**
```python
STOCKS_TO_MONITOR = [
    ("XXXX", 0, 0),       # Monitoring only, no alarms
    ("YYYY", 20, 0),      # Alarm only if price drops <= 20
    ("ZZZZ", 0, 150),     # Alarm only if price rises >= 150
    ("WWW", 800, 1000),  # Alarm if price drops <= 800 OR rises >= 1000
]
```

You can also adjust the `CHECK_INTERVAL` variable to change how often the app refreshes (default is 15-30 seconds recommended to avoid IP bans from Yahoo).

### Usage

Run the script from your terminal:
```bash
python main.py
```
*(Or `py main.py` on Windows)*

The terminal will print out the current prices at your chosen interval. If a target is hit, a desktop notification will appear summarizing which stock triggered the alarm and why (📉 Drop or 📈 Rise).

To stop the script, press `Ctrl + C` in your terminal.

---
*Disclaimer: This is a personal tool. Data is pulled via the `yfinance` library, which relies on Yahoo Finance's publicly available APIs. Use at your own discretion; not intended for high-frequency algorithmic trading.*
