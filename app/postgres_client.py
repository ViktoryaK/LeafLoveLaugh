import psycopg2
from fastapi import HTTPException, status


class PostgresClient:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self._dbname: str = dbname
        self._user: str = user
        self._password: str = password
        self._host: str = host
        self._port: int = port
        self._connection = None
        self._cursor = None

    def connect(self):
        try:
            self._connection = psycopg2.connect(
                dbname=self._dbname,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
            self._cursor = self._connection.cursor()
        except psycopg2.Error as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()
