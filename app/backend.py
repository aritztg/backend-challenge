from os import getenv
from typing import Annotated

import uvicorn
from custom_types import Message
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response
from settings import TOPIC_MAPPING

# Load env variables from `.env`.
load_dotenv()

# Define app paths.
INPUT_PATH = '/input/'

# App handler.
app = FastAPI(title='Landbot messages API', description='Message catcher and proxy microservice.')


async def check_token(csrf_token: str) -> bool:
    """Utility function to check CSRF validity against an environment predefined constant."""
    if not csrf_token == getenv('VALID_CSRF_TOKEN'):
        raise HTTPException(status_code=403, detail='Unauthorised. Invalid CSRF Token.')

    return True


@app.post(INPUT_PATH)
async def send_message(csrf_token: Annotated[str, Depends(check_token)],  # pylint: disable=W0613
                       message: Message) -> Response:
    """Main entry point of the backend app mounted as a POST method in /{INPUTPATH} entrypoint.

    It will check first the mandatory CSRF token, and the rest of the input message data (a dict with two keys,
    topic and description, which must be defined as well).
    Finally, it will send the task/user-request to different channels depending on the topic passed. Note that a
    topic could be mapped to multiple channels, so they would be executed sequentially (this could be improved to make
    those async).
    """

    # Clean topic.
    topic_lower = message.topic.lower()

    # Ensure valid topic.
    if topic_lower not in TOPIC_MAPPING:
        raise HTTPException(status_code=400, detail=f'Malformed. Invalid topic "{message.topic}".')

    # Ensure description.
    if not message.description.strip():
        raise HTTPException(status_code=400, detail='Malformed. No description.')

    # Perform operation.
    for channel in TOPIC_MAPPING[topic_lower]:
        channel().send(message)

    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
