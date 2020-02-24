import vk
import random
from settings import *
from vkMessage import vkMessage
session = vk.Session()
api = vk.API(session, v=5.80)


def trySend(fn):
    try:
        def catch_arg(body):
            fn(body)
    except Exception as e:
        print(e)
    return fn


@trySend
def send_chat(body):
    if body.keyboard:
        api.messages.send(access_token=token, user_id=body.user_id, message=body.message, attachment=body.attachment, lat = body.coord['lat'], long = body.coord['long'], keyboard = body.keyboard)
    else:
            api.messages.send(access_token=token, user_id=body.user_id, message=body.message, attachment=body.attachment, lat = body.coord['lat'], long = body.coord['long'])


@trySend
def send_dialog(body):
    api.messages.send(access_token=token, chat_id=body.peer_id - 2000000000, message=body.message, attachment=body.attachment, lat = body.coord['lat'], long = body.coord['long'], keyboard = '{"buttons":[],"one_time":true}')



@trySend
def send_report(body):
    api.messages.send(access_token=token, user_id = 21766756, message=body.message, attachment=body.attachment)


@trySend
def getMessagesUploadServer(body):
    answer = api.docs.getMessagesUploadServer(access_token = token, peer_id = body)
    return answer


@trySend
def doc_save(body, photo, server, hash):
    answer = api.photos.saveMessagesPhoto(access_token = token, photo = photo, server = server, hash = hash)
    return answer
