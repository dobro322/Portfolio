import command_system
import vkapi
import requests
from vkMessage import vkMessage
import DataBase as DB
from keyboard import KeyBoard
import main_menu as MM

make_offer_command = command_system.Command()

def cancel_keyboard():
    KB = KeyBoard('false', 1)
    KB.add_button('Отмена','red','{}')
    return KB.get_button()

def get_chairman_id(faculty_id):
    query = """
    SELECT Faculty_chairman_id
    FROM Faculties
    WHERE Faculty_id = %s
    """
    args = (faculty_id,)
    return DB.get_data(query,args)[0]

def make_offer(offer, peer_id, code):
    chairman = get_chairman_id(DB.get_faculty(peer_id))
    destinations = ['21766756','285623077']
    if chairman and not chairman in '-':
        destinations.append(str(chairman))
    def send(destination_id):
        message = vkMessage(("Предложение от @id%s\n" % (peer_id)) + str(offer))
        message.peer_id = message.user_id = destination_id
        message.send()
    for id in destinations:
        send(id)
    DB.set_state(peer_id, 9)
    return MM.main_menu('Ваше сообщение было успешно отправлен Студенческому совету!\nОжидайте ответа от вашего председателя!')

make_offer_command.keys = [
    '9', #Главное меню
    '10' #Оставить предложение
]

state_list = {
    '10' : make_offer
}

def make_offer(body, peer_id, code):
    message = vkMessage('')
    if code == '9' and body.lower() == 'обратная связь':
        message.message = DB.get_state_help(10)
        message.keyboard = cancel_keyboard()
        DB.set_state(peer_id, 10)
    elif code in ['10']:
        if body.lower() == 'отмена':
            message = MM.main_menu()
            DB.set_state(peer_id, 9)
        else:
            message = state_list[code](body, peer_id, code)
    return message

make_offer_command.description = ''
make_offer_command.process = make_offer
