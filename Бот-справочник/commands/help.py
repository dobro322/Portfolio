import command_system
import re
from keyboard import KeyBoard
from vkMessage import vkMessage

def help(body, peer_id, from_id):
    message = vkMessage('')
    KB = KeyBoard()
    if body:
        for i in command_system.command_list:
            if re.match(i.keys,body):
                message.message, message.keyboard = i.deephelp()
    else:
        message.message = 'Привет, студент!\n\
        Я Ваня Формин, бот-справочник СПбГУТ, который поможет тебе ответить на многие вопросы.\n\n\
        Для того, чтобы я реагировал на твои команды, тебе потребуется обратиться ко мне как "Информ" или "Ваня".\n\n\
        Вот список моих команд:\n'
        for i in command_system.command_list:
            if i.description:
                message.message += ' • ' + i.description + '\n'
                label = re.match('.*?\s',i.description).group(0)
                KB.addButton(label,'white','{}')
        message.message +'\nТакже отвечаю на частозадаваемые вопросы (Ваня, помощь частозадаваемые)\n'
        message.message += '\nЧтобы вызвать подсказку по одной из этих команд, напиши "Ваня, помощь *команда*" или просто "Ваня, *команда*"'
    message.message += '\n\nУвидел ошибку, есть предложение, хочешь сказать спасибо разрабу?\nИспользуй команду "Ваня, репорт *текст сообщения*"'
    message.keyboard = KB.getButton()
    return message

help_command = command_system.Command()

help_command.keys = r'(помощь|help|помоги|спаси|начать|выручай|меню)\s?'
help_command.description = ''
help_command.deephelp = 'Помогаю освоиться в боте'
help_command.process = help
