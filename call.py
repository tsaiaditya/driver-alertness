from twilio.rest import Client
from flask import Response
import time

def call(message, to=''):#Put ur phone number here
    xml = "<?xml version='1.0' encoding='UTF-8'?><Response>\n\t<Say voice='alice'>"+ message +"</Say>\n</Response>"  
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC0b500d773dae941d552ed27de46cf919'#put ur account_sid
    auth_token = 'bd5dbc5c61f7e88fa958ff663277da04'#put ur auth_token
    client = Client(account_sid, auth_token)

    msg = client.messages.create(
        to=to,
        from_='+12075187477',
        body=message
    )
    print(msg)

    print(Response(xml, mimetype='text/xml'))
    call = client.calls.create(
                            url='https://twilio.com/docs/demo.xml',
                            to=to,
                            from_='+12075187477'
                        )
    print(call.sid)

if __name__ == '__main__':
    call('meh')
