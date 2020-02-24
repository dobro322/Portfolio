import command_system
from vkMessage import vkMessage

def boyan(body, peer_id):
    message = vkMessage('')
    print('boyan')
    for i in boyan_command.keys:
        if i in body:
            body = body.split(' ')
            if body[2]:
                message.message = str(body[2]).capitalize() + ' получает бояном по голове'
                return message
            else:
                message.message = 'Кто боян? Кто боян-то? Ты здесь один'
    return message

boyan_command = command_system.Command()

boyan_command.keys = ['боян']
boyan_command.description = '&#128118; Боян *Имя* - отбояню человека'
boyan_command.process = boyan
