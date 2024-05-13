from fastapi import FastAPI

from app.common import search_service_url
from database_client import SearchDatabaseClient

app = FastAPI(host="localhost", port=search_service_url)

client = SearchDatabaseClient(host='cassandra-search', port=9044, keyspace='lll_search')


@app.on_event("startup")
async def startup_event():
    client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


@app.get("/search_service")
async def get_search(sunlight: str = None, moisture: str = None, indoor_spread_min: float = 0,
                     indoor_spread_max: float = 100, indoor_height_min: float = 0,
                     indoor_height_max: float = 100, toxic_dogs: bool = False, toxic_cats: bool = False):
    result = client.get_tags(sunlight, moisture, indoor_spread_min, indoor_spread_max, indoor_height_min,
                             indoor_height_max, toxic_dogs, toxic_cats)
    return [{column: getattr(row, column) for column in getattr(row, "_fields")} for row in result]
