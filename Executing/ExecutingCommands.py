import os
import os.path
import shutil


def handle_Commands(command):
    #-----opeing file to check the where it suppoerts are not-----#
    with open("Executing//WindowsApps.txt", "r") as _file:
        _WindowsApps = _file.read()
    with open("Executing//automatoins.txt") as _file:
        _automation = _file.read()

    #-----Main function-----#
    if command in _WindowsApps:
        os.popen(command)
    elif command in _automation:
        print(command)
        return automation(command)
    elif command == "getcommands":
        return listingCommands(command)
    else:
        return "no commands found"
    return "opened"


def automation(command):
    pwd = os.getcwd()
    os.popen(pwd+"\\Executing\\"+command+".lnk")
    return f"{command} started"


def DialogCommand(command, args):
    pwd = os.getcwd()
    os.popen(pwd+"\\Executing\\"+command+".lnk " + args)
    return f"{command} started"


def listingCommands(command):
    with open("Executing/AlexaCando.txt") as _file:
        data = _file.read()
    return str(data)

def result(value1,value2):
    pwd = os.getcwd()
    final=pwd+"\\Executing\\Rantest1.py"+" "+value1+" "+value2
    print(final)
    os.system(final)
    return str(value1+value2)
