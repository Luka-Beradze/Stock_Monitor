
## Stock Price Monitor (GUI Edition)

A lightweight, fully interactive desktop application that monitors real-time stock prices using Yahoo Finance. Unlike the CLI version, this app features a clean Graphical User Interface (GUI) where you can dynamically add, edit, and remove stock targets on the fly without ever touching the code.

*<img width="598" height="673" alt="image" src="https://github.com/user-attachments/assets/ff720858-3b23-4e34-8c04-8b5c44526b09" />*

### Features
* **Interactive UI:** Add, update, or remove stocks and price targets directly from the app.
* **No Code Editing Required:** Manage your portfolio entirely through the graphical interface.
* **Dual-Direction Alerts:** Set alerts for when a stock *drops below* a certain price, *rises above* a certain price, or both.
* **Native Desktop Notifications:** Pops up directly on Windows/Mac without needing a third-party app.
* **Live Activity Log:** Real-time, auto-scrolling log of current prices directly inside the application window.
* **Background Threading:** The app runs smoothly and won't freeze while pulling data from the internet.

### How to Use

If you downloaded the pre-built `.exe` file, simply double-click it to run! No installation required.

1. **Add a Stock:** Type the Ticker (e.g., `SPCX`, `AAPL`), set your Low Target and High Target, and click **Add / Update**.
2. **Monitor Only:** If you just want to watch the price without getting an alarm, leave the targets at `0`.
3. **Start:** Click **▶ START MONITORING**. The app will fetch live prices every 15 seconds.
4. **Alerts:** You can minimize the app. If a price boundary is crossed, a native Windows/Mac notification will pop up on your screen.

### Running from Source (For Developers)

If you prefer to run the raw Python script instead of the `.exe`:

1. **Clone the Branch.**

   1.5. `git checkout gui-branch  # (If applicable)`

2. **Install required dependencies:**
   ```bash
   pip install yfinance plyer
   ```

3. **Run the app:**
   ```bash
   python program.py
   ```

### Building the `.exe` Yourself

Want to compile the `.exe` file yourself? We use `PyInstaller` to package the app.

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the build command inside the project folder:
   ```bash
   python -m PyInstaller --noconsole --onefile --hidden-import plyer.platforms.win.notification program.py
   ```
   *(Note for Windows users: Use `py` instead of `python` if your system paths are not set up).*

3. Once finished, navigate to the newly created `dist` folder. Your standalone `program.exe` will be waiting inside!

---
*Disclaimer: Data is pulled via the `yfinance` library, which relies on Yahoo Finance's publicly available APIs. Use at your own discretion; not intended for high-frequency algorithmic trading.*
