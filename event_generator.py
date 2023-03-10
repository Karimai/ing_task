import json
from datetime import datetime
# from publisher import DecimalEncoder
from faker import Faker
import random

fake = Faker()

companies = ["Acme Inc.", "Globex Corporation", "Soylent Industries", "Initech", "Umbrella Corporation",
             "Wonka Industries", "Stark Industries", "Wayne Enterprises", "Oscorp Industries",
             "Weyland-Yutani Corporation", "Cyberdyne Systems", "Aperture Science", "Black Mesa",
             "Vault-Tec Corporation", "Abstergo Industries", "Encom International", "Tyrell Corporation",
             "Massive Dynamic", "Blue Sun Corporation", "Sirius Cybernetics Corporation", "Hooli", "Monarch Sciences",
             "Bluth Company", "Strickland Propane", "Virtucon", "Spacely Space Sprockets", "Rich Industries",
             "Dunder Mifflin", "Prestige Worldwide", "Oceanic Airlines", "Krusty Krab", "Planet Express", "Buy N Large",
             "Wernham Hogg Paper Merchants", "Los Pollos Hermanos", "Mega Corp", "Rekall", "SPECTRE", "Dr. Evil Inc.",
             "FrobozzCo International", "Gekko & Co.", "Tessier-Ashpool SA", "Faber College", "Zorg Industries",
             "Gringotts Wizarding Bank", "C.H.U.D. Industries", "Thompson and Thomson", "J.P. Grosse & Co.",
             "Globo-Chem", "The Sopranos Waste Management"]


def event_faker():
    venue = {
        "venue_name": random.choice(companies),
        "lon": fake.longitude(),
        "lat": fake.latitude(),
        "venue_id": fake.random_number(digits=8)
    }
    member = {
        "member_id": fake.random_number(digits=9),
        "photo": fake.image_url(),
        "member_name": fake.name()
    }
    event = {
        "event_name": fake.sentence(),
        "event_id": fake.random_number(digits=9),
        "time": int(datetime.timestamp(datetime.combine(fake.future_date(), fake.time_object())) * 1000),
        "event_url": fake.uri()
    }
    group_topics = [
        {"urlkey": fake.word(), "topic_name": fake.sentence()} for _ in range(random.randint(1, 5))
    ]
    group = {
        "group_topics": group_topics,
        "group_city": fake.city(),
        "group_country": fake.country_code(),
        "group_id": fake.random_number(digits=8),
        "group_name": fake.sentence(),
        "group_lon": fake.longitude(),
        "group_urlname": fake.word(),
        "group_lat": fake.latitude()
    }
    data = {
        "venue": venue,
        "visibility": fake.word(),
        "response": fake.word(),
        "guests": fake.random_number(digits=2),
        "member": member,
        "rsvp_id": fake.random_number(digits=10),
        "mtime": int(datetime.timestamp(datetime.combine(fake.future_date(), fake.time_object())) * 1000),
        "event": event,
        "group": group
    }
    return data


if __name__ == '__main__':
    print(event_faker())
