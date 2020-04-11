from Executing import ExecutingCommands as EC
from flask import Flask, escape, request
import os
app = Flask(__name__)


@app.route('/')
def hello():
    name = os.environ['COMPUTERNAME']
    return f'Hello, {escape(name)}!'


@app.route('/command', methods=['GET'])
def handle_command():
    command = request.args.get('command', '').replace(" ", "")
    print(command)
    return EC.handle_Commands(command)


@app.route('/dialogcommand', methods=['GET'])
def handle_dialogcommand():
    command = request.args.get('command', '').replace(" ", "")
    args = request.args.get('args', '').replace(" ", "")
    print(command)
    return EC.DialogCommand(command, args)


@app.route('/result', methods=['GET'])
def handle_result():
    args1 = request.args.get('value1', '')
    args2 = request.args.get('value2', '')
    print(args1+args2)
    return EC.result(args1, args2)
    
    # return "done"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
