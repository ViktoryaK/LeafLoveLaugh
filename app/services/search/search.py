from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.common import search_service_url
from app.services.search.database_client import SearchDatabaseClient

app = FastAPI(host="localhost", port=search_service_url)

client = SearchDatabaseClient(host='cassandra-search', port=9042, keyspace='lll_search')


@app.on_event("startup")
async def startup_event():
    client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


class SearchData(BaseModel):
    sunlight: str
    moisture: str
    indoor_spread_min: float
    indoor_spread_max: float
    indoor_height_min: float
    indoor_height_max: float
    toxic_dogs: bool
    toxic_cats: bool


@app.get("/search")
async def get_search(data: SearchData):
    print(data)
    result = client.get_tags(data.sunlight, data.moisture, data.indoor_spread_min, data.indoor_spread_max,
                             data.indoor_height_min,
                             data.indoor_height_max, data.toxic_dogs, data.toxic_cats)
    print(result)
    return [{column: getattr(row, column) for column in getattr(row, "_fields")} for row in result]
