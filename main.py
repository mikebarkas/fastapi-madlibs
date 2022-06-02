import asyncio
import time

import requests
from fastapi import FastAPI, HTTPException, status
from httpx import AsyncClient

app = FastAPI()

URL = 'https://reminiscent-steady-albertosaurus.glitch.me/'
template = 'It was a {adjective} day. I went downstairs to see if I could {verb} dinner. I asked, "Does the stew need fresh {noun}?"'
response_error = 'A required data source was not available'


async def request(client: AsyncClient, speech: str):
    return await client.get(URL + speech)


async def task():
    async with AsyncClient() as client:
        return {i: await request(client, i) for i in ['noun', 'verb', 'adjective']}
        # speech_parts = {'noun': '', 'verb': '', 'adjective': ''}
        # for item in speech_parts:
        #     speech_parts[item] = await request(client, item)
        # return speech_parts


@app.get('/v1/madlibs')
def madlib():
    start = time.time()

    noun = requests.get(URL + 'noun')
    if noun.status_code != 200:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=response_error)
    noun = noun.text.replace('"', '')
    verb = requests.get(URL + 'verb')
    if verb.status_code != 200:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=response_error)
    verb = verb.text.replace('"', '')
    adjective = requests.get(URL + 'adjective')
    if adjective.status_code != 200:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=response_error)
    adjective = adjective.text.replace('"', '')

    stop = time.time()

    sentence = template.format(
        adjective=adjective,
        verb=verb,
        noun=noun
    )
    duration = stop - start
    return {
        'status': 'success',
        'data': {'message': sentence},
        'response_time': float(f'{duration:.6f}')
        # 'response_time': duration
    }


@app.get('/v2/madlibs')
async def madlibs():

    start = time.time()
    # Create a task group for getting dependency requirements.
    tasks = asyncio.create_task(task())
    speech = await tasks
    stop = time.time()

    # Check each response for errors.
    for item in speech.items():
        if item[1].is_error:
            # return HTTP exception
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=response_error
            )

    sentence = template.format(
        adjective=speech['adjective'].text.replace('"', ''),
        verb=speech['verb'].text.replace('"', ''),
        noun=speech['noun'].text.replace('"', '')
    )
    duration = stop - start
    return {
        'status': 'success',
        'data': {'message': sentence},
        'response_time': float(f'{duration:.6f}')
        # 'response_time': duration
    }


@app.get("/")
async def root():
    return {"message": "Hello World", "status": "success"}
