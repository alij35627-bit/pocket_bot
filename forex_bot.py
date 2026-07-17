import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime, timedelta
from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def home(): return "Gemini Jaafar Pro Max is Active and Hunting!"

BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_msg(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
    except: pass

def run_bot():
    print("نظام جيمييني جعفر برو ماكس بدأ العمل...")
    symbols = ["EURUSD=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X"]
    
    while True:
        for symbol in symbols:
            try:
                df = yf.download(symbol, period="5d", interval="1m", progress=False)
                if len(df) < 60: continue
                
                # التحليل الفني للمحترفين
                close = df['Close']
                rsi = ta.rsi(close, length=14)
                macd = ta.macd(close)
                ema_fast = ta.ema(close, length=9)
                ema_slow = ta.ema(close, length=21)
                
                # فلتر "ذكاء السوق": التحقق من استقرار الشموع
                body_size = abs(df['Close'].iloc[-1] - df['Open'].iloc[-1])
                avg_body = abs(df['Close'] - df['Open']).rolling(20).mean().iloc[-1]
                
                # إذا كانت الشمعة الحالية أكبر بـ 3 مرات من المتوسط، فهذا يعني "خبر" أو "تلاعب"
                if body_size > (avg_body * 3): continue 
                
                # منطق القرار: "برو ماكس"
                score = 0
                # شرط 1: تقاطع EMA
                if ema_fast.iloc[-1] > ema_slow.iloc[-1]: score += 30
                # شرط 2: RSI في مناطق مثالية
                if 30 < rsi.iloc[-1] < 70: score += 30
                # شرط 3: إيجابية الـ MACD
                if macd['MACD_12_26_9'].iloc[-1] > macd['MACDs_12_26_9'].iloc[-1]: score += 40
                
                if score >= 90: # لن يرسل إلا إذا كانت الفرصة "كاملة"
                    t = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
                    msg = (f"👑 **Gemini Jaafar Pro Max** 👑\n"
                           f"══════════════════\n"
                           f"👤 جعفر، السوق مهيأ تماماً:\n"
                           f"💱 الزوج: {symbol.replace('=X', '')}\n"
                           f"📈 التوصية: دخول قوي (BUY)\n"
                           f"📊 مستوى الدقة: {score}%\n"
                           f"⏰ وقت الدخول: {t}\n"
                           f"══════════════════\n"
                           f"اللهم يا ميسّر كل عسير، توكلنا على الله.")
                    send_msg(msg)
                    time.sleep(300) # راحة للبوت
            except: continue
        time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8080)
