import command_system
from vkMessage import vkMessage
import re
import txtHandler

file = 'zelast.txt'

def help(body = ''):
    body, keyboard = txtHandler.help(file)
    body += '\nДля того, чтобы вызвать эти команды, напиши "Ваня, *команда*"'
    return body, keyboard

def zelast(body, peer_id, from_id):
    message = vkMessage('')
    if body == 'частозадаваемые':
        print('yes')
        message, keyboard = help()
        return vkMessage(message)
    elif len(body) > 3:
        message = txtHandler.prepeareTheAnswer(body, file)
    return message

zelast_command = command_system.Command()

zelast_command.keys = r'.+'
zelast_command.description = 'Частозадаваемые - отвечаю на многие другие вопросы'
zelast_command.deephelp = help
zelast_command.process = zelast
