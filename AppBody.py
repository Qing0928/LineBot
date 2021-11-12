from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from flask import Flask, request, abort
import requests
import os

app = Flask(__name__)
line_bot_api = LineBotApi('/xc+mRNnP4icof0RTWKH+SrCHu9Sw7G7quRLjLyIP0plaHELgO+Igr5wsDMkQXCtzMQCUK0JBCrcNiSfAFrfBl4G5C4lwMCmMmswiM9Y8R3cXMkiNZDQmmh3TgI6pmK/zf7Dz4iTtvds22VMenIYgAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a5fdce271d8905f7606b78abb74de110')

@app.post('/callback')
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '今天天氣如何':
        weather_reply = '天氣概況:{}\n現在溫度:{}\n最高溫:{}\n最低溫:{}\n濕度:{}\n'
        weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'
        lat = '23.696862531078384'
        lon = '120.53401536679688'
        key = 'YOUR API KEY'
        try:
            response = requests.get(weather_url.format(lat, lon, key))
            weather_json = response.json()
            weather_des = weather_json['weather'][0]['description']
            temp_now = round((int(weather_json['main']['temp']) - 273.15), 2)
            temp_max = round((int(weather_json['main']['temp_max']) - 273.15), 2)
            temp_min = round((int(weather_json['main']['temp_min']) - 273.15), 2)
            hum = weather_json['main']['humidity']
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text=weather_reply.format(weather_des, temp_now, temp_max, temp_min, hum))
            )
        except Exception as e:
            print(e)
    elif event.message.text == 'hello':
        try:
            reply = 'Hi'
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text=reply)
            )
        except Exception as e:
            print(e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
