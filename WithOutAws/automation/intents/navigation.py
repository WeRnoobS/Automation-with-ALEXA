from flask_ask.models import statement
from flask_ask import question, Ask
from automation import ask,logger
import requests


@ask.intent('AMAZON.HelpIntent')
@ask.launch
def launch() -> question:
    log("launch")
    return question("Welcome").simple_card(title="Welcome to Automation Skill", content="Ask me to open softwares.")

@ask.intent('OpeingNormalPrograms',mapping={'name':'NormalProgram'})
def openNormalPrograms(name)->question:
    log("-->"+name)
    url=requests.get("https://alexa2automation.herokuapp.com/read?id=url").text
    requests.get(url+"/command?command="+name)
    return question("Opening "+name).simple_card(title="Automation Skill",content="{0} opened".format(name))


@ask.default_intent
@ask.intent('AMAZON.FallbackIntent')
@ask.intent('AMAZON.StopIntent')
def endSkill()-> question:
    log(ask.intent)
    return statement("Thanks for Using").simple_card(title="Automation Skill",content="Good bye")

def log(msg: str) -> None:
    logger.debug(msg)
