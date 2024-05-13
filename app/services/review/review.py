import json
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import FastAPI
from kafka import KafkaProducer
from app.services.review.database_client import ReviewDatabaseClient

from app.common import review_service_url

app = FastAPI(host="localhost", port=review_service_url)

client = ReviewDatabaseClient(host='cassandra-review', port=9042, keyspace='lll_review')

kafka_producer = KafkaProducer(bootstrap_servers=['kafka-server:9092'])


@app.on_event("startup")
async def startup_event():
    client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


@app.get("/reviews/{plant_id}")
async def get_reviews(plant_id: int):
    result = client.get_reviews_for_plant(plant_id)
    reviews = []
    for row in result:
        print(1, row)
        reviews_dict = {}
        for column in row._fields:
            reviews_dict[column] = getattr(row, column)
        reviews.append(reviews_dict)
    return reviews


@app.post("/review/{plant_id}")
async def post_review(plant_id: int, user_id: UUID, user_name: str, review: str):
    review_id = uuid4()
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    values = [review_id, plant_id, review, date, user_id, user_name]
    client.post_review(values)
    data = {
        "plant_id": plant_id,
        "user_id": str(user_id),
        "review_id": str(review_id),
        "user_name": user_name,
        "review": review,
        "date": date,
    }

    kafka_producer.send("reviews", json.dumps(data).encode('utf-8'))
