import vkapi
import os
import importlib
from command_system import command_list
from vkMessage import vkMessage

def get_answer(body, peer_id):
    # Сообщение по умолчанию если распознать не удастся
    trigger = ['146208019','бот','плат','боже','brooda', 'бoт', 'omae', 'слыш', 'press', 'момо', 'бандит', 'йоу', 'всем', 'мафиозник']
    message = vkMessage('')
    for j in trigger:
        if j in body.split(' ')[0]:
            for c in command_list:
                message = c.process(body, peer_id)
                if message.isEmpty():
                    #message.show()
                    return message
    return message

def create_answer(data, token):
   load_modules()
   message = get_answer(data['text'].lower().replace(',',''), data['peer_id'])
   message.user_id = data['from_id']
   message.peer_id = data['peer_id']
   #message.show()
   message.send()


def change_level(data, token):
    admin  = data['admin_id']
    user = data['user_id']
    level_old = data['level_old']
    level_new = data['level_new']
    if not str(admin) in ["21766756", "217338357"] and int(level_new > 0):
        vkapi.change_level(user)
        message = vkMessage('Удален пользователь @id%s \nДобавил @id%s' % (user, admin))
        vkapi.send_report(message)
    if str(user) in ["21766756", "217338357"] and int(level_new) == 0:
        if str(user) == "21766756":
            vkapi.reset_level_with_katya(user)
        if str(user) == "217338357":
            vkapi.reset_level_with_plat(user)
        message = vkMessage('Восстановлен @id%s \nУдалил @id%s' % (user, admin))
        vkapi.send_report(message)

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
