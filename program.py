import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import yfinance as yf
from plyer import notification

class StockMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Stock Price Monitor")
        self.root.geometry("600x650")
        
        self.is_monitoring = False
        self.monitor_thread = None
        self.check_interval = 15  # Check every 15 seconds
        
        input_frame = ttk.LabelFrame(root, text="Add / Update Stock", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(input_frame, text="Ticker:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_ticker = ttk.Entry(input_frame, width=10)
        self.entry_ticker.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Low Target:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_low = ttk.Entry(input_frame, width=10)
        self.entry_low.grid(row=0, column=3, padx=5, pady=5)
        self.entry_low.insert(0, "0")
        
        ttk.Label(input_frame, text="High Target:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_high = ttk.Entry(input_frame, width=10)
        self.entry_high.grid(row=0, column=5, padx=5, pady=5)
        self.entry_high.insert(0, "0")
        
        self.btn_add = ttk.Button(input_frame, text="Add / Update", command=self.add_stock)
        self.btn_add.grid(row=0, column=6, padx=10, pady=5)
        
        list_frame = ttk.Frame(root, padding=10)
        list_frame.pack(fill="both", expand=False)
        
        columns = ("ticker", "low", "high")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=6)
        self.tree.heading("ticker", text="Ticker")
        self.tree.heading("low", text="Low Target ($)")
        self.tree.heading("high", text="High Target ($)")
        self.tree.column("ticker", anchor="center")
        self.tree.column("low", anchor="center")
        self.tree.column("high", anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.btn_remove = ttk.Button(root, text="Remove Selected Stock", command=self.remove_stock)
        self.btn_remove.pack(pady=5)
        
        self.btn_start = ttk.Button(root, text="▶ START MONITORING", command=self.start_monitoring)
        self.btn_start.pack(pady=5)
        
        self.btn_stop = ttk.Button(root, text="⏹ STOP", command=self.stop_monitoring, state="disabled")
        self.btn_stop.pack(pady=5)
        
        log_frame = ttk.LabelFrame(root, text="Live Output", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, state="disabled", wrap="word", height=10)
        self.log_text.pack(fill="both", expand=True)

    def log(self, message):
        """Safely print text to the GUI text box."""
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")  # Auto-scroll to bottom
        self.log_text.config(state="disabled")

    def add_stock(self):
        ticker = self.entry_ticker.get().upper().strip()
        try:
            low = float(self.entry_low.get())
            high = float(self.entry_high.get())
        except ValueError:
            messagebox.showerror("Input Error", "Targets must be numbers.")
            return

        if not ticker:
            messagebox.showerror("Input Error", "Ticker cannot be empty.")
            return
            
        # Check if already exists and update, else insert new
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == ticker:
                self.tree.item(item, values=(ticker, low, high))
                self.entry_ticker.delete(0, 'end')
                return

        self.tree.insert("", "end", values=(ticker, low, high))
        self.entry_ticker.delete(0, 'end')

    def remove_stock(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                self.tree.delete(item)

    def get_stocks_from_gui(self):
        """Reads the current stocks directly from the Treeview table."""
        stocks = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            stocks.append((values[0], float(values[1]), float(values[2])))
        return stocks

    def get_current_price(self, ticker_symbol):
        try:
            stock = yf.Ticker(ticker_symbol)
            data = stock.history(period='1d')
            if not data.empty:
                return data['Close'].iloc[0]
            return None
        except Exception:
            return None

    def start_monitoring(self):
        if not self.get_stocks_from_gui():
            messagebox.showwarning("Warning", "Add at least one stock first!")
            return
            
        self.is_monitoring = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.log("🟢 Monitoring Started...")
        
        # Start the background thread
        self.monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.is_monitoring = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.log("🔴 Monitoring Stopped.")

    def monitoring_loop(self):
        while self.is_monitoring:
            stocks = self.get_stocks_from_gui()
            self.log(f"\n--- Checking {len(stocks)} stocks at {time.strftime('%H:%M:%S')} ---")
            
            triggered_alerts = []

            for ticker, low, high in stocks:
                if not self.is_monitoring: break # Exit immediately if stop button pressed
                
                price = self.get_current_price(ticker)
                
                if price is not None:
                    self.log(f" {ticker}: ${price:.2f}")
                    
                    if low > 0 and price <= low:
                        triggered_alerts.append(f"📉 {ticker}: ${price:.2f} (Below ${low:.2f})")
                    elif high > 0 and price >= high:
                        triggered_alerts.append(f"📈 {ticker}: ${price:.2f} (Above ${high:.2f})")
                else:
                    self.log(f" {ticker}: Data N/A")

            if triggered_alerts and self.is_monitoring:
                self.log("⚠️ ALARM TRIGGERED!")
                notification.notify(
                    title="🚨 Stock Price Alert! 🚨",
                    message="\n".join(triggered_alerts),
                    app_name="Stock Monitor",
                    timeout=10
                )
            
            # Wait for interval, but check every 1 sec if user pressed "Stop"
            for _ in range(self.check_interval):
                if not self.is_monitoring: break
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockMonitorApp(root)
    root.mainloop()
