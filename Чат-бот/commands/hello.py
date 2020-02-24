import command_system
from vkMessage import vkMessage

def hello(str, peer_id):
    message = vkMessage('')
    print('hello')
    for i in hello_command.keys:
        if i in str:
            message.message = 'Привет, друг!\nЯ новый чат-бот.'
            return message
    return message

hello_command = command_system.Command()

hello_command.keys = ['привет', 'hello', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = ''
hello_command.process = hello
