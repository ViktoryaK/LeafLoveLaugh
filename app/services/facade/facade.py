from fastapi import FastAPI, Request, HTTPException
import requests

from app.common import catalog_service_url, review_service_url, authentication_service_url, search_service_url, \
    facade_service_port

app = FastAPI(host="localhost", port=facade_service_port)


@app.get("/catalog")
async def catalog():
    response = requests.get(f'{catalog_service_url}/catalog')

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.get("/catalog/{plant_id}")
async def get_plant_by_id(plant_id: int = 0):
    data = {"plant_id": plant_id}
    response = requests.get(f'{catalog_service_url}/catalog/{plant_id}', json=data)

    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response_comments = requests.get(f'{review_service_url}/review_service/{plant_id}', json=data)

    return response.text + response_comments.text


@app.post("/register")
async def register_user(username: str, password: str, request: Request):
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


@app.get("/reviews")
async def get_latest_reviews():
    response = requests.get(f"{review_service_url}/latest-reviews")
    return [{"username": requests.get(f"{authentication_service_url}/user/{review['user_id']}").json()["name"],
             "": "",
             "text": review["text"]}
            for review in response.json()]


@app.get("/search")
async def get_search(sunlight: str = None, moisture: str = None, indoor_spread_min: float = 0,
                     indoor_spread_max: float = 100, indoor_height_min: float = 0,
                     indoor_height_max: float = 100, toxic_dogs: bool = False, toxic_cats: bool = False):
    response = requests.get(f"{search_service_url}/search",
                            json={"sunlight": sunlight, "moisture": moisture, "indoor_spread_min": indoor_spread_min,
                                  "indoor_spread_max": indoor_spread_max, "indoor_height_min": indoor_height_min,
                                  "indoor_height_max": indoor_height_max, "toxic_cats": toxic_cats,
                                  "toxic_dogs": toxic_dogs})
    return response.text
