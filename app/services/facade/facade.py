from typing import Annotated, Optional

from fastapi import FastAPI, Request, HTTPException, Form
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.common import catalog_service_url, review_service_url, search_service_url1, \
    facade_service_port, latest_service_url, search_service_url2

app = FastAPI(host="localhost", port=facade_service_port)
templates = Jinja2Templates(directory="app/services/facade/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    response = requests.get(f'{catalog_service_url}/catalog')

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return templates.TemplateResponse("catalog.html", {"request": request, "catalog": response.json()})


@app.get("/catalog/{plant_id}", response_class=HTMLResponse)
async def get_plant_by_id(request: Request, plant_id: int = 0):
    response = requests.get(f'{catalog_service_url}/catalog/{plant_id}')

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response_comments = requests.get(f'{review_service_url}/reviews/{plant_id}')

    return templates.TemplateResponse("plant.html", {"request": request, "plant": response.json(),
                                                     "comments": response_comments.json()})


@app.post("/catalog/{plant_id}")
async def create_review(plant_id: int, user_name: Annotated[str, Form()], review: Annotated[str, Form()]):
    response = requests.post(f"{review_service_url}/review/{plant_id}",
                             json={"user_name": user_name, "review": review},
                             headers={'Content-Type': 'application/json'})

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"status": "ok", "message": "Review created successfully"}


@app.get("/latest-reviews", response_class=HTMLResponse)
async def get_latest_reviews(request: Request):
    response = requests.get(f"{latest_service_url}/latest-reviews")

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    reviews = [{"user": review["user_name"],
                "plant": requests.get(f"{catalog_service_url}/catalog/{review['plant_id']}").json(),
                "text": review["review"]}
               for review in response.json()]
    return templates.TemplateResponse("latest_reviews.html", {"request": request, "reviews": reviews})


@app.get("/search", response_class=HTMLResponse)
async def get_search(request: Request, sunlight: str = "", moisture: str = "",
                     indoor_spread_min: float = 0,
                     indoor_spread_max: float = 100, indoor_height_min: float = 0,
                     indoor_height_max: float = 100, toxic_dogs: Optional[str] = None,
                     toxic_cats: Optional[str] = None):
    toxic_cats = toxic_cats == "on"
    toxic_dogs = toxic_dogs == "on"
    json_data = {"sunlight": sunlight, "moisture": moisture,
                 "indoor_spread_min": indoor_spread_min,
                 "indoor_spread_max": indoor_spread_max,
                 "indoor_height_min": indoor_height_min,
                 "indoor_height_max": indoor_height_max, "toxic_cats": toxic_cats,
                 "toxic_dogs": toxic_dogs}
    response = requests.get(f"{search_service_url1}/search", json=json_data,
                            headers={'Content-Type': 'application/json'})

    if not response.ok:
        response = requests.get(f"{search_service_url2}/search", json=json_data,
                                headers={'Content-Type': 'application/json'})
        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    return templates.TemplateResponse("search.html", {"request": request, "search": response.json()})
