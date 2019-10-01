from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('9VQ8Qr0WqXSatWwjDT+Pj/ksUDMdo8SzUzDS3Zl8lvh/E/dbxaTZTS0HmYzfGUPtm/6xJgYu5ibiL+/0lAOpBJlXA2xL8V+zPC6ZUsySnAiPPfpVWErBUDGrjhAMvjvKL+bBGfMqvGOQWzsLA1FK31GUYhWQfeY8sLGRXgo3xvw=
')
handler = WebhookHandler('83af864e412a83c546e5bf9330adecdc')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()