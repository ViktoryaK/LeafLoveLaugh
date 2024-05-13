from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

from app.services.authentication.database_client import AuthorizationDatabaseClient, UserAlreadyExistsError, \
    AuthenticationFailure, UserNotFoundError
from app.common import authentication_service_port

app = FastAPI(host="localhost", port=authentication_service_port)

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = AuthorizationDatabaseClient(dbname="postgres",
                                     user="postgres",
                                     password="987234",
                                     host="postgres-users",
                                     port=5432)


@app.on_event("startup")
async def startup_event():
    client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()


class LoginData(BaseModel):
    username: str
    password: str


@app.post('/login')
async def login(data: LoginData):
    try:
        return {"user_id": client.authenticate_user(data.username, crypt_context.hash(data.password))}
    except AuthenticationFailure:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


class RegisterData(BaseModel):
    username: str
    password: str


@app.post('/register')
async def register(data: RegisterData):
    try:
        return {"user_id": client.register_user(data.username, crypt_context.hash(data.password))}
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@app.get('/user/{user_id}')
async def get_user_info(user_id: UUID):
    try:
        return client.get_user_info(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
