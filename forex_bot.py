import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime, timedelta
from flask import Flask
import threading

# إعداد خادم ويب بسيط لإبقاء التطبيق حياً
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# بيانات التليجرام
BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_msg(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
    except:
        pass

def run_bot():
    print("البوت بدأ العمل في الخلفية...")
    while True:
        for symbol in ["EURUSD=X", "GBPUSD=X"]:
            try:
                df = yf.download(symbol, period="2d", interval="1m", progress=False)
                
                if df.empty or 'Close' not in df.columns: continue
                
                rsi = ta.rsi(df['Close'], length=14)
                if rsi is None or len(rsi) < 1: continue
                
                val = float(rsi.iloc[-1])
                dur = 5 if val < 20 or val > 80 else (4 if val < 25 or val > 75 else (3 if val < 27 or val > 73 else (2 if val < 29 or val > 71 else 1)))
                t = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
                
                if val < 30:
                    send_msg(f"🚀 صفقة (CALL)\nالزوج: {symbol}\nالوقت: {t}\nالمدة: {dur} دقيقة\nRSI: {val:.2f}")
                    time.sleep(3)
                elif val > 70:
                    send_msg(f"🔥 صفقة (PUT)\nالزوج: {symbol}\nالوقت: {t}\nالمدة: {dur} دقيقة\nRSI: {val:.2f}")
                    time.sleep(3)
            except:
                continue
        time.sleep(60)

# تشغيل الخادم والبوت معاً
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_flask()
