import command_system
from vkMessage import vkMessage
import re
import txtHandler

file = 'aud.txt'

def help(body = ''):
    body, keyboard = txtHandler.help(file, payload = 'Где')
    body += '\nДля того, чтобы вызвать эти команды, напиши "Ваня, где *команда*"'
    return body, keyboard

def aud(body, peer_id, from_id):
    if body:
        pattern = re.compile('\d\d\d(/\d)?')
        if pattern.match(body):
            return vkMessage('К сожалению, я пока что могу возвращать только определенные аудитории.\n\
            Подробнее: "Ваня, где"')
        message = txtHandler.prepeareTheAnswer(body, file)
    else:
        message, keyboard = help()
        return vkMessage(message = message, keyboard = keyboard)
    return message

aud_command = command_system.Command()

aud_command.keys = r'где\s?'
aud_command.description = 'Где - показываю информацию о том, где находится тот или иной кабинет'
aud_command.deephelp = help
aud_command.process = aud
