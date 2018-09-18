"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import http.client
import json

# --------------- Helpers that build all of the responses ----------------------
session_store = {}
phone_number_store = {}

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Gitex Bank. " \
                    "What can I help? "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome to Gitex Bank, " \
                    "Do you need car loan?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request( sid ):
    card_title = "Session Ended"
    speech_output = "Thank you for using our service. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    # Request ED URL
    requestED(sid)

    del session_store[sid]

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def requestED( sid ):

    conn = http.client.HTTPConnection("135.27.132.224")

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"family\"\r\n\r\nGitexAlexa\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\nRestCallEd\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"version\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"eventBody\"\r\n\r\n{carLoan:{intent:\"carLoan\", lastConversation:\""+ session_store[sid] +"\", phoneNumber:\""+ phone_number_store[sid] +"\", UserName:\"Jim Test\"}}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Postman-Token': "67abf3fb-2b5d-472c-ae2b-63ea37a90df8"
        }

    conn.request("POST", "/services/EventingConnector/events", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def get_response_for_car_loan_options_intent(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "We provid car loans for different time period. " \
                    "From 6 months to 3 years. " \
                    "Do you want to know more details?"
    reprompt_text = "We have car loans from 6 months to 3 years. " \

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_creator_intent(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "My creator is Ji Jun Xiang. "
    reprompt_text = "Jun Xiang created me. " \

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_loan_interest_intent(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "The interest rate is ranging from 5% to 8% per year accroding to your previous record. " \
                    "Please tell us your phone number to provid more deatils for you."
    reprompt_text = "The interest rate is ranging from 10% to 15% per year. Please provide your phone number for us to callback."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def extract_phone_number(intent):
    if 'slots' in intent:
        slots = intent['slots']
        for key, val in slots.items():
            if val.get('value'):
                if (val.get('value')).isdigit():
                    return int(val['value'].lower())
    return 0


def get_response_for_number_intent(intent):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    speech_output = "Thank you for providing the phone number. We will contact you ASAP."
    reprompt_text = "We received your phone number, and will contact you now. "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_error_intent(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "Sorry, I cannot understand. "
    reprompt_text = "Sorry, I don't understand. " \

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

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

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        session_store[session['sessionId']] = ["enter skill"]
        return get_welcome_response()
    elif intent_name == "LoanOptions":
        session_store[session['sessionId']].append("ask for car loan options")
        return get_response_for_car_loan_options_intent(intent, session)
    elif intent_name == "Creator":
        session_store[session['sessionId']].append("ask for creator")
        return get_response_for_creator_intent(intent, session)
    elif intent_name == "LoanInterestRate":
        session_store[session['sessionId']].append("ask for loan interest rate")
        return get_response_for_loan_interest_intent(intent, session)
    elif intent_name == "number":
        session_store[session['sessionId']].append("customer phone number is: " + extract_phone_number(intent) )
        phone_number_store[session['sessionId']] = extract_phone_number(intent)
        return get_response_for_number_intent(intent)
    elif intent_name == "AMAZON.FallbackIntent":
        session_store[session['sessionId']].append("fall back intent")
        return get_response_for_error_intent(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        session_store[session['sessionId']].append("stop intent")
        return handle_session_end_request(session['sessionId'])
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    print(event)
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

