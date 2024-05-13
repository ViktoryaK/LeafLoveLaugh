from fastapi import FastAPI, Request, HTTPException
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.common import catalog_service_url, review_service_url, authentication_service_url, search_service_url, \
    facade_service_port, latest_service_url

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
    data = {"plant_id": plant_id}
    response = requests.get(f'{catalog_service_url}/catalog/{plant_id}', json=data)

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response_comments = requests.get(f'{review_service_url}/reviews/{plant_id}', json=data)

    return templates.TemplateResponse("plant.html", {"request": request, "plant": response.json(),
                                                     "comments": response_comments.json()})


@app.post("/register")
async def register_user(request: Request, username: str, password: str):
    # noinspection DuplicatedCode
    data = {'username': username, 'password': password}
    response = requests.post(f'{authentication_service_url}/register', json=data)

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    request.session["user_id"] = response.json()["user_id"]

    return {"status": "ok", "message": "Successfully registered"}


@app.post("/login")
async def login_user(username: str, password: str, request: Request):
    # noinspection DuplicatedCode
    data = {'username': username, 'password': password}
    response = requests.post(f'{authentication_service_url}/login', json=data)

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    request.session["user_id"] = response.json()["user_id"]

    return {"status": "ok", "message": "Successfully logged in"}


@app.post("/logout")
async def logout_user(request: Request):
    request.session.pop("user_id")


@app.post("/review")
async def create_review(plant_id: int, review: str, request: Request):
    response = requests.post(f"{review_service_url}/review/{plant_id}",
                             json={"user_id": request.session.get("user_id"), "review": review})

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"status": "ok", "message": "Review created successfully"}


@app.get("/reviews/{plant_id}")
async def create_review(plant_id: int):
    response = requests.get(f"{review_service_url}/reviews/{plant_id}")

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.get("/latest-reviews")
async def get_latest_reviews(request: Request):
    response = requests.get(f"{latest_service_url}/latest-reviews")
    reviews = [{"user": requests.get(f"{authentication_service_url}/user/{review['user_id']}").json(),
             "plant": requests.get(f"{catalog_service_url}/catalog/{review['plant_id']}").json(),
             "text": review["text"]}
            for review in response.json()]
    return templates.TemplateResponse("latest_reviews.html", {"request": request, "reviews": reviews})


@app.get("/search", response_class=HTMLResponse)
async def get_search(request = Request, sunlight: str = None, moisture: str = None, indoor_spread_min: float = 0,
                     indoor_spread_max: float = 100, indoor_height_min: float = 0,
                     indoor_height_max: float = 100, toxic_dogs: bool = False, toxic_cats: bool = False):
    response = requests.get(f"{search_service_url}/search",
                            json={"sunlight": sunlight, "moisture": moisture, "indoor_spread_min": indoor_spread_min,
                                  "indoor_spread_max": indoor_spread_max, "indoor_height_min": indoor_height_min,
                                  "indoor_height_max": indoor_height_max, "toxic_cats": toxic_cats,
                                  "toxic_dogs": toxic_dogs})

    return templates.TemplateResponse("search.html", {"request": request, "search": response.json()})
