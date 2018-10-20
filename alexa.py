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
customer_numbers = {"Sara": "971505592712", "Peter": "971561086668", "Venky": "917420818954", "Kuntal": "919810496569"}
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

def get_user_name_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "name please"
    speech_output = "Do not have that user.  Please tell me your User Name."

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Do not have that user.  Please tell me your User Name."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_thank_you_call_back(sid, number='0', name="no_name"):
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


def handle_session_end_request(sid, number='0', name="no_name"):
    card_title = "Session Ended"
    speech_output = "bye  "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    # Request ED URL
    # requestED(sid, number, name)
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
              " form-data; name=\"eventBody\"\r\n\r\n{\n  \"Phone\":\"" + sms_number + "\",\n  \"Flow\":\"3\",\n\"" \
                                                                                     "Text\":\"" + body + "\" \n}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"

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
              + json.dumps(session_store[sid]) + ", \"phoneNumber\":\"" + number + "\", \"UserName\":\"" + user_name + "\"}" \
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

    speech_output = "Thank you " + user_name_store[session['sessionId']] + ".  You are now verified. How can I help? "
    reprompt_text = "Thank you " + user_name_store[session['sessionId']] + ".  You are now verified. How can I help?"

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
                if 'Sara' in (val.get('value')) or 'sara' in (val.get('value')):
                    return 'Sara'
                elif 'Peter' in (val.get('value')) or 'peter' in (val.get('value')):
                    return 'Peter'
                elif 'Venky' in (val.get('value')) or 'venky' in (val.get('value')):
                    return 'Venky'
                elif 'Kuntal' in (val.get('value')) or 'kuntal' in (val.get('value')):
                    return 'Kuntal'
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
        if cust_name not in customer_numbers:
            return get_user_name_response()
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
        # print("going to send sms for: " + current_user + ", with - " + SMS_BODY_VIDEO)
        # requestSMS(customer_numbers[current_user], SMS_BODY_VIDEO)
        return get_response_for_number_intent(intent, sid_, customer_numbers[current_user], current_user)

    elif intent_name == "AMAZON.FallbackIntent":
        if session_store.get(sid_) is None:
            session_store[sid_] = ["fall back intent"]
        else:
            session_store[sid_].append("fall back intent")
        return get_response_for_error_intent(intent, session)

    elif intent_name == "thank_you_call_back":
        session_store[sid_].append(" thank you and callback intent")
        print("received session end event.")
        current_user = user_name_store[sid_]
        # print("going to send sms for: " + current_user + ", with - " + SMS_BODY_VIDEO)
        # requestSMS(customer_numbers[current_user], SMS_BODY_VIDEO)
        return handle_thank_you_call_back(sid_, customer_numbers[current_user], current_user)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        session_store[sid_].append("stop intent")
        print("received session end event.")
        current_user = user_name_store[sid_]
        # print("going to send sms for: " + current_user + ", with - " + SMS_BODY_VIDEO)
        # requestSMS(customer_numbers[current_user], SMS_BODY_VIDEO)
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


