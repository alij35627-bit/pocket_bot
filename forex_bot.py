import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime, timedelta

BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_telegram_msg(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
    except:
        pass

symbols = ["EURUSD=X", "GBPUSD=X"]

print("البوت بدأ العمل بنظام الاستقرار العالي...")

while True:
    for symbol in symbols:
        try:
            # استخدام فترة زمنية أطول ومحاولة جلب البيانات
            df = yf.download(symbol, period="5d", interval="1m", progress=False)
            
            if df.empty or 'Close' not in df.columns:
                continue
                
            # حساب المؤشر
            rsi = ta.rsi(df['Close'], length=14)
            
            if rsi is None or len(rsi) < 1:
                continue
            
            val = rsi.iloc[-1]
            
            # التحقق من أن القيمة رقم
            if val is None or str(val) == 'nan':
                continue
            
            rsi_val = float(val)
            
            # تحديد المدة
            if rsi_val < 20 or rsi_val > 80: dur = 5
            elif rsi_val < 25 or rsi_val > 75: dur = 4
            elif rsi_val < 27 or rsi_val > 73: dur = 3
            elif rsi_val < 29 or rsi_val > 71: dur = 2
            else: dur = 1
            
            t = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
            
            if rsi_val < 30:
                send_telegram_msg(f"🚀 صفقة (CALL)\nالزوج: {symbol}\nالتوقيت: {t}\nالمدة: {dur} دقيقة\nRSI: {rsi_val:.2f}")
                time.sleep(3)
            elif rsi_val > 70:
                send_telegram_msg(f"🔥 صفقة (PUT)\nالزوج: {symbol}\nالتوقيت: {t}\nالمدة: {dur} دقيقة\nRSI: {rsi_val:.2f}")
                time.sleep(3)
        
        except Exception:
            continue
            
    time.sleep(60)
