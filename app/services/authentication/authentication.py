from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from passlib.context import CryptContext

from app.services.authentication.database_client import AuthorizationDatabaseClient, UserAlreadyExistsError, \
    AuthenticationFailure, UserNotFoundError
from app.common import authentication_service_port

app = FastAPI(host="localhost", port=authentication_service_port)

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = AuthorizationDatabaseClient(dbname="postgres",
                                     user="postgres",
                                     password="987234",
                                     host="db",
                                     port=5432)


@app.on_event("startup")
async def startup_event():
    client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


@app.post('/login')
async def login(username: str, password: str):
    try:
        return {"user_id": client.authenticate_user(username, crypt_context.hash(password))}
    except AuthenticationFailure:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@app.post('/register')
async def register(username: str = "user", password: str = "user"):
    try:
        return {"user_id": client.register_user(username, crypt_context.hash(password))}
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@app.get('/user/{user_id}')
async def get_user_info(user_id: UUID):
    try:
        return client.get_user_info(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
