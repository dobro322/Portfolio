from flask import Flask, render_template, jsonify, request
import json
import handler
from flask_cors import cross_origin

app = Flask(__name__)


API_HANDLER = {
    'user': {
        'new': handler.new_user,
        'state': handler.get_state,
        'updateinfo': handler.update_info,
        'all': handler.all_users,
        'delete_all': handler.delete_all_users
    },
    'operator': {
        'calluser': handler.call_user,
        'create': handler.create_operator,
        'show': handler.show_operators,
        'delete_all': handler.delete_all_operators,
        'move_user': handler.move_user,
        'add_course': handler.add_course,
        'get_courses': handler.get_course,
        'clear_current': handler.clearCurrent
    }
}


@app.route('/admin', methods=['GET'])
def panel():
    return render_template('index.html')


@app.route('/tv', methods=['GET'])
def tv():
    return render_template('tv.html')


@app.route('/tv/api', methods=['POST'])
@cross_origin()
def tv_api():
    props = request.get_json()
    return jsonify(handler.show_tv(props['faculties']))


@app.route('/api/<string:method>/<string:type>', methods=['POST', 'GET'])
@cross_origin()
def api(method, type):
    if method in API_HANDLER:
        if type in API_HANDLER[method]:
            props = request.get_json()
            return jsonify({'items': API_HANDLER[method][type](data = props if props else {})})
        else:
            return {'error': 'No such method: ' + str(type)}
    else:
        return {'error': 'No such method: ' + str(method)}
    return json.dumps({'method': method, 'type': type})


if __name__ == "__main__":
    app.run(debug=True)
