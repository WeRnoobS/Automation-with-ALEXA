from flask_ask.models import statement
from flask_ask import question, Ask
from automation import ask, logger
import requests
from os import getenv

url = "http://127.0.0.1:5001"
if getenv('FLASK_DEBUG') == 'development':
    url = requests.get(
        "https://alexa2automation.onrender.com/read?id=url").text


@ask.intent('AMAZON.HelpIntent')
@ask.launch
def launch() -> question:
    log("launch")
    return question("Welcome").simple_card(title="Welcome to Automation Skill", content="Ask me to open softwares.")


@ask.intent('OpeingNormalPrograms', mapping={'name': 'NormalProgram'})
def openNormalPrograms(name) -> question:
    log("-->"+name)
    requests.get(url+"/command?command="+name)
    return question("Opening "+name).simple_card(title="Automation Skill", content="{0} Opened".format(name))


@ask.intent('projectList')
def getProjectList() -> statement:
    log("--> getting project list")
    val = requests.get(url+"/getProjectNames").text
    return question("This is list of projects").simple_card(title="Automation Skill", content=val)


@ask.intent('openProject', mapping={'option': 'option'})
def openProject(option) -> statement:
    log("--> openProject"+option)
    option = requests.get(url+"/openProject?option="+option).text
    if 'Unable' in option:
        return question(option).simple_card(title="Automation Skill", content=option)
    return question("opened "+option).simple_card(title="Automation Skill", content="{0} Opened".format(option))


@ask.default_intent
@ask.intent('AMAZON.FallbackIntent')
@ask.intent('AMAZON.StopIntent')
def endSkill() -> question:
    log(ask.intent)
    return statement("Thanks for Using").simple_card(title="Automation Skill", content="Good bye")


def log(msg: str) -> None:
    logger.debug(msg)
