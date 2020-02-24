#coding: utf-8

from flask import Flask, render_template, request, redirect
import json
import requests as req
from flask_wtf import FlaskForm
from wtforms import StringField
import MarchLibrary as ML

app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisisasecret!"


class KeyInput(FlaskForm):
    key = StringField('key', render_kw={'autofocus': True})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/end', methods=['GET'])
def form():
    try:
        id = request.cookies.get('vk_id')
        ticket = ML.get_number(id)
        wish = ML.get_wish(ticket, id)
    except:
        redirect_to_auth = redirect('/')
        return app.make_response(redirect_to_auth)
    return render_template('end.html', ticket=ticket, wish=wish)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    key = KeyInput()
    id = request.cookies.get('vk_id')
    if id:
        if ML.check_person(id):
            redirect_to_auth = redirect('/end')
            return app.make_response(redirect_to_auth)
    else:
        redirect_to_auth = redirect('/')
        return app.make_response(redirect_to_auth)

    if key.validate_on_submit():
        if not (ML.check_key(key.key.data)):
            ML.add_person(id)
            ML.key_used(key.key.data)
            redirect_to_auth = redirect('/end')
            return app.make_response(redirect_to_auth)
        else:
            text = "неверно"
            return render_template('auth.html', key=key, wrong_key=text)

    return render_template('auth.html', key=key, wrong_key="")


@app.route('/set_cookie', methods=['POST', 'GET'])
def cookie():
    code = request.args['code']
    answer = req.post('https://oauth.vk.com/access_token', data={
                         'client_id': 'xxx',
                         'client_secret': 'xxx',
                         'redirect_uri': 'https://xn--8-8sbab0degus9b.xn--p1ai/set_cookie',
                         'code': str(code)

                     })
    a = json.loads(answer.text)['user_id']
    if not ML.check_person(a):
        redirect_to_auth = redirect('/auth')
    else:
        redirect_to_auth = redirect('/end')

    resp = app.make_response(redirect_to_auth)
    resp.set_cookie('vk_id', str(a))
    return resp


if __name__ == "__main__":
    app.run(debug=True)
