#coding: utf-8

import vkapi
import os
import importlib
import re
from command_system import command_list
from vkMessage import vkMessage
import json

def get_answer(body, peer_id, from_id, payload):
    # Сообщение по умолчанию если распознать не удастся
    message = vkMessage('')
    trigger = re.compile('((ваня)|(информ)|(петрович)|(ivan)|(\[club128637216\|1NFORM\])|(\[club128637216\|[@*]1nformproject\]))[ ,]', re.I)
    if trigger.match(body) or peer_id < 2000000000:
        body = trigger.sub('',body, 1)
        if payload and body != 'начать':
            body = payload + ' ' + body
        for i, c in enumerate(command_list):
            if re.match(c.keys, body):
                if i < len(command_list) - 1:
                    body = re.sub(c.keys,'',body, 1)
                message = c.process(body, peer_id, from_id)
                break

        if not message.isEmpty():
            message.message = 'Не понял команду.\nПопробуйте "Ваня, помощь"'

    return message

def create_answer(data):
   load_modules()
   try:
       data['payload'] = json.loads(data['payload'].lower())['text']
   except:
       data['payload'] = ""


   message = get_answer(data['text'].lower().replace(',',''),
                        data['peer_id'],
                        data['from_id'],
                        data['payload'])

   message.user_id, message.peer_id = data['from_id'], data['peer_id']
   message.send()


def load_modules():
   try:
       files = os.listdir(os.getcwd() + "\commands\\")
   except Exception as e:
       print ("Loading test lib")
       files = os.listdir(os.getcwd() + '/VKBot/commands/')
   finally:
       modules = sorted(filter(lambda x: x.endswith('.py'), files))
       print(modules)
       for m in modules:
           importlib.import_module("commands." + m[0:-3])

def test():
    meme = {
    "from_id": 21766756,
    "peer_id": 21766756,
    "text": "[club128637216|@1nformproject] помощь"
    }
    create_answer(meme)

#test()


def massflood(peer_id=2000000001):
    message = vkMessage('-Мстители: Война без конечности: мы сделали лучший кроссовер всех времен\nБонч:')
    message.peer_id = peer_id
    message.attachment = 'wall-146208019_7818'
    try:
        message.send()
        print('Succes')
    except Exception as e:
        print('Failed')


# for n in range(6, 16):
#     print('Try: ' + str(2000000000 + n))
#     massflood(2000000000 + n)
