from flask import Flask, render_template, request, json, jsonify
import Handler
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'

@app.route("/", methods=["GET", "POST"])
def index():
    data = request.data
    if not data:
        return "No data"
    data = json.loads(data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        token = Handler.get_community(data)["conf_token"]
        return token
    elif data['type'] == 'message_new':
        Handler.create_answer(data['object']['message'], data["group_id"])
    elif data['type'] == 'wall_post_new':
        Handler.create_auto_mailing(data['object'], data["group_id"])
    return 'ok'


@app.route("/admin")
def admin():
    return render_template("index.html")


@app.route("/<string:type>", methods=["POST"])
def api(type):
    data = request.data
    if not data:
        return "No data"
    data = json.loads(data)
    handler = {
        "newSubType": Handler.new_sub_type,
        "newMail": Handler.create_mailing,
        "getAdmin": Handler.get_admin,
        "setAdminGroup": Handler.set_admin_group,
        "getSubs": Handler.get_subs,
        "getCommunity": Handler.get_community,
        "removeSub": Handler.remove_sub,
        "editSub": Handler.edit_sub
    }
    if type not in handler:
        return "No such type"

    res = handler[type](data)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
