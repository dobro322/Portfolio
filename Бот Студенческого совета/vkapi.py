import vk
import random
from settings import *
session = vk.Session()
api = vk.API(session, v=5.80)


def try_send(send):
    def catch_arg(message):
        try:
            send(message)
        except Exception as e:
            print('Can\'t send message to VK: ' + str(e))
            return -1
    return catch_arg


@try_send
def send_private(message):
    if message.keyboard:
        return api.messages.send(access_token=token, user_id=message.user_id, message=message.message, attachment=message.attachment, lat = message.coord['lat'], long = message.coord['long'], keyboard = message.keyboard)
    else:
        return api.messages.send(access_token=token, user_id=message.user_id, message=message.message, attachment=message.attachment, lat = message.coord['lat'], long = message.coord['long'])


@try_send
def send_conversation(message):
    return api.messages.send(access_token=token, chat_id=message.peer_id - 2000000000, message=message.message, attachment=message.attachment, lat = message.coord['lat'], long = message.coord['long'], keyboard = '{"buttons":[],"one_time":true}')


def get_bdate(id):
    message = api.users.get(access_token=token, user_ids = id, fields = 'bdate')
    try:
        bdate = message[0]['bdate']
        return bdate
    except Exception as e:
        return e

def get_insta(id):
    message = api.users.get(access_token=token, user_ids = id, fields = 'connections')
    if 'instagram' in message[0]:
        return message[0]['instagram']
    else:
        return None

@try_send
def send_report(message):
    return api.messages.send(access_token=token, user_id = 21766756, message=message.message, attachment=message.attachment)



def get_messages_upload_server(message):
    return api.docs.getMessagesUploadServer(access_token = token, peer_id = message)

def get_doc_upload_server(message):
    return api.photos.getMessagesUploadServer(access_token = token, peer_id = message)

def save(file, title):
    return api.docs.save(access_token = token, file = file, title = title)

def doc_save(server, photo, hash):
    return api.photos.saveMessagesPhoto(access_token = token, photo = photo, server = server, hash = hash)
