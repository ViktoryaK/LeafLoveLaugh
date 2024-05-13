import asyncio
import json

from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer
from cassandra_client import CassandraClient

app = FastAPI(host="localhost", port=8085)

loop = asyncio.get_event_loop()

client = CassandraClient(host="cassandra-latest", port=9044, keyspace='lll-comments')

kafka_consumer = AIOKafkaConsumer("reviews", bootstrap_servers=['kafka-server:9092'])


async def consume():
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


@app.get("/latest_service")
async def latest_service():
    result = client.get_reviews()
    reviews = []
    for row in result:
        reviews_dict = {}
        for column in row._fields:
            reviews_dict[column] = getattr(row, column)
        reviews.append(reviews_dict)
    response = {"reviews": reviews}
    return response
