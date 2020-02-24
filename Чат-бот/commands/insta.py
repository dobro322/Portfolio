import command_system
from vkMessage import vkMessage

def insta(str, peer_id):
    message = vkMessage('')
    print('dewae')
    for i in insta_command.keys:
        if i in str:
            if 'разраба' in str:
                message.message = 'instagram.com/dobro322'
            if 'флексера' in str:
                message.message = 'instagram.com/java_lrd'
            return message
    return message

insta_command = command_system.Command()

insta_command.keys = ['инста']
insta_command.description = ''
insta_command.process = insta
