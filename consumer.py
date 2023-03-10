import json
import os
import threading
import time
import sys
from collections import defaultdict
from datetime import datetime
import logging

from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()
event_topic = os.getenv("event_topic")
TOP_EVENTS = 10
# The 'active object' design pattern is being used

logging.basicConfig(
    level=logging.DEBUG,  # or logging.DEBUG to see more detailed messages
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("./app-logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


class IngKafkaConsumer:
    def __init__(self, topic, server_address):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[server_address],
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id="my-group",
        )
        self.events = []
        self.popular_events = []
        self.venues = defaultdict(int)  # store occurrence of the venues
        self._is_running = False
        self.thread = threading.Thread(target=self.run)

    def start(self):
        self._is_running = True
        self.thread.start()

    def stop(self):
        self._is_running = False
        self.thread.join()

    def run(self):
        while self._is_running:
            for message in self.consumer:
                event = json.loads(message.value)
                self.events.append(event)
                self.venues[event["venue"]["venue_name"]] += 1
                sorted_events = sorted(
                    self.venues.items(), key=lambda x: x[1], reverse=True
                )
                self.popular_events = []
                for venue_name, occurrence in sorted_events[
                    : min(TOP_EVENTS, len(sorted_events))
                ]:
                    for event in self.events:
                        if event["venue"]["venue_name"] == venue_name:
                            self.popular_events.append(
                                (
                                    venue_name,
                                    event["venue"]["lon"],
                                    event["venue"]["lat"],
                                    event["event"]["event_name"],
                                    datetime.fromtimestamp(
                                        event["event"]["time"] / 100
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    occurrence,
                                )
                            )
                            break
            time.sleep(1)

    def get_popular_events(self):
        return self.popular_events
