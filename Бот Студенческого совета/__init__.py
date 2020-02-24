from flask import Flask, request, json
from settings import *
import vk
import messageHandler

app = Flask(__name__)

session = vk.Session()
api = vk.API(session, v=5.80)

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        messageHandler.create_answer(data['object'])
        return 'ok'

def test():
    meme = {'from_id': 163563035, 'peer_id': 163563035, 'text':'20.06-01.07', 'attachments': []}
    messageHandler.create_answer(meme)

#test()
