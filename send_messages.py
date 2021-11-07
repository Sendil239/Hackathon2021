import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC718febdc00d4c9c4486c34d05e0f401e'
auth_token = '4275c9119ceb81403246d3366353f2ac'
client = Client(account_sid, auth_token)

body = "Hello World!"
# message = client.messages \
#                 .create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+15306257808',
#                      to='+17162755453'
#                  )

message = client.messages \
    .create(
         messaging_service_sid='MGc9d8086c0fc0491253c647e0ec818544',
         body=body,
         to='+17162755453'
     )


print(message.sid)
