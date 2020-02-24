import command_system
from vkMessage import vkMessage
import random

def ili(body, peer_id):
    message = vkMessage('')
    print('dewae')
    for i in ili_command.keys:
        if i in body:
            variables = ['Я думаю, что лучше ', 'Мне кажется, это ', 'Очевидно, ', 'Птичка начирикала, что ', 'Однозначно ']
            answers = ['первое', 'второе']
            message.message = variables[random.randint(0,len(variables) - 1)] + answers[random.randint(0,1)]
            return message
    return message

ili_command = command_system.Command()

ili_command.keys = ['или']
ili_command.description = '&#8265; *1 вариант* или *2 вариант*? - помогу с выбором'
ili_command.process = ili
