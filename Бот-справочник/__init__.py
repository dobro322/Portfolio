from flask import Flask, request, json
from settings import *
import messageHandler
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        messageHandler.create_answer(data['object'])
        try:
            requests.post('https://ocheredsut.ru/api/1/conversations/messages', json=data['object'])
        except Exception as e:
            print('Failed')
        return 'ok'


if __name__ == "__main__":
    data = {
      "date": 1564334951,
      "from_id": 21766756,
      "id": 0,
      "out": 0,
      "peer_id": 2000000100,
      "text": "",
      "conversation_message_id": 13,
      "fwd_messages": [],
      "random_id": 0,
      "attachments": [],
    }
    result = requests.post('http://127.0.0.1:5000/api/1/conversations/messages', json=data)
    print(result.text)
