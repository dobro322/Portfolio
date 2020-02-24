import command_system
import vkapi
import requests
from vkMessage import vkMessage
import DataBase as DB
from keyboard import KeyBoard
import main_menu as MM
import Events

faculties = [
    'ИКСС',
    'РТС',
    'ИСиТ',
    'ИВО',
    'ГФ',
    'ЦЭУБИ',
    'ФП',
    'ИНО',
    'СПбКТ'
]

hostels = [
    'Другое',
    'Дальневосточное',
    'Рыбацкое',
    'Лесное',
    'Василеостровское',
    'Стойкости',
    'Яковлевское'
]

report_script_command = command_system.Command()

def normalizer(number = '+7 (999) 999-99-99'):
    for a in ['(', ')' , '-', ' ']:
        number = number.replace(a, '')
    numb_arr = ['+7 ','(' , '', '', ') ' , '' , '' , '-' , '' , '-', '']
    for x in range(10, 0, -1):
        number, result = number[:-1], number[-1]
        numb_arr[x] += str(result)
    return ''.join(numb_arr)


def check_fill(id, code):
    code = str(int(code) + 1)
    DB.set_state(id, code)
    message = vkMessage(DB.get_state_help(code))
    message.keyboard = cancel_keyboard()
    message.attachment = "photo-147403573_456239150"
    return message


def update_template(user_column):
    return """
    UPDATE Persons
    SET %s = %s, Status = %s
    WHERE VK = %s
    """ % (user_column,'%s','%s','%s')


def cancel_keyboard():
    KB = KeyBoard('false', 1)
    KB.add_button('Отмена','red','{}')
    return KB.get_button()


def update(query, column_text, peer_id, state_code):
    state_code = str(int(state_code) + 1)
    args = (column_text, state_code, peer_id)
    DB.insert_data(query, args)
    message = vkMessage(DB.get_state_help(state_code))
    message.keyboard = cancel_keyboard()
    return message


def faculty_keyboard():
    KB = KeyBoard('false', 2)
    for n in faculties:
        KB.add_button(n,'white','{}')
    return KB.get_with_person_button('Отмена')


def hostel_keyboard():
    KB = KeyBoard('false', 2)
    for n in hostels[1:]:
        KB.add_button(n,'white','{}')
    return KB.get_with_person_button('Другое')


def update_name(id, name, code):
    query = update_template('FIO')
    message = update(query, name, id, code)
    message.keyboard = faculty_keyboard()
    return message


def update_faculty(id, fac, code):
    faculties_low = [x.lower() for x in faculties]
    query = update_template('Faculty_id')
    message = update(query, faculties_low.index(fac.lower() )+1, id, code)
    return message


def update_group(id, group, code):
    group = group.upper()
    query = update_template('GroupId')
    message = update(query, group, id, code)
    message.keyboard = hostel_keyboard()
    return message


def update_hostel(id, address, code):
    query = update_template('Hostel_Id')
    message = update(query, hostels.index(address), id, code)
    return message


def update_phone(id, phone, code):
    phone = normalizer(phone)
    query = update_template('Phone')
    code = 5
    args = (phone, code, id)
    DB.insert_data(query, args)
    DB.set_state(id, '9')
    person = DB.get_person(id)
    if person[7]:
        try:
            DB.set_state(id, person[7])
            DB.set_after_reg(id, '')
            return Events.events_main("Что это такое?", id, person[7], [])
        except Exception as e:
            raise e
    return MM.main_menu()

report_script_command.keys = [
    '0', #Незарегистрированный
    '1', #Ввод ФИО
    '2', #Ввод факультета
    '3', #Ввод группы
    '4', #Ввод статуса общежития
    '5'  #Ввод мобильного
]

state_list = {
    '1' : update_name,
    '2' : update_faculty,
    '3' : update_group,
    '4' : update_hostel,
    '5' : update_phone
}

def report_script(body, peer_id, code):
    message = vkMessage('')
    if code == '0' and body.lower() == 'регистрация':
        message = check_fill(peer_id, code)
    elif code in ['1','2','3','4','5']:
        if body.lower() == 'отмена':
            DB.delete_person(peer_id)
            return MM.start_menu()
        else:
            message = state_list[code](peer_id, body, code)
    return message

report_script_command.description = ''
report_script_command.process = report_script
