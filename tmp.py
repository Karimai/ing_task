import json
from collections import defaultdict

from publisher import start

venues = defaultdict(int)
counter = 0
events = []
for i in start():
    json_i = json.loads(i)
    events.append(json_i)
    venues[json_i["venue"]["venue_name"]] += 1
    sorted_items = sorted(venues.items(), key=lambda x: x[1], reverse=True)
    # time.sleep(1)
    counter += 1
    if counter == 1120:
        print(counter, len(sorted_items))
        print(sorted_items[:10])
