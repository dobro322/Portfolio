import command_system
from vkMessage import vkMessage

def pressf(str, peer_id):
    message = vkMessage('')
    print('dewae')
    for i in pressf_command.keys:
        if 'f' in str:
            message.message = 'F'
            return message
        if ')))' in str:
            message.message = ')))'
            return message
    return message

pressf_command = command_system.Command()

pressf_command.keys = ['f',')))']
pressf_command.description = ''
pressf_command.process = pressf
