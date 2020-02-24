import command_system
from vkMessage import vkMessage

def info(str, peer_id):
    message = vkMessage('')
    print('info')
    for i in info_command.keys:
        if i in str:
            message.message = "Помощь:\n\n"
            for c in command_system.command_list:
                #attachment = 'photo-146208019_456240870
                if c.description:
                    message.message += c.description + '\n'
    return message

info_command = command_system.Command()

info_command.keys = ['помощь', 'помоги', 'help']
info_command.description = '&#127891;Помощь - Покажу список команд'
info_command.process = info
