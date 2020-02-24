from functools import wraps
from flask import request
from . import DataBase as DB
from .DataBase import currtime
import re
from datetime import datetime, timedelta

"""
Сообщения
"""


def messages_new(quest, member, text):
    return 1


def words_count(quest, member, text):
    return len(text.split(' '))


def gav_count(quest, member, text):
    result = re.findall(r'[гГ]ав', text)
    return 1 if len(result) > 0 else 0


def emoji_count(quest, member, text):
    result = re.findall(r'💜', text)
    return 1 if len(result) > 0 else 0


def bracket_count(quest, member, text):
    result = re.findall(r'\)\)\)', text)
    return 1 if len(result) > 0 else 0


"""
Серфинг
"""


def faculty_take_count(quest, member, abit):
    return 1 if abit['faculty'] in quest['counting']['additional']['faculty'] else 0


def other_take_count(quest, member, abit):
    return 1 if not abit['faculty'] == member['info']['faculty'] else 0


def add_count(quest, member, abit):
    return 1


def faculty_hard_count(quest, member, abit):
    return 1 if abit['faculty'] in quest['counting']['additional']['faculty'] else 0


def other_hard_count(quest, member, abit):
    return 1 if not abit['faculty'] == member['info']['faculty'] else 0


def faculty_found_count(quest, member, abit):
    return 1 if abit['faculty'] in quest['counting']['additional']['faculty'] else 0


def other_found_count(quest, member, abit):
    return 1 if not abit['faculty'] == member['info']['faculty'] else 0


def faculty_hardfound_count(quest, member, abit):
    return 1 if abit['faculty'] in quest['counting']['additional']['faculty'] and abit['status']['name'] == '3' else 0


def other_hardfound_count(quest, member, abit):
    return 1 if not abit['faculty'] == member['info']['faculty'] and abit['status']['name'] == '3' else 0


def abiturient_comment_count(quest, member, abit):
    return 1


"""
Задания
"""


def task_count(quest, member, task):
    return 1


def task_comments_count(quest, member, task):
    return 1


def task_comments_words_count(quest, member, task):
    return len(task['description'].split(' '))


QUEST_HANDLER = {
    "messages": {
        "new": {
            "counting_messages": {
                "description": "Считать количество сообщений",
                "function": messages_new,
            },
            "counting_words": {
                "description": "Считать количество слов",
                "function": words_count
            },
            "counting_emoji": {
                "description": "Считать количество эмодзи",
                "function": emoji_count
            },
            "counting_brackets": {
                "description": "Считать количество скобок",
                "function": bracket_count
            },
            "counting_gavs": {
                "description": "Считать количество гав",
                "function": gav_count
            }
        }
    },
    "surf": {
        "take": {
            "take_faculty": {
                "description": "Считать количество взятых абитуриентов с факультета",
                "function": faculty_take_count
            },
            "other_faculty": {
                "description": "Считать количество взятых абитуриентов не со своего факультета",
                "function": other_take_count
            }
        },
        "add": {
            "add_faculty": {
                "description": "Считать количество добавленных в конфы абитуриентов",
                "function": add_count
            }
        },
        "hard": {
            "hard_faculty": {
                "description": "Считать количество абитуриентов, отправленных в 'сложное' c факультета",
                "function": faculty_hard_count
            },
            "hard_other_faculty": {
                "description": "Считать количество абитуриентов, отправленных в 'сложное' не со своего факультета",
                "function": other_hard_count
            }
        },
        "confirm": {
            "find_faculty": {
                "description": "Считать количество абитуриентов, найденных с факультета",
                "function": faculty_found_count
            },
            "find_other_faculty": {
                "description": "Считать количество абитуриентов, найденных не со своего факультета",
                "function": other_found_count
            },
            "find_hard_faculty": {
                "description": "Считать количество сложных абитуриентов, найденных с факультета",
                "function": faculty_hardfound_count
            },
            "find_hard_other": {
                "description": "Считать количество сложных абитуриентов, найденных не со своего факультета",
                "function": other_hardfound_count
            }
        },
        "platfinder_success": {
            "find_faculty_platfinder": {
                "description": "Считать количество абитуриентов, найденных с факультета системой",
                "function": faculty_found_count
            },
        },
        "platfinder_failed": {
            "failed_faculty_platfinder": {
                "description": "Считать количество ошибок Платфайндера",
                "function": faculty_found_count
            },
        },
        "comment": {
            "counting_comments": {
                "description": "Считать количество комментариев абитуриентам",
                "function": abiturient_comment_count
            }
        },
        "fail_predict": {
            "counting_failed_confirmation":{
                "description": "Считать количество раз, когда человек подтверждает неверное предложение системы",
                "function": add_count
            }
        },
        "confirm_predict": {
            "counting_success_confirmation":{
                "description": "Считать количество раз, когда человек подтверждает верное предложение системы",
                "function": add_count
            }
        }
    },
    "tasks": {
        "add": {
            "counting_task": {
                "description": "Считать количество добавленных тасков в канбан-доску",
                "function": task_count
            }
        },
        "comment": {
            "counting_task_comments": {
                "description": "Считать количество комментариев для тасков",
                "function": task_comments_count
            },
            "counting_task_comments_words": {
                "description": "Считать количество слов комментариев для тасков",
                "function": task_comments_words_count
            }
        }
    }
}


