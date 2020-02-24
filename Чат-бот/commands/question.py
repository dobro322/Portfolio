import command_system
import random
from datetime import datetime, date, timedelta
from vkMessage import vkMessage
import vkapi

def question(body, peer_id):
    message = vkMessage('')
    print('question')
    if '?' in body:
        temp = body.split(' ')
        for i in temp:
            message = vkMessage('')
            if 'кто' in i and peer_id > 2000000000:
                message.message = vkapi.get_random_conf_user(peer_id)
                return message
            elif 'зачем' in i or 'почему' in i:
                answers = ['А почему ви спгашиваете?', 'Во славу сатане, конечно!', '42']
                message.message = answers[random.randint(0,len(answers) - 1)]
                return message
            elif 'когда' in i:
                startdate=date(2000,1,1)
                nbdays=(date(2036,1,1)-startdate).days
                d=random.randint(0,nbdays)
                message.message = str(startdate+timedelta(days=d))
                return message
            elif 'где' in i:
                if 'риба' in body:
                    message.attachment = "photo-146208019_456241261"
                else:
                    latitude = random.uniform(50,70)
                    longitude = random.uniform(26,180)
                    message.coord = {'lat':latitude, 'long':longitude}
                message.message = 'Тут'
                return message
            elif 'сколько' in i:
                message.message = random.randint(-1000,1000)
                return message

        variables = ['Нет','Не думаю','Ни в коем случае','Не уверен','Маловероятно','Плохо верится','50/50','Может да, а может и нет', 'Затрудняюсь ответить', 'А почему ви спгашиваете?', 'Скорее всего', 'Вполне возможно', 'Вероятность высока', 'Точно', 'Однозначно', 'Да']
        message.message = variables[random.randint(0,len(variables) - 1)]
    return message

question_command = command_system.Command()

question_command.keys = ['?']
question_command.description = '&#128290; Сколько *сообщение*? - выдаю рандомное число от -1000 до 1000\n&#127757; Где *сообщение*? - выдаю случайную геолокацию в области России\n&#128197; Когда *сообщение*? - выдаю случайную дату с 2000 по 2036 год'
question_command.process = question
