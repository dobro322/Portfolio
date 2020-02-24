import command_system
from vkMessage import vkMessage
import re
import txtHandler

file = 'guides.txt'

def help(body = ''):
    body, keyboard = txtHandler.help(file, payload = 'Гайд')
    body += '\nДля того, чтобы вызвать эти команды, напиши "Ваня, гайд *команда*"'
    return body, keyboard

def guides(body, peer_id, from_id):
    if body:
        message = txtHandler.prepeareTheAnswer(body, file)
    else:
        message, keyboard = help()
        return vkMessage(message = message, keyboard = keyboard)
    return message

guides_command = command_system.Command()

guides_command.keys = r'гайд\s?'
guides_command.description = 'Гайд - показываю различные гайды по СПбГУТ'
guides_command.deephelp = help
guides_command.process = guides
