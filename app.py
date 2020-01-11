import os, sys, requests
from flask import Flask, request
from pymessenger import Bot



PAGE_ACCESS_TOKEN = $PAGE_TOKEN
VerifyToken = $VERIFY_TOKEN

app = Flask(__name__)
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # Webhook verifcation
    if request.args.get('hub.mode') == "subscribe" and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == VerifyToken:
            return "Verifcation token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                sender_name = requests.get('https://graph.facebook.com/' + str(sender_id) + '?fields=first_name&access_token='+PAGE_ACCESS_TOKEN).json()['first_name']
                recipient_id = messaging_event['recipient']['id']


                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        sender_message = messaging_event['message']['text']
                    else:
                        sender_message = 'Undefine'

                    print(sender_name+":", sender_message)
                    if (sender_message.lower() == 'hi') or (sender_message.lower() == 'hello'):

                        bot.send_text_message(sender_id, 'Hello '+sender_name)


    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True, port=80)
