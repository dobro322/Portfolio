import zipfile
import command_system
import vkapi
import requests
from vkMessage import vkMessage
import datetime
import DataBase as DB
import SendToPredsed
from keyboard import KeyBoard
import main_menu as MM
import re

registration_script_command = command_system.Command()

def update_template(report_column):
    return """
    UPDATE Reports
    SET %s = %s
    WHERE ID = (
    SELECT *
    FROM (
    SELECT MAX(ID)
    FROM Reports
    WHERE PersonId = %s)
    AS t1) """ % (report_column,'%s', '%s')

def cancel_keyboard():
    KB = KeyBoard('false', 1)
    KB.add_button('Отмена','red','{}')
    return KB.get_button()

def update(peer_id, column_text, query):
    args = (column_text, peer_id)
    DB.insert_data(query, args)
    code = str(int(DB.get_current_state(peer_id)) + 1)
    DB.set_state(peer_id, code)
    message = vkMessage(DB.get_state_help(code))
    message.keyboard = cancel_keyboard()
    return message

def cancel_report(peer_id):
    DB.delete_report(DB.get_last_report(peer_id)[0])
    DB.set_state(peer_id, 9)
    return MM.main_menu()

def new_report(id):
    query = """
    INSERT INTO Reports(PersonId)
    VALUES(%s)
    """
    DB.insert_data(query, (id,))
    message = vkMessage(DB.get_state_help(6))
    message.keyboard = cancel_keyboard()
    DB.set_state(id, 6)
    return message


def insert_header(id, header):
    header = re.sub(r'жалоба на ',  '', header, flags = re.I)
    query = update_template('Header')
    return update(id, header, query)

def update_body(id, body):
    body = re.sub(r'я жалуюсь на то(,)? что ',  '', body, flags = re.I)
    query = update_template('Body')
    return update(id, body, query)

def update_orders(id, orders):
    query = update_template('Orders')
    args = (orders, id)
    DB.insert_data(query,args)
    code = 9
    DB.set_state(id, code)
    update_date(id)
    SendToPredsed.prepare_doc(id)
    message = MM.main_menu('Ваша жалоба успешно отправлена!\nОжидайте рассмотрения.')
    return message

def update_date(id):
    now = datetime.datetime.now()
    query = update_template('Date')
    now = '%s-%s-%s' % (now.year, now.month, now.day)
    args = (now, id)
    DB.insert_data(query, args)

registration_script_command.keys = [
    '6', #Заголовок жалобы
    '7', #Описание жалобы
    '8', #Требования
    '9'
]

state_list = {
    '6' : insert_header,
    '7' : update_body,
    '8' : update_orders
}
registration_script_command.description = ''


def registration_script(body, peer_id, code):
    message = vkMessage('')
    if code == '9' and body.lower() == 'жалоба':
        message = new_report(peer_id)
    elif code in ['6','7','8']:
        if body.lower() == 'отмена':
            message = cancel_report(peer_id)
        else:
            message = state_list[code](peer_id, body)
    return message

registration_script_command.process = registration_script
