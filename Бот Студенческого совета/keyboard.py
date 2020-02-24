from string import Template
import string
import vkapi
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender
import DataBase as DB
import Ticket
from vkMessage import vkMessage
import re

Button = Template("""
    {
        "action": {
          "type": "text",
          "payload": "$payload",
          "label": "$label"
        },
        "color": "$color"
      }""")

colors = {'red':'negative',
          'green':'positive',
          'white':'default',
          'blue':'primary'}

class KeyBoard:
    def __init__(self, one_time = 'false', rows = 2):
        self.keyboard = '{"one_time":%s,"buttons":[' % (one_time)
        self.rows = rows
        self.one_time = one_time
        self.Buttons = []
        self.buttonCount = 0


    def add_button(self, label = 'button', color = 'red', payload = '{\\"text\\":\\"''\\"}'):
        self.Buttons.append({'label' : label,
                        'color' : color,
                        'payload' : payload})
        self.buttonCount += 1

    def get_button(self):
        for k, button in enumerate(self.Buttons, 1):
            if not (k - 1) % self.rows:
                self.keyboard += '['
            self.keyboard += Button.substitute(payload = button['payload'], label = button['label'], color = colors[button['color']]) + ','
            if (not k % self.rows) or k == len(self.Buttons):
                self.keyboard = self.keyboard[:-1] + '],'
        if self.Buttons:
            self.Buttons = []
            return self.keyboard[:-1]+']}'

    def get_with_person_button(self, person_button_text):
        self.get_button()
        self.keyboard = self.keyboard[:-1] + ',['
        self.keyboard += Button.substitute(payload = '{\\"text\\":\\"''\\"}', label = person_button_text, color = colors['red']) + ']]}'
        return self.keyboard

def bdate(id):
    bdate = vkapi.get_bdate(id)
    tbdate = bdate.split('.')
    try:
        if(int(tbdate[1]) < 10):
            tbdate[1] = "0" + str(tbdate[1])
        if(int(tbdate[0]) < 10):
            tbdate[0] = "0" + str(tbdate[0])

        tbdate[2]
        return '.'.join(tbdate)
    except Exception as e:
        return None

def dative_surname(id):
    FI = DB.get_person(id)[1].split(' ')
    petr = Petrovich()
    surname = petr.lastname(FI[0], Case.DATIVE)
    name = petr.firstname(FI[1], Case.DATIVE)
    return surname + ' ' + name

def dative_name(id):
    FI = DB.get_person(id)[1].split(' ')
    petr = Petrovich()
    name = petr.firstname(FI[1], Case.DATIVE)
    return FI[0] + ' ' + name

def get_ygrad(id):
    person = DB.get_user(id)
    group_name = person[2]
    a = int(re.findall("\d+", group_name)[0][0])
    if group_name[-1] == "М":
        a = a - 4
    return 9 - a

def get_code(person, prefix = "AIS"):
    args = (get_ygrad(person[0]), person[1])
    query = """
               SELECT COUNT(0)
               FROM AIS
               WHERE Course = %s
               AND Faculty = %s
            """ % args
    number = DB.get_data(query)
    code = 0
    code += person[1] * 10000
    code += get_ygrad(person[0]) * 1000
    code += number[0] + 1
    return prefix + str(code)

def get_ticket(id):
    person = DB.get_user(id)
    code = get_code(person)
    FI = re.match("[а-яё]+ [а-яё]+", person[3], flags= re.I).group(0)
    add_message = vkMessage('Держите Ваш билет.\n\
                             Этот билет необходимо предъявить на стойке регистрации около аудитории, в которой будет проходить форум 1 марта.\n\
                             Распечатывать билет не обязательно, достаточно будет показать штрих-код на билете с телефона, и ваше присутствие будет зарегистрировано!')
    add_message.attachment = Ticket.get_ticket_attachment(id, FI, code)
    add_message.peer_id = add_message.user_id = id
    add_message.send()
    return code


def get_insta(id):
    insta = vkapi.get_insta(id)
    if insta:
        return insta
    else:
        return None


input_mapping = {
    '$дательный' : dative_surname,
    '$дательный_имя' : dative_name,
    '$дата_вк' : bdate,
    '$ticket_id' : get_ticket,
    '$course' : get_ygrad,
    '$insta' : get_insta
}
