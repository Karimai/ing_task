import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from decimal import Decimal
from json import JSONDecodeError
from typing import Dict, List
from event_generator import event_faker
from dotenv import load_dotenv
from kafka import KafkaProducer
from pydantic import BaseModel, validator

logging.basicConfig(
    level=logging.DEBUG,  # or logging.DEBUG to see more detailed messages
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("./app-logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

load_dotenv()
event_topic = os.getenv("event_topic")


class Venue(BaseModel):
    venue_name: str
    lon: float
    lat: float
    venue_id: int


class Member(BaseModel):
    member_id: int
    photo: str | None
    member_name: str


class Event(BaseModel):
    event_name: str
    event_id: str
    time: int
    event_url: str

    @validator("time")
    def validate_time(cls, value):
        try:
            datetime.fromtimestamp(value / 1000)
            return value
        except Exception:
            raise ValueError("time must be a valid Unix timestamp")


class GroupTopic(BaseModel):
    urlkey: str
    topic_name: str


class Group(BaseModel):
    group_topics: List[GroupTopic]
    group_city: str
    group_country: str
    group_id: int
    group_name: str
    group_lon: float
    group_urlname: str
    group_lat: float


class RSVP(BaseModel):
    venue: Venue
    visibility: str
    response: str
    guests: int
    member: Member
    rsvp_id: int
    mtime: int
    event: Event
    group: Group


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class SampleGenerator:
    def __init__(self, faker: bool = True, source: str = "meetup.json"):
        self.source = source
        self.faker = faker

    def start(self) -> str:
        """
        Generate sample JSON data.

        This function reads JSON-formatted data from a file, decodes it, and
        yields each line of data as a JSON-formatted string. I would prefer using
        Faker package to generate infinite data.

        Yields:
        -------
        A string of JSON-formatted data.
        """
        if self.faker:
            while True:
                try:
                    sample_data: Dict = json.loads(json.dumps(event_faker(), cls=DecimalEncoder))
                except JSONDecodeError as e:
                    logger.warning(f"Error in Decoding JSON (skip one event): {str(e)}")

                # Validate the data using the Pydantic class
                try:
                    RSVP(**sample_data)
                    yield json.dumps(sample_data, cls=DecimalEncoder)
                except Exception as e:
                    logger.error(f"Error: {str(e)}")

        else:
            with open(self.source, "r") as data_fd:
                for line in data_fd.readlines():
                    try:
                        sample_data: Dict = json.loads(line)
                    except JSONDecodeError as e:
                        logger.warning(f"Error in Decoding JSON (skip one event): {str(e)}")
                        continue

                    # Validate the data using the Pydantic class
                    try:
                        RSVP(**sample_data)
                        logger.debug(sample_data["venue"]["venue_name"])
                        yield json.dumps(sample_data, cls=DecimalEncoder)
                    except Exception as e:
                        logger.error(f"Error: {str(e)}")


class EventPublisher:
    def __init__(self, topic: str, bootstrap_servers: str):
        """
        Initialize an EventPublisher object.

        Parameters:
        -----------
        topic : str
            The name of the Kafka topic to publish to.
        bootstrap_servers : str
            The address of Kafka broker.
        """
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    async def publish(self, event: str):
        """
        Publish an event to a Kafka topic.
        Parameters:
        -----------
        event : str
            The JSON-formatted data to publish.
        """
        self.producer.send(self.topic, value=event.encode("utf-8"))

    async def close(self):
        """
        Close the Kafka producer.
        """
        await self.producer.close()


async def run_publisher():
    """
    Run an EventPublisher object to publish sample JSON data to a Kafka topic.
    :return:
    """
    publisher = EventPublisher(
        topic=event_topic, bootstrap_servers=os.getenv("bootstrap_servers")
    )
    sample_generator = SampleGenerator(faker=True, source="meetup.json")
    for event in sample_generator.start():
        logger.info("event published ...")
        await publisher.publish(event)
        await asyncio.sleep(1)
    await publisher.close()
