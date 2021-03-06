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
        messageHandler.create_answer(data['object'], token)
        return 'ok'
    elif data['type'] == 'group_officers_edit':
        messageHandler.change_level(data['object'], token)
        return 'ok'
