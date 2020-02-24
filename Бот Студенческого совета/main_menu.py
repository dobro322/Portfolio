from keyboard import KeyBoard
from vkMessage import vkMessage
import DataBase as DB

def main_menu_keyboard():
    KB = KeyBoard('true', 1)
    KB.add_button('Мероприятия','green','{}')
    for n in ['Жалоба','Обратная связь','Коллективная жалоба']:
        KB.add_button(n,'white','{}')
    return KB.get_button()

def main_menu(greeting_text = 'Возможности главного меню:\n• Мероприятия\n• Жалоба\n• Обратная связь\n• Коллективная жалоба'):
    message = vkMessage(greeting_text)
    message.keyboard = main_menu_keyboard()
    return message

def start_keyboard(additional):
    KB=KeyBoard('false',1)
    for n in ['Регистрация']:
        KB.add_button(n,'green','{}')
    for n in additional:
        KB.add_button(n[2],'green','{}')
    return KB.get_button()

def start_menu(greeting_text = "Добро пожаловать в АСУ Студенческого совета!\nВыберите действие:\n"):
    greeting_text += "• Регистрация"
    events = DB.get_events()
    for event in events:
        greeting_text += "\n• %s" %(event[2])
    message = vkMessage(greeting_text)
    message.keyboard = start_keyboard(events)
    return message
