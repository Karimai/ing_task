import asyncio
import json
import os
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from consumer import IngKafkaConsumer
from publisher import run_publisher

app = FastAPI()
load_dotenv()
venues = defaultdict(int)
topic = os.getenv("event_topic")
events = []
popular_events = []

loop = asyncio.get_event_loop()
loop.create_task(run_publisher())
ing_consumer = IngKafkaConsumer(
    topic=os.getenv("event_topic"), server_address=os.getenv("bootstrap_servers")
)
ing_consumer.start()


@app.get("/events", response_class=JSONResponse)
async def get_events(request: Request):
    """
    Retrieve the most popular events at the top venues.

    This function continuously retrieves events from a `KafkaConsumer`, adds them to a
    list, and keeps track of the most popular  venues based on the number of events
    held there. It then generates  JSON-formatted data for the most popular events at
    the top venues,  and streams that data to the client.

    Returns:
    --------
    A `StreamingResponse` object that streams JSON-formatted data to the client.
    """

    async def generate():
        while True:
            top_events = ing_consumer.get_popular_events()
            # print('in event api endpoint...')
            yield json.dumps(top_events)
            await asyncio.sleep(1)

    return StreamingResponse(generate())


@app.get("/")
async def root():
    return {"message": "Lets go!"}
