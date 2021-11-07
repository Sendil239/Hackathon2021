import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = '########################'
auth_token = '###############'
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
         messaging_service_sid='###############',
         body=body,
         to='+###############'
     )


print(message.sid)
