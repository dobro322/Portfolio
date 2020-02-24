import command_system
from vkMessage import vkMessage
import re
import txtHandler

file = 'hostels.txt'

def help(body = ''):
    body, keyboard = txtHandler.help(file, payload = 'Общага')
    body += '\nДля того, чтобы вызвать эти команды, напиши "Ваня, общага *команда*"'
    return body, keyboard

def hostels(body, peer_id, from_id):
    if body:
        message = txtHandler.prepeareTheAnswer(body, file)
    else:
        message, keyboard = help()
        return vkMessage(message = message, keyboard = keyboard)
    return message

hostels_command = command_system.Command()

hostels_command.keys = r'(общежити[ея]|общаг[аи])\s?'
hostels_command.description = 'Общежития - показываю информацию об общежитиях СПбГУТ'
hostels_command.deephelp = help
hostels_command.process = hostels
