import command_system
import vkapi
from vkMessage import vkMessage

def cat(str, peer_id):
    message = vkMessage('')
    print('cat')
    str = str.split(' ', 1)
    for i in cat_command.keys:
        if i in str[1]:
            message.message = 'Рандомный пост с Бонч.Мемов:\n'
            message.attachment = vkapi.get_random_wall_picture(-146208019)
    return message

cat_command = command_system.Command()

cat_command.keys = ['дай мем']
cat_command.description = '&#128169; Дай мем - Пришлю радномный мем с Bonch.Memes'
cat_command.process = cat
