from os import getenv
from typing import Annotated

import uvicorn
from custom_types import Message
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from settings import TOPIC_MAPPING

# Load env variables from `.env`.
load_dotenv()

# Define app paths.
INPUT_PATH = '/input/'

# App handler.
app = FastAPI(title='Landbot messages API', description='Message catcher and proxy microservice.')


async def check_token(csrf_token):
    if not csrf_token == getenv('VALID_CSRF_TOKEN'):
        raise HTTPException(status_code=403, detail='Unauthorised. Invalid CSRF Token.')

    return True


@app.post(INPUT_PATH)
async def send_message(csrf_token: Annotated[str, Depends(check_token)], message: Message):  # pylint: disable=W0613

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

    return {"topic": message.topic, "description": message.description}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
