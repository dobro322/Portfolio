import command_system
import random
from vkMessage import vkMessage

def masha(str, peer_id):
    message = vkMessage('')
    for i in masha_command.keys:
        if i in str:
            start = ['турбо','толма','смир','пусси','стёпа','гум','инком','баба','чугун','дети','пиар','шейко','хули','цыпа','посто','дезигно']
            middle = ['чёво','свин','маша','пончик','копатыч','нова','пенетрейтор','пуков','фак','говно','зина','погиб','ганов']
            end = ['1999','228','322','1488','1337','3000']

            mes = ''
            mes += start[random.randint(0,len(start) - 1)]
            mes += middle[random.randint(0,len(middle) - 1)]
            mes += end[random.randint(0,len(end) - 1)]
            message.message = mes
            return message
    return message

masha_command = command_system.Command()

masha_command.keys = ['напомни пароль маши']
masha_command.description = ''
masha_command.process = masha