def drop_abit_found_quests(member, abit):

    DB.inform_users.update_one(
        {
            "info.vk": member['info']['vk'],
            "score.surf.faculty": abit['faculty']
        },
        {
            "$inc": {
                "score.surf.$.amount": -1
            }
        }
    )

    for quest in member['quests']:

        if quest['added'] > abit['status']['date_found']:
            continue

        if datetime.fromtimestamp(quest['date']).date() < datetime.fromtimestamp(abit['status']['date_found']).date():
            continue

        if 'date_completed' in quest:
            if quest['date_completed']:
                if quest['date_completed'] < abit['status']['date_found']:
                    continue

        quest_template = DB.inform_quests.find_one({"id": quest["id"]})

        if not quest_template:
            continue

        if quest_template['counting']['function'] not in QUEST_HANDLER['surf']['confirm'].keys():
            continue

        if quest_template['daily']:
            if not datetime.fromtimestamp(quest['added']).date() == datetime.fromtimestamp(abit['status']['date_found']).date():
                continue

        function_list = [
            "find_faculty",
            "find_other_faculty",
            "find_hard_faculty",
            "find_hard_other"
        ]
        function = quest_template['counting']['function']

        score = 0
        if quest['completed']:
            score = quest_template['cost']

        metric = 0
        if function in function_list:
            metric_func = QUEST_HANDLER["surf"]["confirm"][function]["function"]
            metric = metric_func(quest_template, member, abit)

        DB.inform_users.update_one(
            {
                "info.vk": member['info']['vk'],
            },
            {
                "$inc": {
                    "score.abtx.amount": -score
                }
            }
        )

        DB.inform_users.update_one(
            {
                "info.vk": member['info']['vk'],
                "quests": {
                    "$elemMatch": {
                        "id": quest["id"],
                        "added": quest["added"]
                    }
                }
            },
            {
                "$set": {
                    "quests.$.count.current": quest["count"]["current"] - metric,
                    "quests.$.completed": False,
                    "quests.$.date_completed": None
                }
            }
        )


def achieve_quest(member_id, quest_id):
    member = DB.get_member("info,quests,score", member_id)
    quest = DB.inform_quests.find_one({"id": int(quest_id)})
    data = {
        'id':  quest['id'],
        'date': quest['date'],
        'added': currtime(),
        'count': {
            'current': 1,
            'needed': 1
        },
        'completed': True,
        'date_completed': currtime()
    }
    news = {
        "title": quest['title'],
        "text": 'Поздравляем, вы выполнили задание "{}"'.format(quest['title'])
    }
    DB.add_news(news, member_id)
    DB.add_score(member, quest['cost'])
    member['quests'].append(data)

    return DB.edit_user(
        member_id,
        {
            'quests': member['quests'],
        }
    )


