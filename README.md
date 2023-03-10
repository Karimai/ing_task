* Description:

Receive a continous events from a third-party and return the most top ten events information in a stream manner.

The poetry has been used to handle the virtual environment and the dependencies.

Apachie Kafka framework is used for stream processing. 


### Docker
The project is a multi container application consists of four services:
1. ZooKepper: ZooKeeper is used as the coordination service for the Kafka messaging system. ZooKeeper is a tool for managing and coordinating distributed systems, and it plays a critical role in the reliable operation of systems like Kafka.
2. kafka: It depends on the zookeeper service. Kafka is a distributed streaming platform that is used to build real-time data pipelines and streaming applications.
3. app: It uses the Dockerfile which is present in the current directory to build an image.
4. ing_log: It uses busybox image, which is a lightweight base image. This mounts the ./app-logs on the host to /app/logs directory in the container. It is helpful to have log data in the host system even service goes down. 

### RUN
By running `docker-compos up --build`, four containers should be up and running. By surfing https://127.0.0.1:8000/ you should be able to see "Let's go!" message. For seeing the stream data you should browse http://127.0.0.1:8000/events. every seconds, you should receive one json data which include the most top ten events. Data includes venue name, gro location (lon, lat), event name and event time.


### Publisher
It uses KafkaProducer in order to publish a new events. Ideally, the data should come from a real resources such as meetup. The next best idea can by generate data by It is better to use a data generator such as Faker package. For the sake of simplicity, here we use meetup.json file which includes around 1500 events. Some are not valid since of lacking critical data such as venue name or geo-location information. Since these info are necessary, those won't be considered as a valid data.

### Data Validation
Data validation is done in Publisher. It uses pydantic package internally. Some data should not be critical such as photo field. It is optional. The time stamp also should be valid unix timestamps. All the other fields are considered as critical data.


### code style:
This project uses three tools for checking code style; isort, black, and flake8. Those are also hooks for commit. It is responsibility of the developers to install `pre-commit` locally. In case of any code style issue, it prevents code be committed.

### test:
There some very basic tests in test_main.py, test_main.http, and test_generator.html. For testing test_main.*, one connect to a running app service and run pytest. However, in order to test the test_generator there is no need to connect the app serive and it can be test on the host machine.

