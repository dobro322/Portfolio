import command_system
from vkMessage import vkMessage

def who(str, peer_id):
    message = vkMessage('')
    print('dewae')
    for i in who_command.keys:
        if i in str:
            message.message = 'лол'
            return message
    return message

who_command = command_system.Command()

who_command.keys = ['смотри']
who_command.description = '&#10067;Кто *сообщение* - выберу случайного человека из чата'
who_command.process = who
