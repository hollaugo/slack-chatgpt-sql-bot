import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# Connect to the Chinook database
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# Initialize the OpenAI model with a set temperature
llm = OpenAI(temperature=0)

# Create a database chain with the OpenAI model and database
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, top_k=3)

# Initialize the Slack App with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Set up an event listener for all incoming messages
@app.message("")
def message_all(message, say):
    # Process the incoming message text through the database chain
    result = db_chain.run(message['text'])
    print(message['text'])
    # Respond with the result
    say(result)

# Kick off the Socket Mode handler
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
