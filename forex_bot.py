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
        requests.get(url, timeout=10)
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

symbols = ["EURUSD=X", "GBPUSD=X"]

print("البوت يعمل الآن ويحلل المدة الزمنية (1-5 دقائق) تلقائياً...")

while True:
    for symbol in symbols:
        try:
            data = yf.download(symbol, period="1d", interval="1m", progress=False)
            
            if not data.empty:
                # حساب المؤشرات
                rsi_values = ta.rsi(data['Close'], length=14)
                
                # تأكد أن هناك قيم للـ RSI
                if rsi_values is not None and not rsi_values.empty:
                    current_rsi = rsi_values.iloc[-1]
                    
                    # التحقق من أن القيمة ليست فارغة قبل التحويل
                    if current_rsi is not None:
                        current_rsi = float(current_rsi)
                        
                        data['SMA'] = ta.sma(data['Close'], length=10)
                        close_price = data['Close'].iloc[-1]
                        sma_price = data['SMA'].iloc[-1]
                        
                        # --- تحديد المدة تلقائياً ---
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
                        
                        # التحقق من الإشارة
                        if current_rsi < 30:
                            msg = (f"🚀 صفقة قوية (CALL)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة الموصى بها: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                            send_telegram_msg(msg)
                        elif current_rsi > 70:
                            msg = (f"🔥 صفقة قوية (PUT)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة الموصى بها: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                            send_telegram_msg(msg)
        
        except Exception as e:
            print(f"خطأ في فحص {symbol}: {e}")
            
    time.sleep(60)
