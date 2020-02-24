import command_system
import random
from vkMessage import vkMessage

def percents(char, peer_id):
    message = vkMessage('')
    print('percents')
    for i in percents_command.keys:
        if i in char:
            message.message = "Я считаю, что инфа - " + str(random.randint(0,100)) + "%"
    return message

percents_command = command_system.Command()

percents_command.keys = ['инфа']
percents_command.description = '&#128065;&#8205; Инфа *сообщение* - выдаю инфу в процентах'
percents_command.process = percents
