# office-hours

A small application that lets you set up a video call and receive an SMS when someone joins the call.

## Setup
- Create [a Twilio account](https://www.twilio.com/referral/D4tqHM).
- In the [Twilio Console](https://console.twilio.com), create a new [phone number](https://console.twilio.com/?frameUrl=/console/phone-numbers/incoming) if you do not already have one.
- [Generate an API Key](https://www.twilio.com/console/project/api-keys).
- Clone this repository.
- Create and activate a virtual environment.
- Create a _.env_ file by copying the _.env.template_ file. Replace the placeholder text with the values for your Twilio Account SID, API Key SID, API Key Secret, and Twilio phone number in [E.164 format](https://www.twilio.com/docs/glossary/what-e164).
- Run `pip install -r requirements.txt` to install dependencies.
- Run `flask run` to start the server locally. To see it running, navigate to http://localhost:5000.
- To create a temporary public URL for your application, install [ngrok](https://ngrok.com/download) and run the command `ngrok http 5000`.
- Once ngrok is running, open one of the URLs next to `Forwarding` in your browser:
```
ngrok by @inconshreveable                                       (Ctrl+C to quit)

Session Status                online
Account                      <YOUR_ACCOUNT_NAME>
Version                       2.3.40
Region                        <YOUR_REGION>
Web Interface                 http://127.0.0.1:4040
Forwarding                    <URL> -> http://localhost:5000
Forwarding                    <URL> -> http://localhost:5000
```
