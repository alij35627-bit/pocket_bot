import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime, timedelta

BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_telegram_msg(message):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}", timeout=10)
    except:
        pass

symbols = ["EURUSD=X", "GBPUSD=X"]

print("البوت يعمل الآن بنظام الحماية المطلقة...")

while True:
    for symbol in symbols:
        try:
            data = yf.download(symbol, period="5d", interval="1m", progress=False)
            
            # التأكد أن البيانات تحتوي على عمود الإغلاق
            if data is None or 'Close' not in data.columns:
                continue
                
            rsi_series = ta.rsi(data['Close'], length=14)
            
            # التأكد أن المؤشر تم حسابه ولا يحتوي على قيم فارغة
            if rsi_series is None or len(rsi_series) == 0:
                continue
                
            current_rsi = rsi_series.iloc[-1]
            
            if current_rsi is None or str(current_rsi) == 'nan':
                continue
                
            current_rsi = float(current_rsi)
            
            # تحديد المدة
            if current_rsi < 20 or current_rsi > 80: duration = 5
            elif current_rsi < 25 or current_rsi > 75: duration = 4
            elif current_rsi < 27 or current_rsi > 73: duration = 3
            elif current_rsi < 29 or current_rsi > 71: duration = 2
            else: duration = 1
            
            next_minute = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
            
            if current_rsi < 30:
                send_telegram_msg(f"🚀 صفقة قوية (CALL)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                time.sleep(2)
            elif current_rsi > 70:
                send_telegram_msg(f"🔥 صفقة قوية (PUT)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                time.sleep(2)
                
        except Exception:
            continue # تجاهل أي خطأ فني والاستمرار للزوج التالي
            
    time.sleep(60)
