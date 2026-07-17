import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime, timedelta

# --- بيانات البوت ---
BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=15)
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

symbols = ["EURUSD=X", "GBPUSD=X"]

print("البوت يعمل الآن بنظام الحماية الكاملة...")

while True:
    for symbol in symbols:
        try:
            # 1. جلب البيانات مع فترة كافية
            data = yf.download(symbol, period="5d", interval="1m", progress=False)
            
            # 2. حماية من البيانات الفارغة
            if data is None or data.empty or len(data) < 20:
                continue
            
            # 3. حساب RSI بشكل آمن
            rsi_series = ta.rsi(data['Close'], length=14)
            
            if rsi_series is None or rsi_series.empty:
                continue
                
            current_rsi = rsi_series.iloc[-1]
            
            # 4. حماية من قيم الـ nan أو None
            if current_rsi is None or str(current_rsi) == 'nan':
                continue
            
            # تحويل آمن للرقم
            current_rsi = float(current_rsi)
            
            # 5. تحديد المدة (1-5 دقائق)
            if current_rsi < 20 or current_rsi > 80:
                duration = 5
            elif current_rsi < 25 or current_rsi > 75:
                duration = 4
            elif current_rsi < 27 or current_rsi > 73:
                duration = 3
            elif current_rsi < 29 or current_rsi > 71:
                duration = 2
            else:
                duration = 1
            
            next_minute = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
            
            # 6. إرسال الإشارات
            if current_rsi < 30:
                msg = (f"🚀 صفقة قوية (CALL)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                send_telegram_msg(msg)
                time.sleep(2)
            
            elif current_rsi > 70:
                msg = (f"🔥 صفقة قوية (PUT)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                send_telegram_msg(msg)
                time.sleep(2)

        except Exception as e:
            # نكتب الخطأ في اللوج لنعرف السبب دون توقف البوت
            print(f"حدث خطأ مؤقت في {symbol}: {e}")
            
    time.sleep(60)
