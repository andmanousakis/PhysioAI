import sys
import typer
from message.data import transform_features_py  # noqa
from message.data import transform_features_sql  # noqa
from message.data import get_features

from message.model import ChatModel, OpenAIKeys
from message.config import get_settings
from prompts.prompts import get_system_prompt, get_user_prompt

# Initialize chat model.
chat_model = ChatModel()

# Initialize settings.
app = typer.Typer()

# 
@app.command()
def transform():

    try:

        # Uncomment the function you want to run
        transform_features_sql()
        # transform_features_py()

        return
    
    except Exception as e:

        print(f"An error occurred: {e}")
        raise typer.Exit(code=1)

#
@app.command()
def get_message(session_group: str) -> str:

    """
    Generates a personalized message based on the session features
    for a given session group.
    """

    features = get_features(session_group=session_group)  # noqa

    ###### YOUR CODE HERE ######

    if not features:
        print("No features found for the given session_group.")
        raise typer.Exit(code=1)
    
    features = features[0]  # get the first dict record


    response = chat_model.get_completion(
        temperature=0.7,
        model="gpt-4-turbo-preview",
        messages=[
            {OpenAIKeys.ROLE: "system", OpenAIKeys.CONTENT: get_system_prompt()},
            {OpenAIKeys.ROLE: "user", OpenAIKeys.CONTENT: get_user_prompt(features)},
        ],
    )

    print(response)
    return response    

