from flask import Flask, render_template, jsonify, request, json
import DataBase as DB
from flask_cors import CORS, cross_origin
import requests


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('index1.html')


@app.route('/showmethetruth', methods=['GET', 'POST'])
def all():
    return render_template('panel.html')


@app.route('/api/<string:method>', methods=['POST'])
@cross_origin()
def api(method):
    handler = {
        'get': DB.get_group,  # name - имя группы
        'new': DB.new_group,  # name - имя группы, course - курс группы, faculty - факультет
        'update': DB.update_group,  # articles - {first - первый семестр, second - второй семестр}
        'all': DB.all_groups,
        'new_answer': DB.new_answer,
        'groups': DB.groups_only
    }
    args = request.data
    if args:
        args = json.loads(args)

        if "token" in args:
            data = {
                "secret": "6LdIb60UAAAAAIpWaEiQN7hoj7aiAm71URZIifzD",
                "response": args["token"]
            }
            uri = "https://www.google.com/recaptcha/api/siteverify"
            resp = requests.post(uri, data=data)
            resp = resp.text
            resp = json.loads(resp)
            if not resp["success"]:
                return {"Msg": "Stop it"}

    server_res = handler[method](args)
    return jsonify(server_res)


if __name__ == '__main__':
    app.run(debug=False)
