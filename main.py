import json
import subprocess
import os

# imports for env kafka redis
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads
import base64
import json
import os
import redis

load_dotenv()

KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

RECEIVE_TOPIC = 'NEURAL_TALK'
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"


print(f"kafka : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

# Redis initialize
r = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT,
                      password=REDIS_PASSWORD, ssl=True)

# Kafka initialize - To receive img data to process
consumer = KafkaConsumer(
    RECEIVE_TOPIC,
    bootstrap_servers=[f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)

# Kafka initialize - For Sending processed img data further
producer = KafkaProducer(
    bootstrap_servers=[f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

result_dir = "vis/"
result_file = result_dir + "vis.json"

for message in consumer:
    print('xxx--- inside consumer ---xxx')
    print(f"kafka - - : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

    
    message = message.value
    image_id = message['image_id']
    data = message['data']

    # Setting image-id to topic name(container name), so we can know which image it's currently processing
    r.set(RECEIVE_TOPIC, image_id)

    # set image path
    file_path = "images/" + image_id


    with open(file_path, "wb") as fh:
        fh.write(base64.b64decode(data.encode("ascii")))


    os.system("th eval.lua -model model_id1-501-1448236541.t7 -image_folder images -num_images 1")
    with open(result_file) as json_file:
        data = json.load(json_file)
    caption = []
    for items in data:
        caption.append(items["caption"])
    response = {
        'image_id': image_id,
        "captions" : caption,
    }
    os.remove(file_path)
    os.remove(result_dir + "imgs/img1.jpg")
    os.remove(result_file)

    # sending full and text res(without cordinates or probability) to kafka
    producer.send(SEND_TOPIC_FULL, value=response)
    producer.send(SEND_TOPIC_TEXT, value=response)

    producer.flush()


