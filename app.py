import os
import sys
import json
import re

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello Waqas", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if message_text=="1":
                        send_message(sender_id,"Enter your Order ID:")
                    elif message_text=="2":
                        send_message(sender_id,"Enter the Order ID you want to check:")
                    
                    elif getorderid(message_text):
                        
                        send_message(sender_id,"You Entered:")
                        send_message(sender_id,getorderid(message_text))
                    else:    
                        send_message(sender_id, "Hello, Welcome to PlanB Facebook Page!!!, Here is What I Can Do For You: \n Reply with 1 if you have your amazon order ID and want to send recharge to a Digicel number. \n Reply with 2 to check your order ID,\n")
                    
                
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

def getorderid(txtmsg):
    re1 = '(\\d)'
    re2 = '(\\d)'
    re3 = '(\\d)'
    re4 = '(-)'
    re5 = '(\\d)'
    re6 = '(\\d)'
    re7 = '(\\d)'
    re8 = '(\\d)'
    re9 = '(\\d)'
    re10 = '(\\d)'
    re11 = '(\\d)'
    re12 = '(-)'
    re13 = '(\\d)'
    re14 = '(\\d)'
    re15 = '(\\d)'
    re16 = '(\\d)'
    re17 = '(\\d)'
    re18 = '(\\d)'
    re19 = '(\\d)'

    rg = re.compile(
        re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12 + re13 + re14 + re15 + re16 + re17 + re18 + re19,
        re.IGNORECASE | re.DOTALL)
    m = rg.search(txtmsg)
    if m:
        d1 = m.group(1)
        d2 = m.group(2)
        d3 = m.group(3)
        c1 = m.group(4)
        d4 = m.group(5)
        d5 = m.group(6)
        d6 = m.group(7)
        d7 = m.group(8)
        d8 = m.group(9)
        d9 = m.group(10)
        d10 = m.group(11)
        c2 = m.group(12)
        d11 = m.group(13)
        d12 = m.group(14)
        d13 = m.group(15)
        d14 = m.group(16)
        d15 = m.group(17)
        d16 = m.group(18)
        d17 = m.group(19)

        order_number = d1 + d2 + d3 + c1 + d4 + d5 + d6 + d7 + d8 + d9 + d10 + c2 + d11 + d12 + d13 + d14 + d15 + d16 + d17
        if order_number:
            return order_number
        else:
            return 0    
    

if __name__ == '__main__':
    app.run(debug=True)
