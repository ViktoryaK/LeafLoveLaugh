import asyncio
import json

from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer

from app.common import latest_service_port
from app.services.latest.database_client import LatestDatabaseClient

app = FastAPI(host="localhost", port=latest_service_port)

loop = asyncio.get_event_loop()

client = LatestDatabaseClient(host="cassandra-latest", port=9042, keyspace='lll_latest_reviews')

kafka_consumer = AIOKafkaConsumer("reviews", bootstrap_servers='kafka-server:9092')


async def consume():
    await kafka_consumer.start()
    try:
        async for msg in kafka_consumer:
            data = json.loads(msg.value.decode('utf-8'))
            client.post_review(data)
    finally:
        await kafka_consumer.stop()


@app.on_event("startup")
async def startup_event():
    client.connect()
    await loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


@app.get("/latest-reviews")
async def get_latest_reviews():
    result = client.get_reviews()
    reviews = []
    for row in result:
        reviews_dict = {}
        for column in row._fields:
            reviews_dict[column] = getattr(row, column)
        reviews.append(reviews_dict)
    return reviews
