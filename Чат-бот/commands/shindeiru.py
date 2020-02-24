import command_system
from vkMessage import vkMessage

def shindeiru(str, peer_id):
    message = vkMessage('')
    print('dewae')
    for i in shindeiru_command.keys:
        if i in str:
            message.message = 'NANI'
            message.attachment = 'photo-146208019_456240880'
            return message
    return message

shindeiru_command = command_system.Command()

shindeiru_command.keys = ['wa mou shindeiru']
shindeiru_command.description = ''
shindeiru_command.process = shindeiru
