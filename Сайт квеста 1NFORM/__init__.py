#coding: utf-8
from pymongo import MongoClient
from flask import Flask, render_template, redirect, request, json
import datetime
import requests as req
from flask_cors import cross_origin
import MongoDataBase
import School

app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisisasecret!"


@app.route('/platondrius', methods=['GET', 'POST'])
def admin():
    data = request.get_json()
    if data:
        if data['method'] == 'refill':
            School.refill()
        if data['method'] == 'delete_all_users':
            MongoDataBase.delete_all_users()
        if data['method'] == 'fill_random':
            MongoDataBase.fill_random()
        if data['method'] == 'sort_pk':
            MongoDataBase.sort_pk('hello')
    return render_template('admin.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/parttable/', methods=["GET"])
def parttable():
    code = request.args.get("code")
    if code:
        answer = req.post('https://oauth.vk.com/access_token', data={
                         'client_id': 'xxx',
                         'client_secret': 'xxx',
                         'redirect_uri': 'http://1nform.ru/parttable',
                         'code': str(code)
                     })
        vk = json.loads(answer.text)['user_id']
        resp = app.make_response(redirect('/parttable'))
        resp.set_cookie('vk', str(vk), max_age=60*60*24*365*2)
        return resp
    vk = request.cookies.get('vk')
    if vk:
        if MongoDataBase.check_org(vk):
            return render_template('parttable.html')
        else:
            return render_template('NotFound.html')
    else:
        return render_template('orgauth.html')


@app.route('/school/', methods=["GET"])
def school():
    token = request.cookies.get('token')
    code = request.args.get("code")
    if token and not code:
        coll = MongoClient('xxx', 27017).school.user
        user = coll.find_one({'token': (token)})
        if user:
            if user['deps']:
                resp = app.make_response(redirect('/school/card'))
                return resp
            return render_template('school.html')
        else:
            return render_template('vkauth.html')
    if code:
        answer = req.post('https://oauth.vk.com/access_token', data={
                         'client_id': 'xxx',
                         'client_secret': 'xxx',
                         'redirect_uri': 'http://1nform.ru/school',
                         'code': str(code)
                     })
        token = json.loads(answer.text)['access_token']
        vk = json.loads(answer.text)['user_id']
        token = MongoDataBase.user_check(int(vk), token)
        if not token:
            return render_template('NotFound.html')
        resp = app.make_response(redirect('/school'))
        resp.set_cookie('token', str(token), max_age=60*60*24*365*2)
        resp.set_cookie('vk', str(vk), max_age=60*60*24*365*2)
        return resp
    return render_template('vkauth.html')


@app.route('/api/schelude/', methods=["GET", "POST"])
@cross_origin()
def schelude():
    now = datetime.datetime.now()
    datetime.time(now.hour, now.minute, now.second)
    return str(datetime.time(now.hour, now.minute, now.second))


@app.route('/school/api/user/', methods=["POST", "GET"])
@cross_origin()
def user():
    data = request.get_json()
    HANDLER = {
        'queue': MongoDataBase.get_queue,
        'check_user': MongoDataBase.check_user,
        'update': MongoDataBase.new_deps_comment,
        'reserve': MongoDataBase.reserve_change
    }
    data = HANDLER[data['method']](data= data)
    return json.dumps(data)


@app.route('/school/api/queue/', methods=["POST", "GET"])
@cross_origin()
def queue():
    data = request.get_json()
    HANDLER = {
        'next': MongoDataBase.get_next_queue,
        'to_end': MongoDataBase.queue_to_end,
        'delete': MongoDataBase.get_next_queue,
        'current': MongoDataBase.first_queue,
        'last': MongoDataBase.last_queue,
        'update': MongoDataBase.update_comment,
        'all': MongoDataBase.get_all
    }
    data = HANDLER[data['method']](data= data)
    return json.dumps(data)


@app.route('/school/card/', methods=["GET"])
@cross_origin()
def card():
    token = request.cookies.get('token')
    if not token:
        return app.make_response(redirect('/school'))

    user = MongoDataBase.check_user({'token': token})
    if user:
        if user['deps']:
            return render_template('card.html', token=token)

    deps = []
    dct = request.args.to_dict()
    if dct:
        if 'surfer' in dct:
            deps += ['Сёрфер']
        if 'companion' in dct:
            deps += ['Собеседник']
        if 'pk' in dct:
            deps += ['Приемная комиссия']
        if 'fundraising' in dct:
            deps += ['Фандрайзинг']
        if 'secondary' in dct:
            deps += [dct['secondary']]
        user = {
            'token': token,
            'vk': request.cookies.get('vk'),
            'deps': deps
        }
        MongoDataBase.update_user(user)
        return app.make_response(redirect('/school/card'))
    else:
        return app.make_response(redirect('/school'))


@app.route('/panel/', methods=["GET"])
def panel():
    code = request.args.get("code")
    if code:
        answer = req.post('https://oauth.vk.com/access_token', data={
                         'client_id': 'xxx',
                         'client_secret': 'xxx',
                         'redirect_uri': 'http://1nform.ru/panel',
                         'code': str(code)
                     })
        vk = json.loads(answer.text)['user_id']
        resp = app.make_response(redirect('/panel'))
        resp.set_cookie('vk', str(vk), max_age=60*60*24*365*2)
        return resp
    vk = request.cookies.get('vk')
    if vk:
        if MongoDataBase.check_org(vk):
            return render_template('panel.html')
        else:
            return render_template('NotFound.html')
    else:
        return render_template('panelauth.html')


if __name__ == "__main__":
    app.run(debug=True)
