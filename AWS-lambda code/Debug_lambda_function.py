
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import json
import requests
from Debuger import Log_file
import calendar


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # print("event.session.application.applicationId=" +
    #       event['session']['application']['applicationId'])
    # print(" printing context")
    # print(context)

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent_name)
    # Dispatch to your skill's intent handlers
    if intent_name == "ThingsYouCanDo":
        return list_commands()
    elif intent_name == "ExecutingCommands":
        return sending_command_to_device(intent, session)
    elif intent_name == "WhatsMyCommandIntent":
        return get_command_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "OpeingNormalPrograms":
        return sending_command_to_device(intent, session)
    elif intent_name == "GettingResult":
        return demo(intent, session)
    else:
        print(intent_name)
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    url = getting_device_location()
    session_attributes = {}
    card_title = "Welcome"
    html = requests.get(url)
    speech_output = "Welcome to We R noobs automation feel good to intract with us. "+html.text

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "say , create project or Get results or clean my Desktop"
    should_end_session = False
    result = build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    Log_file.logeer(result)
    return result


def set_command_in_session(intent, session):
    """ Sets the command in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Command' in intent['slots']:
        favorite_command = intent['slots']['Command']['value']
        session_attributes = create_favorite_command_attributes(
            favorite_command)
        html = requests.get(
            'http://example.ngrok.io/command?command='+favorite_command)
        speech_output = "I sent the  command to your system.Let me know if you want me to send another command."
        reprompt_text = "Please tell me the command I should send to your system by saying, " \
                        "Send the shutdown command"
    else:
        speech_output = "I did not understand that. Please try again."
        reprompt_text = "Please tell me the command I should send to your system by saying, " \
                        "Send the shutdown command"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_favorite_command_attributes(favorite_command):
    return {"favoriteCommand": favorite_command}


def get_command_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if "favoriteCommand" in session.get('attributes', {}):
        favorite_command = session['attributes']['favoriteCommand']
        speech_output = "Your last command was " + favorite_command + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your last command was. " \
                        "Please tell me the command I should send to your system by saying, " \
                        "Send the shutdown command"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def list_commands():
    session_attributes = {}
    card_title = "Commands"
    # html = requests.get('http://example.ngrok.io/command?command=working')
    speech_output = "Create project \nDesktop Cleaner \nget Results"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "say , Create project \nDesktop Cleaner \nget Results"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def sending_command_to_device(intent, session):
    url=getting_device_location()
    session_attributes = {}
    
    if 'NormalProgram' in intent['slots'] :
        favorite_command =intent['slots']['NormalProgram']['value']
        card_title =intent['name']
        value=gettingvalueFormintent(intent['slots']['NormalProgram'])
        should_end_session=False
        session_attributes=create_favorite_command_attributes(favorite_command)
        url = getting_device_location_form_tmp()
        html = requests.get(url+"/command?command="+value)
        speech_output=html.text
        reprompt_text="i think it is openend please check it" 
        
    elif 'SingleCommands' in intent['slots']:
        favorite_command =intent['slots']['SingleCommands']['value']
        value=gettingvalueFormintent(intent['slots']['SingleCommands'])
        card_title =intent['name']
        should_end_session=False
        session_attributes=create_favorite_command_attributes(favorite_command)
        print(url)
        html = requests.get(url+"/command?command="+value)
        speech_output='Executing ' +favorite_command
        reprompt_text="i think it is Executed"
    else :
        card_title="error"
        speech_output="unable to process ur request"
        should_end_session=True
    result = build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    Log_file.logeer(result) 
    return result


def demo(intent, session):
    url=getting_device_location()
    passingcommand="result"
    yearwithmonth=""
    Btechyear=""
    Btechsem=""
    finalvalue=""
    examyear=intent['slots']['ExamYear']['value']
    Btechsem=gettingvalueFormintent(intent['slots']['sem'])
    Btechyear=gettingvalueFormintent(intent['slots']['year'])
    eyear=examyear.split("-")[0]
    if eyear=="2019":
        monthabbr=calendar.month_abbr[int(examyear.split("-")[1])]
        if monthabbr=="Nov":
            yearwithmonth=f'"Nov/Dec {eyear}"'
        elif monthabbr=="June" or monthabbr=="Jun":
            yearwithmonth=f'"June/July {eyear}"'
        elif monthabbr=="July"or monthabbr=="Jul":
            yearwithmonth=f'"June/July {eyear}"'
        elif monthabbr=="Dec":
            yearwithmonth=f'"Nov/Dec {eyear}"'
        elif monthabbr==calendar.month_abbr[4]:
            yearwithmonth=f'"April {eyear}"'        
    elif eyear=="2018":
        monthabbr=calendar.month_name[int(examyear.split("-")[1])]
        yearwithmonth=f'"{monthabbr} {eyear}"'
    finalvalue=f'"B.Tech {Btechyear} Year {Btechsem} Semester (R15)"'
    print(finalvalue+" "+yearwithmonth)
    print(yearwithmonth)
    favorite_command ="result"
    card_title =intent['name']
    # print(url+"/dialogcommand?command="+passingcommand+"&args="+arguments)
    html = requests.get(url+"/result?value1="+finalvalue+"&value2="+yearwithmonth)
    should_end_session=False
    speech_output='Executing '+html.text
    # speech_output= finalvalue +" "+yearwithmonth
    reprompt_text="i think it is Executed"
        
    session_attributes=create_favorite_command_attributes(favorite_command)
    result=build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    Log_file.logeer(result)
    return "result"
# --------------- Function for getting location of devcies ----------------------


def getting_device_location():
    url = requests.get("https://alexautomation.herokuapp.com/read?id=url")
    with open('url.txt', 'w') as file:
        file.write(url.text)
    return url.text


def getting_device_location_form_tmp():
    try:
        with open('url.txt', 'r') as file:

            gobal = file.readline()
        if gobal != "":
            # print(gobal)
            return gobal
        else:
            getting_Device_location()
    except:
        print("identifier")
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'WeRnoobs - ' + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def gettingvalueFormintent(intent):
    value = ""
    try:
        for i in intent['resolutions']['resolutionsPerAuthority']:
            a = i['values']
            for i in a:
                value = i['value']['name']
    except Exception as e:
        return "open dropbox"

    return value


test = input()
filename = test+'.json'
print(filename)
with open(filename) as f:
    data = json.load(f)
context = "<__main__.LambdaContext object at 0x7f13445d5ef0>"
# print(data)
lambda_handler(data, context)
