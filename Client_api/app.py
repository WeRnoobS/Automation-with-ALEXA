from Executing import ExecutingCommands
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
    return ExecutingCommands.ExecutingCommands.getInstance().handle_Commands(command)


@app.route('/dialogcommand', methods=['GET'])
def handle_dialogcommand():
    command = request.args.get('command', '').replace(" ", "")
    args = request.args.get('args', '').replace(" ", "")
    print(command)
    return ExecutingCommands.ExecutingCommands.getInstance().DialogCommand(command, args)


@app.route('/result', methods=['GET'])
def handle_result():
    args1 = request.args.get('value1', '')
    args2 = request.args.get('value2', '')
    print(args1+args2)
    return ExecutingCommands.ExecutingCommands.getInstance().result(args1, args2)


@app.route('/getProjectNames', methods=['GET'])
def getProjectNames():
    print("get Project names Called")
    return ExecutingCommands.ExecutingCommands.getInstance().getProjectNames()


@app.route('/openProject', methods=['GET'])
def openProject():
    print("Called openProject")
    val = request.args.get(key="option", default=0, type=int)
    return ExecutingCommands.ExecutingCommands.getInstance().openProject(val)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=5001)
