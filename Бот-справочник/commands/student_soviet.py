import command_system
from vkMessage import vkMessage
import re
import txtHandler

file = 'student_soviet.txt'

def help(body = ''):
    body, keyboard = txtHandler.help(file, payload = 'СС')
    body += '\nДля того, чтобы вызвать эти команды, напиши "Ваня, сс *команда*"'
    return body, keyboard

def student_soviet(body, peer_id, from_id):
    if body:
        message = txtHandler.prepeareTheAnswer(body, file)
    else:
        message, keyboard = help()
        return vkMessage(message = message, keyboard = keyboard)
    return message

student_soviet_command = command_system.Command()

student_soviet_command.keys = r'((студенческий совет)|(с{2})|(студ(\s?|-?)совет))\s?'
student_soviet_command.description = 'СС - Показываю информацию про Студенческий совет СПбГУТ'
student_soviet_command.deephelp = help
student_soviet_command.process = student_soviet
