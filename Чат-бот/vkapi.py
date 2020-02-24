import vk
import random
from settings import *
session = vk.Session()
api = vk.API(session, v=5.95)


def send_chat(body):
    try:
        api.messages.send(access_token=token, user_id=body.user_id, message=body.message, attachment=body.attachment, lat = body.coord['lat'], long = body.coord['long'])
    except Exception as e:
        print(e)


def send_dialog(body):
    try:
        api.messages.send(access_token=token, chat_id=body.peer_id - 2000000000, message=body.message, attachment=body.attachment, lat = body.coord['lat'], long = body.coord['long'])
    except Exception as e:
        print(e)


def delete_mess(peer_id, msg_id):
    # return api.messages.getByConversationMessageId(access_token = token, peer_id = peer_id, conversation_message_ids = msg_id)
    return api.messages.delete(access_token=token, message_ids=msg_id, delete_for_all=False)


def send_report(body):
    try:
        api.messages.send(access_token=token, user_id = 21766756, message=body.message, attachment=body.attachment)
    except Exception as e:
        print(e)


def change_level(user_id):
    api.groups.editManager(access_token=implict_token, group_id = 146208019, user_id = user_id)

def reset_level_with_katya(user_id):
    api.groups.editManager(access_token=katya_token, group_id = 146208019, user_id = user_id, role = "administrator")

def reset_level_with_plat(user_id):
    api.groups.editManager(access_token=implict_token, group_id = 146208019, user_id = user_id, role = "administrator")

def get_random_wall_picture(group_id):
    # max_num = api.photos.get(access_token=serv_token, owner_id=group_id, album_id='wall', count=0)['count']
    # num = random.randint(1, max_num)
    # photo = api.photos.get(access_token=serv_token, owner_id=str(group_id), album_id='wall', count=1, offset=num)
    # attachment = 'photo' + str(group_id) + '_' + str(photo['items'][0]['id'])
    # try:
    #     message = api.wall.getById(access_token=serv_token, posts=(str(group_id) + '_' + str( photo['items'][0]['post_id'] ))) [0]['text']
    # except:
    #     print('index error\n')

    max_num = api.wall.get(access_token = serv_token, owner_id = group_id)['count']
    num = random.randint(1, max_num)
    post = api.wall.get(access_token = serv_token, owner_id = str(group_id), offset = num, count = 1)['items'][0]['id']
    attachment = 'wall' + str(group_id) + '_' + str(post)
    return attachment


def get_random_conf_user(conf_id):
    try:
        t = api.messages.getConversationMembers(access_token = token, peer_id = conf_id)['profiles']
        max_num = len(t)
        num = random.randint(0, max_num - 1)
        id = "Я думаю, что @id" + str(t[num]['id']) + "(" + str(t[num]['first_name']) +  ")"
        return id
    except Exception as e:
        print (e)

#get_random_conf_user(2000000002)

def kick():
    api.messages.removeChatUser(access_token = token, chat_id = 39, user_id = 79491745)

#kick()
