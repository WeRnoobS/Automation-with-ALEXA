import os
import os.path
import configparser


class ExecutingCommands:
    __instance = None

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.foldernames = {}
        self.currentpath = config['DEFAULT']['ProjectPath']

    @staticmethod
    def getInstance():
        if ExecutingCommands.__instance == None:
            ExecutingCommands.__instance = ExecutingCommands()
        return ExecutingCommands.__instance

    def handle_Commands(self, command):
        # -----opeing file to check the where it suppoerts are not-----#
        with open("Executing//WindowsApps.txt", "r") as _file:
            _WindowsApps = _file.read()
        with open("Executing//automatoins.txt") as _file:
            _automation = _file.read()

        # -----Main function-----#
        if command in _WindowsApps:
            os.popen(command)
        elif command in _automation:
            print(command)
            return self.automation(command)
        elif command == "getcommands":
            return self.listingCommands(command)
        else:
            return "command not found"
        return "opening "+command

    def automation(self, command):
        pwd = os.getcwd()
        os.popen(pwd+"\\Executing\\"+command+".lnk")
        return f"{command} started"

    def DialogCommand(self, command, args):
        pwd = os.getcwd()
        os.popen(pwd+"\\Executing\\"+command+".lnk " + args)
        return f"{command} started"

    def listingCommands(self, command):
        with open("Executing/AlexaCando.txt") as _file:
            data = _file.read()
        return str(data)

    def result(self, value1, value2):
        pwd = os.getcwd()
        final = pwd+"\\Executing\\Rantest1.py"+" "+value1+" "+value2
        print(final)
        os.system(final)
        return str(value1+value2)

    def getProjectNames(self):

        dirs = os.listdir(self.currentpath)
        folderNames = ''
        self.foldernames = {}
        val = 1
        for i in dirs:
            if "." not in i:
                self.foldernames[val] = i
                folderNames += f"{val}. {i} \n"
                val = val+1
        folderNames += "Choose any one option and say open option"
        return folderNames

    def openProject(self, value):
        if len(self.foldernames.keys()) != 0:
            folderName = self.foldernames[value]
            os.popen(f"code {self.currentpath}\\{folderName}")
            return folderName
        else:
            return "Unable to Find Folder or Project Folder is Empty"
