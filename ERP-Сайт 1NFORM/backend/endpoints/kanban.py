from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
from .. import Questing

api = Namespace('kanban', description='Kanban operations')
task_api = Namespace('task', description='Task operations')


def check(user, dep):
    user = DB.get_member('departments', user['vk'])
    if dep in user['departments'] or dep == 'Все':
        return True
    else:
        return False


@api.route('/')
class Kanbans(Resource):
    @role('204')
    def get(self):
        token = request.headers.get('Authorization')
        return DB.get_member_deps(token), 200


@api.route('/<string:dep>')
class Kanban(Resource):
    @role('204')
    def get(self, dep):
        if dep in DB.check_member('departments', request.headers.get('Authorization'))['departments'] or dep == 'Все':
            answer = DB.get_tasks(dep)
            responsibles = DB.users_from_dep(dep, 'info')
            return {"tasks": answer, "responsibles": responsibles}, 200
        else:
            return {"Msg": 'No permissions for this department'}, 405

    @role('204')
    def post(self, dep):

        data = request.data
        if not data:
            return {"Msg": 'No data passed'}, 422

        data = json.loads(data)

        member = DB.check_member('info,score,quests,news,departments', request.headers.get('Authorization'))
        if dep in member['departments'] or dep == 'Все':

            for responsible in data['responsibles']:
                if not check(responsible, dep):
                    return {
                        "Msg": "Can't add %s as a responsible" % responsible['name']
                    }, 422
                else:
                    DB.add_news({
                        "title": "Канбан",
                        "text": "Вы были упомянуты в новой задаче '%s'" % data['title'],
                        "type": "personal"
                    }, member['info']['vk'])

            Questing.task_quest("add", data, member)
            return DB.add_task(data, member), 200
        else:
            return {"Msg": 'Not allowed'}, 405


@task_api.route('/<int:task>')
class Task(Resource):
    @role('204')
    def get(self, task):
        task = DB.get_task(task)
        if task['department'] in DB.check_member('departments', request.headers.get('Authorization'))['departments'] or task['department'] == 'Все':
            return task, 200
        else:
            return {"Msg": 'Not allowed'}, 405

    @role('204')
    def post(self, task):
        data = request.data
        if not data:
            return {"Msg": 'No task passed'}, 422

        data = json.loads(data)

        if 'comment' not in data:
            return {"Msg": 'comment is needed'}, 422

        member = DB.check_member('info,score,quests,departments', request.headers.get('Authorization'))
        task = DB.get_task(task)

        if task['department'] in member['departments'] or task['department'] == 'Все':

            for responsible in task['responsibles']:
                if not check(responsible, task['department']):
                    return {
                        "Msg": "Can't add %s as a responsible" % responsible['name']
                    }, 422
                else:
                    DB.add_news({
                        "title": "Канбан",
                        "text": "Задача, в которой вы упомянуты, была прокомментирована '%s'" % task['title'],
                        "type": "personal"
                    }, member['info']['vk'])

            Questing.task_quest("comment", data, member)
            return DB.add_task_comment(data['comment'], task['id'], member), 200
        else:
            return {"Msg": 'Not allowed'}, 405

    @role('224')
    def put(self, task):
        data = request.data
        if not data:
            return {"Msg": 'No task passed'}, 422

        data = json.loads(data)
        member = DB.check_member('departments,info', request.headers.get('Authorization'))
        task = DB.get_task(task)

        if task['department'] in member['departments'] or task['department']  == 'Все':

            for responsible in task['responsibles']:
                if not check(responsible, task['department']):
                    return {
                        "Msg": "Can't add %s as a responsible" % responsible['name']
                    }, 422
                else:
                    DB.add_news({
                        "title": "Канбан",
                        "text": "Задача, в которой вы упомянуты, была изменена '%s'" % task['title'],
                        "type": "personal"
                    }, member['info']['vk'])

            return DB.change_task(data, task['id']), 200
        else:
            return {"Msg": 'Not allowed'}, 405

    @role('724')
    def delete(self, task):
        if DB.get_task(task)['department'] in DB.check_member('departments', request.headers.get('Authorization'))['departments'] or DB.get_task(task)['department'] == 'Все':
            return DB.delete_task(task), 200
        else:
            return {"Msg": 'Not allowed'}, 405
