import command_system
from vkMessage import vkMessage

def vova(str, peer_id):
    message = vkMessage('')
    for i in vova_command.keys:
        if i in str:
            message.message = 'Где дизайн?'
            return message
    return message

vova_command = command_system.Command()

vova_command.keys = ['вова']
vova_command.description = ''
vova_command.process = vova
