import command_system
import vkapi
import requests
from vkMessage import vkMessage
import DataBase as DB
from keyboard import KeyBoard
import main_menu as MM
import os

make_offer_command = command_system.Command()


def get_request(url):
    try:
        with open(os.getcwd() + '\Docs\\Collective.docx', 'rb') as f:
            return requests.post(url['upload_url'], files={'file': f})
    except:
        with open(os.getcwd() + '/VKBot/Docs/Collective.docx', 'rb') as f:
            return requests.post(url['upload_url'], files={'file': f})

def set_message(answer, peer_id):
    message = vkMessage('')
    message.attachment = 'doc' + str(answer[0]['owner_id']) + '_' + str(answer[0]['id'])
    message.message =  'Держите шаблон коллективной жалобы. \n\
                        Теперь вам необходимо самостоятельно заполнить и распечатать документ, после чего собрать подписи. \n\
                        Для сбора подписей прилагается таблица на втором листе'
    message.user_id = message.peer_id = int(peer_id)
    return message

def get_answer(req):
    return vkapi.save(req, 'Коллективная жалоба.docx')

def make_offer(body, peer_id, code):
    message = vkMessage('')
    if body.lower() == 'коллективная жалоба':
        url = vkapi.get_messages_upload_server(peer_id)
        request = get_request(url)
        req = request.text.split('":"')[1][0:-2]
        answer = get_answer(req)
        message = set_message(answer, peer_id)
        message.send()
        message = MM.main_menu()
    return message


make_offer_command.keys = [
    '9'
]

make_offer_command.description = ''
make_offer_command.process = make_offer
