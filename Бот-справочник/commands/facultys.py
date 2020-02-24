import command_system
from vkMessage import vkMessage
import re
import txtHandler

file = 'facultys.txt'

def help(body = ''):
    body, keyboard = txtHandler.help(file, payload = 'Факультет')
    body += '\nДля того, чтобы вызвать эти команды, напиши "Ваня, факультет *команда*"'
    return body, keyboard

def facultys(body, peer_id, from_id):
    if body:
        message = txtHandler.prepeareTheAnswer(body, file)
    else:
        message, keyboard = help()
        return vkMessage(message = message, keyboard = keyboard)
    return message

facultys_command = command_system.Command()

facultys_command.keys = r'(факультеты?|институты?|колледжи?)\s?'
facultys_command.description = 'Факультеты - показываю информацию о факультетах/институтах СПбГУТ'
facultys_command.deephelp = help
facultys_command.process = facultys
