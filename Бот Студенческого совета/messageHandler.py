#coding: utf-8

import vkapi
import os
import importlib
import re
from command_system import command_list
from vkMessage import vkMessage
import DataBase as DB
import main_menu as MM
from Events import events_main
from keyboard import KeyBoard

def say_hello(body):
    if re.match('(начать)|(start)', body, flags = re.I):
        return MM.start_menu()
    else:
        return vkMessage('')

def get_answer(body):
        message = vkMessage('')
        try:
            code = str(DB.get_current_state(body['from_id']))
        except Exception as e:
            message = say_hello(body['text'])
            if message.message:
                return message
            code = '0'
            query = """INSERT INTO Persons(VK, Status) VALUES(%s,%s)"""
            args = (body['from_id'], 0)
            DB.insert_data(query, args)
            events = DB.get_events()
            for event in events:
                if body['text'].lower() in event[2].lower():
                    DB.set_after_reg(body['from_id'], event[0])
                    body['text'] = 'Регистрация'
        if code == '0':
            message = say_hello(body['text'])
            if message.message:
                return message


        if "Events" in code:
            return events_main(body['text'], body['from_id'], code, body['attachments'])

        if code == '9' and body['text'] == 'Мероприятия':
            return events_main(body['text'], body['from_id'], code, body['attachments'])
        for module in command_list:
            if code in module.keys:
                message = module.process(body['text'], body['from_id'], code)
                if message.not_empty():
                    break
        if code == '9' and message.message == "":
            message = MM.main_menu()
        return message


def create_answer(data):
   load_modules()
   try:
       message = get_answer({
           'text': data['text'],
           'from_id': data['from_id'],
           'attachments': data['attachments']
           })
   except Exception as e:
       print(e, "ошибка ввода")
       message = vkMessage('Ошибка ввода')
   message.user_id, message.peer_id = data['from_id'], data['peer_id']
   #message.show()
   message.send()



def open_files():
    try:
        files = os.listdir(os.getcwd() + '/VKBot/commands/')
        return files
    except Exception as e:
        files = os.listdir(os.getcwd() + '\commands\\')
        return files
    return 0

def load_modules():
   files = open_files()
   if files:
       modules = sorted(filter(lambda x: x.endswith('.py'), files))
       for m in modules:
           importlib.import_module("commands." + m[0:-3])
       return 1
   return 0



def send_to_first_course():
    first_course = DB.select_all()
    for k, person in enumerate(first_course):
        message = vkMessage("*Объявление*\n\
        В нашей системе открылась регистрация акцию <<Пригласи друга>>\n\
        Также открыта регистрация в приемную комиссию СПбГУТ")
        message.peer_id = message.user_id = person
        message.group = 147403573
        answer = message.send()
        if not answer == -1:
            print(k, " Успешно отправлно %s" % person)
        else:
            print(k, " Ошибка для %s" % person)


#send_to_first_course()
