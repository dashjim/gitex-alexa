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
user_name_store = {}
customer_number_for_SMS = "971505592712"
customer_numbers = {"Sally": "971566826036", "John": "971505592712"}
SMS_BODY_PIN = '[1234] This is the verification code from Beyond Bank.'
SMS_BODY_VIDEO = 'Change me - I am a video sms body.'


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
    speech_output = "Welcome to Beyond Bank.  Please tell me your User Name."

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome to Beyond Bank.  Please tell me your User Name."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request(sid, number='0', name="no_name"):
    card_title = "Session Ended"
    speech_output = "bye  "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    # Request ED URL
    requestED(sid, number, name)
    # requestPOM(sid)

    try:
        del session_store[sid]
        del phone_number_store[sid]
        del user_name_store[sid]
    except:
        print("ERROR: exception is clear session data.")

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def requestSMS(sms_number='0', body='no_body'):
    conn = http.client.HTTPConnection("94.207.38.203")
    # json.dumps(phone_number_store[sid])
    number = "0"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"family\"\r\n\r\n" \
              "HTTPSendSMS\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; " \
              "name=\"type\"\r\n\r\nHTTP\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"version\"\r\n\r\n1.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition:" \
              " form-data; name=\"eventBody\"\r\n\r\n{\n  \"Phone\":" + sms_number + ",\n  \"Flow\":\"3\",\n\"" \
                                                                                     "Text\":" + body + " \n}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Cache-Control': "no-cache",
        'Postman-Token': "8942795a-cb2a-48a3-817f-89dd549fbffe"
    }

    conn.request("POST", "/services/EventingConnector/events", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    print(res.status)
    print(payload)


def requestED(sid, number="0", user_name="no_name"):
    conn = http.client.HTTPConnection("94.207.38.203")
    # json.dumps(phone_number_store[sid])
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"family\"\r\n\r\n" \
              "GitexAlexa\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"type\"" \
              "\r\n\r\nRestCallEd\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data;" \
              " name=\"version\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
              "form-data; name=\"eventBody\"\r\n\r\n{\"intent\":\"carLoan\", \"lastConversation\":" \
              + json.dumps(session_store[sid]) + ", \"phoneNumber\":" + number + ", \"UserName\":" + user_name + "}" \
                                                                                                                 "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Cache-Control': "no-cache",
        'Postman-Token': "67abf3fb-2b5d-472c-ae2b-63ea37a90df8"
    }

    conn.request("POST", "/services/EventingConnector/events", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    print(res.status)
    print(payload)


def requestPOM(sid):
    conn = http.client.HTTPConnection("1ebf15d3.ngrok.io")

    payload = json.dumps(session_store[sid])
    print("sid: " + sid)
    print(session_store)
    print("payload -  " + payload)

    headers = {
        'Content-Type': "text/plain",
        'Cache-Control': "no-cache",
        'Postman-Token': "728de7fc-958b-4f56-92bd-11cf4b89b6e9"
    }

    conn.request("POST", "/v1/echo", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def get_response_for_car_loan_options_intent(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "For existing Beyond Bank customers we can offer rates from as low as 4.5%.  Would you like to speak to an advisor about your options?  "
    reprompt_text = "For existing Beyond Bank customers we can offer rates from as low as 4.5%.  Would you like to speak to an advisor about your options?  "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_name(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "Thank you.  A 4-digit verification code has been sent to your mobile. Please read out the code."
    reprompt_text = "Thank you.  A 4-digit verification code has been sent to your mobile. Please read out the code."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_code(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "Thank you John.  You are now verified. How can I help? "
    reprompt_text = "Thank you John.  You are now verified. How can I help?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_creator_intent(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "My creator is Ji Jun Xiang. "
    reprompt_text = "Jun Xiang created me. "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_loan_interest_intent(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "The interest rate is ranging from 10% to 15% per year accroding to your previous record. " \
                    "Please tell us your phone number to provid more details for you."
    reprompt_text = "The interest rate is ranging from 10% to 15% per year. Please provide your phone number for us to callback."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def extract_user_name(intent):
    if 'slots' in intent:
        slots = intent['slots']
        for key, val in slots.items():
            if val.get('value'):
                if 'Sally' in (val.get('value')):
                    return 'Sally'
                elif 'John' in (val.get('value')):
                    return 'John'
    return "no_name"


def extract_phone_number(intent):
    if 'slots' in intent:
        slots = intent['slots']
        for key, val in slots.items():
            if val.get('value'):
                if (val.get('value')).isdigit():
                    return val['value'].lower()
    return 0


def get_response_for_number_intent(intent, sid, number="0", name='no_name'):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    speech_output = "Great. An adviser will call your mobile within the next couple of minutes. Thank you."
    reprompt_text = "Great. An adviser will call your mobile within the next couple of minutes. Thank you."

    # requestPOM(sid)
    requestED(sid, number, name)

    try:
        del session_store[sid]
        del phone_number_store[sid]
        del user_name_store[sid]
    except:
        print("ERROR in clear session.")

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_response_for_error_intent(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "Sorry, I cannot understand. "
    reprompt_text = "Sorry, I don't understand. "

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

    sid_ = session['sessionId']
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + sid_)

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print("intent id is: " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        if session_store.get(sid_) is None:
            session_store[sid_] = ["enter skill"]
        else:
            session_store[sid_].append("enter skill")

        return get_welcome_response()

    elif intent_name == "LoanOptions":
        if session_store.get(sid_) is None:
            session_store[sid_] = ["ask for car loan options"]
        else:
            session_store[sid_].append("ask for car loan options")
        return get_response_for_car_loan_options_intent(intent, session)

    elif intent_name == "name":
        if session_store.get(sid_) is None:
            session_store[sid_] = ["enter skill and get user name."]
        else:
            session_store[sid_].append("enter skill and get user name.")

        cust_name = extract_user_name(intent)
        user_name_store[sid_] = cust_name
        session_store[sid_].append(cust_name)
        requestSMS(customer_numbers[cust_name], SMS_BODY_PIN)
        return get_response_for_name(intent, session)

    elif intent_name == "Creator":
        session_store[sid_].append("ask for creator")
        return get_response_for_creator_intent(intent, session)

    elif intent_name == "code":
        session_store[sid_].append("received verification code.")
        return get_response_for_code(intent, session)

    elif intent_name == "LoanInterestRate":
        session_store[sid_].append("ask for loan interest rate")
        return get_response_for_loan_interest_intent(intent, session)

    elif intent_name == "number" or intent_name == "agent":
        session_store[sid_].append("callback to customer ")
        phone_number_store[sid_] = extract_phone_number(intent)

        current_user = user_name_store[sid_]
        print("going to send sms for: " + current_user + ", with - " + SMS_BODY_VIDEO)
        requestSMS(customer_numbers[current_user], SMS_BODY_VIDEO)
        return get_response_for_number_intent(intent, sid_, customer_numbers[current_user], current_user)

    elif intent_name == "AMAZON.FallbackIntent":
        if session_store.get(sid_) is None:
            session_store[sid_] = ["fall back intent"]
        else:
            session_store[sid_].append("fall back intent")
        return get_response_for_error_intent(intent, session)

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        session_store[sid_].append("stop intent - no thanks")
        print("received session end event.")
        current_user = user_name_store[sid_]
        print("going to send sms for: " + current_user + ", with - " + SMS_BODY_VIDEO)
        requestSMS(customer_numbers[current_user], SMS_BODY_VIDEO)
        return handle_session_end_request(sid_, customer_numbers[current_user], current_user)
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
