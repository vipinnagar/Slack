import logging
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Initialize Flask app and Slack app
app = Flask(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
token = os.environ['BOT_TOKEN']
slack_app = App(
    token=token,
    signing_secret=os.environ['SIGNING_SECRET']
)


# Route for handling slash command requests
@app.route("/slack/events", methods=["POST"])
def command():
    # Parse request body data
    data = request.form
    # Call the appropriate function based on the slash command and channel
    if data["command"] == "/forward" and data["channel_id"] == os.environ["CHANNEL_1"]:
        text = data["text"]
    else:
        text = f"Invalid command: {data['command']} or not the correct channel"

    # Return response to channel-2
    def send_message_to_target_channel(message):
        slack_api_url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": f"Bearer {token}"}
        channel_id = os.environ['CHANNEL_2']
        new_data = {
            "channel": channel_id,
            "text": message,
        }
        response = requests.post(slack_api_url, headers=headers, json=new_data)
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")
        else:
            logging.info(f"Sent message: {response.text}")

    send_message_to_target_channel(text)
    return f"Message forwarded {text}"


# Initialize SlackRequestHandler to handle requests from Slack
handler = SlackRequestHandler(slack_app)

if __name__ == "__main__":
    # Starting the Flask app on port 5000
    logging.info("Server starting at http://127.0.0.1:5000")
    app.run(port=5000, debug=True)

