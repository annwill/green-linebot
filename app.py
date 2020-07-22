import requests
import json
from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage


def getGreen(dict):
  green_msg=""
  url='https://api.kcg.gov.tw/api/service/Get/0d3d435c-368e-44dd-87c3-fcfabedc7494'
  r=requests.get(url)
  r.encoding='utf-8'
  js=json.loads(r.text)
  green=js['data']

  for item in green:
    place=item['地址']
    sp=place[3:5]
    if(sp=='成功'):
      sp='前金'
    if(sp==dict.strip()):
      green_msg+=item['餐廳名稱']+'\n'+item['地址']+'\n'+item['電話']+'\n'
  if green_msg=='':
    green_msg=dict+': '+'無餐廳資料\n或輸入錯誤' 

  return green_msg

app=Flask(__name__)
#聊天機器人的基本資料
line_bot_api=LineBotApi('fLFlwaB0WUvRl/Mb5aOmcfu557Ek6LLzHGlCNXEko/hrfAqyVHkV7MlGIgu5ZaDdAf+MHFXguiQVb+pY9fSO/VNdoqkHa2Ss2PLrs+2cdixudAJFRe921hQW4nChrzf+Mt87oGH+sGbC0DgfjQQfCgdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('068b5c1269936320f05fa4dad383df1f') 

#接收 LINE 的資訊
@app.route("/callback",methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature=request.headers['X-Line-Signature']
  # get request body as text
  body=request.get_data(as_text=True)
  app.logger.info("Request body:"+body)

  # handle webhook body
  try:
    handler.handle(body,signature)
  except InvalidSignatureError:
    print("Invalid signature. Please check your channel access token/channel secret.")
    abort(400)
  return 'OK'

  # Messaging settings 訊息由 LineBot發送訊息到其他使用者的設定
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=getGreen(text))
    )

if __name__=='__main__':
    app.run()