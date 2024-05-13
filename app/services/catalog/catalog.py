from fastapi import FastAPI, HTTPException, status

from app.services.catalog.database_client import CatalogDatabaseClient, PlantDoesNotExistError
from app.common import catalog_service_port

app = FastAPI(host="localhost", port=catalog_service_port)

client = CatalogDatabaseClient(dbname="postgres",
                               user="postgres",
                               password="987234",
                               host="postgres-catalog",
                               port=5432)


@app.on_event("startup")
async def startup_event():
    client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


@app.get('/catalog')
async def catalog():
    return client.get_all_plants()


@app.get("/catalog/{plant_id}")
async def catalog_by_id(plant_id: int):
    try:
        return client.get_plant_by_id(plant_id)
    except PlantDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant does not exist")
