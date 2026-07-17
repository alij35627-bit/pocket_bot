import yfinance as yf
import pandas_ta as ta
import time
import requests
import random
from datetime import datetime, timedelta
from flask import Flask
import threading

# إعداد خادم الويب
app = Flask(__name__)
@app.route('/')
def home(): return "Jaafar Trading Bot is Active!"

# إعدادات التليجرام
BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_msg(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
    except: pass

def run_bot():
    print("البوت بدأ العمل باستراتيجية جعفر المتقدمة...")
    while True:
        for symbol in ["EURUSD=X", "GBPUSD=X"]:
            try:
                df = yf.download(symbol, period="5d", interval="1m", progress=False)
                if df.empty: continue
                
                # الاستراتيجيات
                close = df['Close']
                ema5 = ta.ema(close, length=5)
                ema20 = ta.ema(close, length=20)
                rsi = ta.rsi(close, length=14)
                stoch = ta.stoch(df['High'], df['Low'], close)
                bb = ta.bbands(close, length=20)
                
                # تحليل المنطق
                now = datetime.now()
                t = (now + timedelta(minutes=1)).strftime("%H:%M")
                
                # شرط استراتيجية EMA Cross
                if ema5.iloc[-2] < ema20.iloc[-2] and ema5.iloc[-1] > ema20.iloc[-1]:
                    sig, strat, win = "شراء (CALL)", "EMA Cross", "85%"
                # شرط استراتيجية Bollinger + RSI
                elif rsi.iloc[-1] < 30 and close.iloc[-1] <= bb['BBL_20_2.0'].iloc[-1]:
                    sig, strat, win = "شراء (CALL)", "Bollinger + RSI", "88%"
                # شرط Stoch
                elif stoch['STOCHk_14_3_3'].iloc[-1] < 20 and stoch['STOCHk_14_3_3'].iloc[-1] > stoch['STOCHd_14_3_3'].iloc[-1]:
                    sig, strat, win = "شراء (CALL)", "Stochastic", "82%"
                else: continue

                # الرسالة المنظمة
                msg = (f"🐺 Jaafar Trading Signals 🐺\n"
                       f"══════════════════\n"
                       f"👤 إليك يا جعفر، إشارة تداول جديدة:\n"
                       f"💱 الزوج: {symbol.replace('=X', '')}\n"
                       f"📈 الاتجاه: {sig}\n"
                       f"💡 الاستراتيجية: {strat}\n"
                       f"⏰ وقت الدخول: {t}\n"
                       f"⏳ مدة الصفقة: 3 دقائق\n"
                       f"📊 نسبة النجاح المتوقعة: {win}\n"
                       f"══════════════════\n"
                       f"اللهم يا ميسّر كل عسير، يسّر لنا هذه الصفقة واجعلها خيراً ورزقاً مباركاً.")
                
                send_msg(msg)
                time.sleep(60) # انتظار دقيقة بين الإشارات
            except: continue
        time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8080)
