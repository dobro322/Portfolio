import command_system
from vkMessage import vkMessage
import vkapi

def who(str, peer_id):
    # message = vkMessage('')
    # print('dewae')
    # for i in who_command.keys:
    #     if i in str:
    #         message.message = str
    #         vkapi.send_report(message)
    #         message.message = 'Ваше сообщение отправлено!'
    #         return message
    # return message
    return ''

who_command = command_system.Command()

who_command.keys = ['репорт']
who_command.description = '' #'&#128232; Репорт *сообщение* - отправит репорт/пожелание админу бота'
who_command.process = who
