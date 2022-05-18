from flask import Flask, escape, request, jsonify,render_template
from firebase_admin import credentials, firestore, initialize_app
import json
from os import environ

cred = credentials.Certificate({
    "type": environ["TYPE"],
    "project_id": environ["project_id"],
    "private_key_id": environ["private_key_id"],
    "private_key": environ["private_key"].replace('\\n', '\n'),
    "client_email": environ["client_email"],
    "client_id": environ["client_id"],
    "auth_uri": environ["auth_uri"],
    "token_uri": environ["token_uri"],
    "auth_provider_x509_cert_url": environ["auth_provider_x509_cert_url"],
    "client_x509_cert_url": environ["client_x509_cert_url"]
})

default_app = initialize_app(cred)
db = firestore.client() 
todo_ref = db.collection('urls')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/command', methods=['GET'])
def handle_command():
    command = request.args.get('command', '')
    return command


@app.route('/add', methods=['POST'])
def create():
    # http://300bf87b.ngrok.io/add?url=https://google.in
    try:
        _urls = str(request.args.get('url', ''))
        _data = {u"url": _urls}
        todo_ref.document("url").set(_data)
        t = todo_ref.document("url").get()
        print("checking")
        # read()
        if t.to_dict() == _data:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"data not entered correctly": False}), 400
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/read', methods=['GET'])
def read():
    # http://300bf87b.ngrok.io/read?id=url
    
    try:
        todo_id = request.args.get('id')
        print(todo_id)
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            # y=todo.to_dict()
            print(todo.to_dict()["url"])
            return todo.to_dict()["url"], 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    # http://300bf87b.ngrok.io/delete?id=url
    try:
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
