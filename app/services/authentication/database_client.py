from typing import ClassVar
from uuid import UUID

from app.postgres_client import PostgresClient
from app.user_info import UserInfo


class UserAlreadyExistsError(RuntimeError):
    pass


class UserNotFoundError(RuntimeError):
    pass


class AuthenticationFailure(RuntimeError):
    pass


class AuthorizationDatabaseClient(PostgresClient):
    _table_name: ClassVar[str] = "users"

    def authenticate_user(self, username: str, password: str) -> UUID:
        self._cursor.execute(f"SELECT user_id FROM {self._table_name} WHERE user_name = %s AND password = %s",
                             (username, password))
        row = self._cursor.fetchone()

        if not row:
            raise AuthenticationFailure()

        return row[0]

    def get_user_info(self, user_id: UUID) -> UserInfo:
        self._cursor.execute(f"SELECT user_name FROM {self._table_name} WHERE user_id = %s", (user_id,))
        row = self._cursor.fetchone()

        if not row:
            raise UserNotFoundError()

        return row[0]

    def register_user(self, username: str, password: str) -> UUID:
        self._cursor.execute(
            f"INSERT INTO {self._table_name} (user_id, user_name, password) VALUES (gen_random_uuid(), %s, %s) RETURNING user_id",
            (username, password))
        result = self._cursor.fetchone()
        self._connection.commit()

        if not result:
            raise UserAlreadyExistsError()

        return result[0]
