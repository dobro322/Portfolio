import vkapi
import os
import importlib
import re
from command_system import command_list
from vkMessage import vkMessage
import DataBase as DB
import main_menu as MM
import keyboard
import spreadsheets

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


def event_menu_template(state, message):
    message = vkMessage(message)
    kb = state[2].split(';')
    KB = keyboard.KeyBoard('false', 1)
    for k in kb:
        KB.add_button(k, color = 'white')
    message.keyboard = KB.get_with_person_button('Назад')
    return message


def events_menu(body, id, code):
    message = vkMessage('В этом меню у вас есть возможность зарегистрироваться на мероприятия:\n')
    events = DB.get_events()
    if events:
        DB.set_state(id, 'Events')
        KB = keyboard.KeyBoard('true', 1)
        for event in events:
            KB.add_button(event[2], 'white')
            message.message += '•' + event[1] + '\n'
        message.keyboard = KB.get_with_person_button('Меню')
    else:
        DB.set_state(id, 9)
        message.message = "К сожалению, мероприятий нет"
        message.keyboard = MM.main_menu_keyboard()

    return message


def submenu_keyboard_template(state,id):
    try:
        args = state[2].split(';')

        if re.match(u'%\d+', args[0]):
            KB = keyboard.KeyBoard('false', int(args[0][1:]))
            args = args[1:]
        else:
            KB = keyboard.KeyBoard('false', 1)

        for key in args:
            if key[0] == "$":
                if not keyboard.input_mapping[key](id) is None:
                    KB.add_button(keyboard.input_mapping[key](id), 'green')
            else:
                KB.add_button(key, 'white')
        KB.add_button("Отмена")
        return KB.get_button()

    except Exception as e:
        KB = keyboard.KeyBoard('false', 1)
        KB.add_button('Отмена', 'red')
        return KB.get_button()


def is_registrated(code, id):
    count = DB.get_submenu_count('_'.join(code[0:3]))
    a = DB.is_registrated('_'.join(code[0:3]), count, id)
    return a


def event_menu(body, id, code, attachments):
    message = vkMessage('')
    if body == 'Назад':
        DB.set_state(id, 'Events')
        return events_menu(body, id, code)
    state = DB.full_state_info('_'.join(code))
    if body in "Что это такое?":
        state = DB.full_state_info('_'.join(code))
        msg = DB.get_event_help('_'.join(code)) + '\n' + state[1]
        message = event_menu_template(state, msg)
        return message
    if body in state[2].split(';'):
        if (body == "Регистрация") and is_registrated(code + ["1"], id):
            return vkMessage('Вы уже зарегистрированы!')
        state = DB.get_event_submenu('_'.join(code), body)
        DB.set_state(id, state[0])
        message.message = state[1]
        DB.new_event_participant(state[0][:-2], id)
        message.keyboard = submenu_keyboard_template(state, id)

    return message


def choose_event(body, id, code, attachments):
    message = vkMessage('')
    if body in 'Меню':
        DB.set_state(id, 9)
        message = MM.main_menu()
        return message
    events = DB.get_events()
    for event in events:
        if body in event:
            DB.set_state(id, event[0])
            state = DB.full_state_info(event[0])
            message = event_menu_template(state, state[1])
    return message


def event_submenu(body, id, code, attachments):
    message = vkMessage('')

    for attch in attachments:
        body += "\n" + attch[attch['type']]['url']

    if body == "Отмена":
        DB.set_state(id, '_'.join(code[0:2]))
        state = DB.full_state_info('_'.join(code[0:2]))
        message = event_menu_template(state, state[1])
        DB.remove_participant('_'.join(code[0:3]), id)
        return message
    last_event_record_date = DB.get_last_event_record_date('_'.join(code[0:3]), id)
    DB.update_event_participant('_'.join(code[0:3]), code[-1], body, id, last_event_record_date)
    count = DB.get_submenu_count('_'.join(code[0:3]))

    if int(code[-1]) < count:
        code[-1] = str(int(code[-1]) + 1)
        state = DB.full_state_info('_'.join(code))
        DB.set_state(id, state[0])
        while (state[1][0] == "$") and (int(code[-1]) <= count):
            body = keyboard.input_mapping[state[1]](id)
            last_event_record_date = DB.get_last_event_record_date('_'.join(code[0:3]), id)
            DB.update_event_participant('_'.join(code[0:3]), code[-1], body, id, last_event_record_date)
            if int(code[-1]) == count:
                curr_state = DB.full_state_info('_'.join(code))
                DB.set_state(id, '_'.join(code[0:2]))
                state = DB.full_state_info('_'.join(code[0:2]))
                return event_menu_template(state, curr_state[3] + '\n\n' + state[1])
            code[-1] = str(int(code[-1]) + 1)
            state = DB.full_state_info('_'.join(code))
            DB.set_state(id, state[0])
        message.message = state[1]
        message.keyboard = submenu_keyboard_template(state, id)
        return message

    if int(code[-1]) == count:
        if '_'.join(code) == "Events_7_1_2":
            List = 'Приемная комиссия'
            person = DB.get_umka(id)
            person = list(person)
            person[1] = "vk.com/id" + str(person[1])
            person[2] = faculties[person[2] - 1]
            person = tuple(person)
            person_event = DB.get_event_participant(id, '_'.join(code[0:3]))
            person_event = list(person_event)
            person_event = tuple(person_event)
            result_person = (person_event[0],) + person + person_event[2:]
            spreadsheets.add_note(result_person, DB.participant_count('_'.join(code[0:3]), "2"), List, '1yWWAGZUVsRnRLV5uwSyWJE7cPYOskRYu6K_O7sdklP0')
        if '_'.join(code) == "Events_8_1_3":
            List = '1NFORM'
            person = DB.get_umka(id)
            person = list(person)
            person[1] = "vk.com/id" + str(person[1])
            person[2] = faculties[person[2] - 1]
            person = tuple(person)
            person_event = DB.get_event_participant(id, '_'.join(code[0:3]))
            person_event = list(person_event)
            person_event = tuple(person_event)
            result_person = (person_event[0],) + person + person_event[2:]
            spreadsheets.add_note(result_person, DB.participant_count('_'.join(code[0:3]), "3"), List, '1CkS4Kvw8J7fCUFUZ2KFpmvBzikd8TRyGGVcjtoqPjNU')
        curr_state = DB.full_state_info('_'.join(code))
        DB.set_state(id, '_'.join(code[0:2]))
        state = DB.full_state_info('_'.join(code[0:2]))
        message = event_menu_template(state, curr_state[3] + '\n\n' + state[1])
        return message


def update_spreadsheet():
    asd = [x[0] for x in DB.rewrite()]
    for k, x in enumerate(asd):
        person = DB.get_msha_user(x)
        person = list(person)
        person[1] = faculties[int(person[1]) - 1]
        person = tuple(person)
        person_event = DB.get_event_participant(x, "Events_2_1")
        person_event = list(person_event)
        person_event[1] = "vk.com/id" + str(person_event[1])
        person_event = tuple(person_event)
        result_person = (person_event[0], ) + person + person_event[1:]
        spreadsheets.add_note(result_person, k + 1)


# update_spreadsheet()



def events_main(body, id, code, attachments):
    if code == '9':
        return events_menu(body, id, code)
    code = code.split('_')
    unit_controller = {
        1: choose_event,
        2: event_menu,
        4: event_submenu
    }
    return unit_controller[len(code)](body, id, code, attachments)
