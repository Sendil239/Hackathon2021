from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sentimentAnalysisProcessor
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    screename,count = body.split("/", 1)
    opMsg = sentimentAnalysisProcessor.tweetAnalyse(screename,count)
    # Start our TwiML response
    resp = MessagingResponse()
    resp.message(opMsg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)