def main():
    e = {'version': '1.0', 'session': {'new': False, 'sessionId': 'amzn1.echo-api.session.c26228a1-58fe-4af4-8de5-9b2d473514b4', 'application': {'applicationId': 'amzn1.ask.skill.99387f0a-7c0c-4958-9e6b-958d00e35e03'}, 'user': {'userId': 'amzn1.ask.account.AE4ZM7LSTJ2DDGGGHVHHWIRDAM6USZIYN4B4F76VQIMEDZVLP23YDPGM7AMUYANKUCYITWERERQBA2XJDKMICZFYPJYAZ6WHFQIQDBI7EMAYUIKJ5E5IBM4NBMAZVK6LYA567D5GLSQMHGU7FUF6IZUWER52ERK2HRZVKXPJBJFUVTLETQQEAHOSQ5LCLPNKZA2AVS6OVWNKFQA'}}, 'context': {'System': {'application': {'applicationId': 'amzn1.ask.skill.99387f0a-7c0c-4958-9e6b-958d00e35e03'}, 'user': {'userId': 'amzn1.ask.account.AE4ZM7LSTJ2DDGGGHVHHWIRDAM6USZIYN4B4F76VQIMEDZVLP23YDPGM7AMUYANKUCYITWERERQBA2XJDKMICZFYPJYAZ6WHFQIQDBI7EMAYUIKJ5E5IBM4NBMAZVK6LYA567D5GLSQMHGU7FUF6IZUWER52ERK2HRZVKXPJBJFUVTLETQQEAHOSQ5LCLPNKZA2AVS6OVWNKFQA'}, 'device': {'deviceId': 'amzn1.ask.device.AEVLHZKFCP2JKA5652BP7BBWM24747OKUXZIP32VRBSMTERUNTNGXQ47GLI4X3XGORQ7K5BRLJZHW25BW46DGLZ3OQ3YMVHZTT55FBMOWMOZTBV6FOZRQTPRRJOKCYDF54OWARVTNV5F2TQAWREI2FO5XTNWATUHS66KSMJTA6K5D42H67GNC', 'supportedInterfaces': {}}, 'apiEndpoint': 'https://api.amazonalexa.com', 'apiAccessToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjk5Mzg3ZjBhLTdjMGMtNDk1OC05ZTZiLTk1OGQwMGUzNWUwMyIsImV4cCI6MTUzODczMzI4MiwiaWF0IjoxNTM4NzI5NjgyLCJuYmYiOjE1Mzg3Mjk2ODIsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUVWTEhaS0ZDUDJKS0E1NjUyQlA3QkJXTTI0NzQ3T0tVWFpJUDMyVlJCU01URVJVTlROR1hRNDdHTEk0WDNYR09SUTdLNUJSTEpaSFcyNUJXNDZER0xaM09RM1lNVkhaVFQ1NUZCTU9XTU9aVEJWNkZPWlJRVFBSUkpPS0NZREY1NE9XQVJWVE5WNUYyVFFBV1JFSTJGTzVYVE5XQVRVSFM2NktTTUpUQTZLNUQ0Mkg2N0dOQyIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFFNFpNN0xTVEoyRERHR0dIVkhIV0lSREFNNlVTWklZTjRCNEY3NlZRSU1FRFpWTFAyM1lEUEdNN0FNVVlBTktVQ1lJVFdFUkVSUUJBMlhKREtNSUNaRllQSllBWjZXSEZRSVFEQkk3RU1BWVVJS0o1RTVJQk00TkJNQVpWSzZMWUE1NjdENUdMU1FNSEdVN0ZVRjZJWlVXRVI1MkVSSzJIUlpWS1hQSkJKRlVWVExFVFFRRUFIT1NRNUxDTFBOS1pBMkFWUzZPVldOS0ZRQSJ9fQ.g_ZkPbiHNXx0QdyaokgLoSOepKfow-7tDjCaCBh3ug22cbj7GAZc8HlK2PvCPi7xGELG6jK8mGopjV_4l3v_cGj3-AXn8KCAV0_v8ZHVNeOMURhp6SRSrt5JGMNhCHEl03IsAXZYfZsGYK3cqy9NmyC-En1NH5iuleye78QBUFBxz1V3X2QsR501s9nMCDhfysZpkmueyz76WfOW0X1ZmN52OutkwLlLy2nUDuQlYqMjghoRxpqOQRlV0sqUBI4Jscnm_riaejjLdY2Dam_AMPUWk5ONjY7g_K4Q_T6ovmFJ3E1J9ULMQ15Kx3o10_cHNCAVjaTAiCFA4Jsq9q7DgQ'}}, 'request': {'type': 'IntentRequest', 'requestId': 'amzn1.echo-api.request.f54888af-0058-4843-9f03-d33f9b6da5e9', 'timestamp': '2018-10-05T08:54:42Z', 'locale': 'en-US', 'intent': {'name': 'name', 'confirmationStatus': 'NONE', 'slots': {'humanName': {'name': 'humanName', 'value': 'sally', 'resolutions': {'resolutionsPerAuthority': [{'authority': 'amzn1.er-authority.echo-sdk.amzn1.ask.skill.99387f0a-7c0c-4958-9e6b-958d00e35e03.AMAZON.US_FIRST_NAME', 'status': {'code': 'ER_SUCCESS_MATCH'}, 'values': [{'value': {'name': 'Sally', 'id': '3fa8b9cc38915ca488e412b59a8aaa79'}}, {'value': {'name': 'Sally S', 'id': '0144aea78a8beea0953087d9d0ca08a0'}}, {'value': {'name': 'Sally S.', 'id': 'd9076509281d4194b47e513d3d2d1ede'}}]}]}, 'confirmationStatus': 'NONE'}}}}}
    e_peter = {'version': '1.0', 'session': {'new': False, 'sessionId': 'amzn1.echo-api.session.a762598c-2a29-40b7-a88f-e06430527b9b', 'application': {'applicationId': 'amzn1.ask.skill.99387f0a-7c0c-4958-9e6b-958d00e35e03'}, 'user': {'userId': 'amzn1.ask.account.AE4ZM7LSTJ2DDGGGHVHHWIRDAM6USZIYN4B4F76VQIMEDZVLP23YDPGM7AMUYANKUCYITWERERQBA2XJDKMICZFYPJYAZ6WHFQIQDBI7EMAYUIKJ5E5IBM4NBMAZVK6LYA567D5GLSQMHGU7FUF6IZUWER52ERK2HRZVKXPJBJFUVTLETQQEAHOSQ5LCLPNKZA2AVS6OVWNKFQA'}}, 'context': {'System': {'application': {'applicationId': 'amzn1.ask.skill.99387f0a-7c0c-4958-9e6b-958d00e35e03'}, 'user': {'userId': 'amzn1.ask.account.AE4ZM7LSTJ2DDGGGHVHHWIRDAM6USZIYN4B4F76VQIMEDZVLP23YDPGM7AMUYANKUCYITWERERQBA2XJDKMICZFYPJYAZ6WHFQIQDBI7EMAYUIKJ5E5IBM4NBMAZVK6LYA567D5GLSQMHGU7FUF6IZUWER52ERK2HRZVKXPJBJFUVTLETQQEAHOSQ5LCLPNKZA2AVS6OVWNKFQA'}, 'device': {'deviceId': 'amzn1.ask.device.AEVLHZKFCP2JKA5652BP7BBWM24747OKUXZIP32VRBSMTERUNTNGXQ47GLI4X3XGORQ7K5BRLJZHW25BW46DGLZ3OQ3YMVHZTT55FBMOWMOZTBV6FOZRQTPRRJOKCYDF54OWARVTNV5F2TQAWREI2FO5XTNWATUHS66KSMJTA6K5D42H67GNC', 'supportedInterfaces': {}}, 'apiEndpoint': 'https://api.amazonalexa.com', 'apiAccessToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjk5Mzg3ZjBhLTdjMGMtNDk1OC05ZTZiLTk1OGQwMGUzNWUwMyIsImV4cCI6MTUzODc0NzE1MiwiaWF0IjoxNTM4NzQzNTUyLCJuYmYiOjE1Mzg3NDM1NTIsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUVWTEhaS0ZDUDJKS0E1NjUyQlA3QkJXTTI0NzQ3T0tVWFpJUDMyVlJCU01URVJVTlROR1hRNDdHTEk0WDNYR09SUTdLNUJSTEpaSFcyNUJXNDZER0xaM09RM1lNVkhaVFQ1NUZCTU9XTU9aVEJWNkZPWlJRVFBSUkpPS0NZREY1NE9XQVJWVE5WNUYyVFFBV1JFSTJGTzVYVE5XQVRVSFM2NktTTUpUQTZLNUQ0Mkg2N0dOQyIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFFNFpNN0xTVEoyRERHR0dIVkhIV0lSREFNNlVTWklZTjRCNEY3NlZRSU1FRFpWTFAyM1lEUEdNN0FNVVlBTktVQ1lJVFdFUkVSUUJBMlhKREtNSUNaRllQSllBWjZXSEZRSVFEQkk3RU1BWVVJS0o1RTVJQk00TkJNQVpWSzZMWUE1NjdENUdMU1FNSEdVN0ZVRjZJWlVXRVI1MkVSSzJIUlpWS1hQSkJKRlVWVExFVFFRRUFIT1NRNUxDTFBOS1pBMkFWUzZPVldOS0ZRQSJ9fQ.W8lC0ntUDvZ9J1XY2UBiDlijDNoqDDV0bVkfxOeayjnDlgbgWbKbwikMzJ2h-9eEhMdGUWNiHIyf8wlEkZq4jGv1jyIBLWEIuRZWO52JLRQGF2H6Z8EbX5uUFAho49iMW663nemmzCV6LNjZ7QXUfzLAWNZdT4Z1ym3IuOvv_iTCs4Ugv-FZz9wTL-OWZbWmrNkVdmiBO5QVOKNbkGjBk7fnB-sFqfRBvH5YmswxM6qb-7uHDzb-vudF-kg126T-X32I1T9PuTnQ8SNCtquU8R-h9OZHUuj1Z74bJzmdg26D5Z_YR26syrLNydq6LGtlizNRERrMGaRJSghd8BPimw'}}, 'request': {'type': 'IntentRequest', 'requestId': 'amzn1.echo-api.request.d336c203-cac3-4943-9870-ffff8391cf90', 'timestamp': '2018-10-05T12:45:52Z', 'locale': 'en-US', 'intent': {'name': 'name', 'confirmationStatus': 'NONE', 'slots': {'humanName': {'name': 'humanName', 'value': 'peter pan', 'resolutions': {'resolutionsPerAuthority': [{'authority': 'amzn1.er-authority.echo-sdk.amzn1.ask.skill.99387f0a-7c0c-4958-9e6b-958d00e35e03.AMAZON.US_FIRST_NAME', 'status': {'code': 'ER_SUCCESS_MATCH'}, 'values': [{'value': {'name': 'Peter Pan', 'id': 'b1f7e8c5c5d12670675975e769ec11b9'}}]}]}, 'confirmationStatus': 'NONE'}}}}}
    lambda_handler(e_peter, None)


if __name__ == "__main__":
    main()