def plustcount(member, quest, metric):
    for qu in member['quests']:
        if qu['id'] == quest['id']:
            quest_date = datetime.fromtimestamp(qu['added']).date()
            today = datetime.fromtimestamp(currtime()).date()

            if qu['completed']:
                if not quest['daily']:
                    return {"Msg": "Completed"}

            if quest['daily']:
                quest_date = datetime.fromtimestamp(qu['added']).date()
                today = datetime.fromtimestamp(currtime()).date()
                if not quest_date == today:
                    continue
                else:
                    if qu['completed']:
                        return {"Msg": "Completed"}
            qu['count']['current'] += metric

            if qu['count']['current'] >= qu['count']['needed']:
                qu['count']['current'] = qu['count']['needed']
                qu['completed'] = True
                qu['date_completed'] = currtime()
                news = {
                    "title": quest['title'],
                    "text": 'Поздравляем, вы выполнили задание "{}"'.format(quest['title'])
                }
                DB.add_news(news, member['info']['vk'])
                DB.add_score(member, quest['cost'])

            return DB.edit_user(
                member['info']['vk'],
                {
                    'quests': member['quests'],
                }
            )

    data = {
        'id':  quest['id'],
        'date': quest['date'],
        'added': currtime(),
        'count': {
            'current': metric,
            'needed': int(quest['counting']['count'])
        },
        'completed': False
    }
    if metric >= int(quest['counting']['count']):
        data['current'] = data['count']['needed']
        data['completed'] = True
        data['date_completed'] = currtime()
        DB.add_score(member, quest['cost'])
        news = {
            "title": quest['title'],
            "text": 'Поздравляем, вы выполнили задание "{}"'.format(quest['title'])
        }
        DB.add_news(news, member['info']['vk'])

    member['quests'].append(data)

    return DB.edit_user(
        member['info']['vk'],
        {
            'quests': member['quests']
        }
    )


def message_quest(arg, member, text):
    quests = DB.get_quests(
        {
            'faculty': member['info']['faculty'],
            'departments': ','.join(member['departments'])
        }
    )
    for quest in quests:
        exp_date = datetime.fromtimestamp(quest['date']).date()
        today = datetime.fromtimestamp(currtime()).date()
        if today <= exp_date:

            if 'function' in quest['counting']:

                function = quest['counting']['function']
                if function in QUEST_HANDLER['messages'][arg]:

                    metric = QUEST_HANDLER['messages'][arg][function]["function"](quest, member, text)
                    plustcount(member, quest, metric)


def surf_quest(arg, abit, member):
    quests = DB.get_quests(
        {
            'faculty': member['info']['faculty'],
            'departments': ','.join(member['departments'])
        }
    )
    for quest in quests:
        exp_date = datetime.fromtimestamp(quest['date']).date()
        today = datetime.fromtimestamp(currtime()).date()
        if today <= exp_date:
            if 'function' in quest['counting']:
                function = quest['counting']['function']
                if function in QUEST_HANDLER['surf'][arg]:

                    metric = QUEST_HANDLER['surf'][arg][function]["function"](quest, member, abit)
                    plustcount(member, quest, metric)


def task_quest(arg, task, member):
    quests = DB.get_quests(
        {
            'faculty': member['info']['faculty'],
            'departments': ','.join(member['departments'])
        }
    )
    for quest in quests:
        exp_date = datetime.fromtimestamp(quest['date']).date() + timedelta(days=1)
        today = datetime.fromtimestamp(currtime()).date()
        if today <= exp_date:
            if 'function' in quest['counting']:
                function = quest['counting']['function']
                if function in QUEST_HANDLER['tasks'][arg]:
                    metric = QUEST_HANDLER['tasks'][arg][function]["function"](quest, member, task)
                    plustcount(member, quest, metric)
