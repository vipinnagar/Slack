import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler


# Initialize Flask app and Slack app
app = Flask(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
token=os.environ['BOT_TOKEN']
slack_app = App(
    token=token,
    signing_secret=os.environ['SIGNING_SECRET']
)


# Route for handling slash command requests
@app.route("/slack/events", methods=["POST"])
def command():
    print("#######################")
    # Parse request body data
    data = request.form
    print(data)
    # Call the appropriate function based on the slash command
    if data["command"] == "/forward" and data["channel_id"] == os.environ['CHANNEL_1']:
        message = data["text"]
    else:
        message = f"Invalid command: {data['command']}"

    # Return response to Slack
    def send_message_to_target_channel(message):
        slack_api_url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": f"Bearer {token}"}
        channel_id = os.environ['CHANNEL_2']
        data = {
            "channel": channel_id,
            "text": message,
        }
        response = requests.post(slack_api_url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")
    send_message_to_target_channel(message)
    return "Message forwarded."


# Function for getting a random joke from the icanhazdadjoke API
def get_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, timeout=5)
    joke = response.json()["joke"]
    return joke


# Initialize SlackRequestHandler to handle requests from Slack
handler = SlackRequestHandler(slack_app)

if __name__ == "__main__":
    # Start the Flask app on port 5000
    app.run(port=5000, debug=False)
