import command_system
from vkMessage import vkMessage

def hellow(str, peer_id):
    message = vkMessage('')
    print('dewae')
    for i in hellow_command.keys:
        if i in str:
            message.message = 'Приветики <3'
            return message
    return message

hellow_command = command_system.Command()

hellow_command.keys = ['привет', 'утро']
hellow_command.description = '&#10067;Кто *сообщение* - выберу случайного человека из чата'
hellow_command.process = hellow
