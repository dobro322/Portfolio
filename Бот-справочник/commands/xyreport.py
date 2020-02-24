import command_system
from vkMessage import vkMessage
import vkapi

def who(body, peer_id, from_id):
    message = vkMessage('')
    print('dewae')
    for i in who_command.keys:
        if i in body and not int(from_id) in [79491745]:
            message.message = 'Репорт от *id' + str(from_id) + '(юзера):\n' + body
            vkapi.send_report(message)
            message.message = 'Ваше сообщение отправлено!'
            return message
    return message

who_command = command_system.Command()

who_command.keys = ['репорт']
who_command.description = ''
who_command.process = who
