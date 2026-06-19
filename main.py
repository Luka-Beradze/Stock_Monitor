import yfinance as yf
import time
from plyer import notification

STOCKS_TO_MONITOR = [
    ## add your stocks here
    ## Format: ("TICKER", LOW_TARGET, HIGH_TARGET)
    ## Set target to 0 if you don't want to set a target for that direction (low or high).
    ("NVDA", 0, 0)
]

"""
#           __Example:__

STOCKS_TO_MONITOR = [
    ("SPCX", 0, 0),       # Monitoring only, no alarms
    ("SPCG", 20, 0),      # Alarm only if price drops <= 20
    ("NVDA", 0, 150),     # Alarm only if price rises >= 150
    ("ASML", 800, 1000)   # Alarm if price drops <= 800 OR rises >= 1000
]
"""

# more than 10 recommended to avoid temprorary IP bans from yahoo finance
CHECK_INTERVAL = 10 # seconds   

def get_current_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        todays_data = stock.history(period='1d')
        if not todays_data.empty:
            current_price = todays_data['Close'].iloc[0]
            return current_price
        return None
    except Exception as e:
        return None

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Stock Monitor",
        timeout=10  
    )

    # initial message 
print("Monitoring started for the following stocks:")
for ticker, low, high in STOCKS_TO_MONITOR:
    if low > 0 and high > 0:
        print(f" - {ticker}: Alert if <= ${low:.2f} OR >= ${high:.2f}")
    elif low > 0:
        print(f" - {ticker}: Alert if <= ${low:.2f}")
    elif high > 0:
        print(f" - {ticker}: Alert if >= ${high:.2f}")
    else:
        print(f" - {ticker}: Monitoring only (No alarms)")
print("Press Ctrl+C to stop.")


while True:
    print(f"\n--- Checked at {time.strftime('%H:%M:%S')} ---")
    
    triggered_alerts = []

    for ticker, low, high in STOCKS_TO_MONITOR:
        price = get_current_price(ticker)
        
        if price is not None:
            print(f"Current Price {ticker}: ${price:.2f}")
            
            if low > 0 and price <= low:
                alert_message = f"📉 {ticker}: ${price:.2f} (Dropped below ${low:.2f})"
                triggered_alerts.append(alert_message)
                
            elif high > 0 and price >= high:
                alert_message = f"📈 {ticker}: ${price:.2f} (Rose above ${high:.2f})"
                triggered_alerts.append(alert_message)
                
        else:
            print(f"Current Price {ticker}: N/A")

    # alarms
    if triggered_alerts:
        print("TARGETS REACHED! Sending combined notification...")
        
        combined_message = "\n".join(triggered_alerts)
        send_notification("🚨 Stock Price Alert! 🚨", combined_message)
        
        time.sleep(6)

    time.sleep(CHECK_INTERVAL)
