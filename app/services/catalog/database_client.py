from typing import ClassVar

from app.plant import Plant
from app.postgres_client import PostgresClient


class PlantDoesNotExistError(RuntimeError):
    pass


class CatalogDatabaseClient(PostgresClient):
    _table_name: ClassVar[str] = "plants"

    @staticmethod
    def _row_to_plant(row) -> Plant:
        return Plant(*row)

    def get_all_plants(self):
        self._cursor.execute(f"SELECT * FROM {self._table_name}")
        return [self._row_to_plant(row) for row in self._cursor.fetchall()]

    def get_plant_by_id(self, plant_id: int):
        self._cursor.execute(f"SELECT * FROM {self._table_name} WHERE plant_id = %s", plant_id)
        row = self._cursor.fetchone()

        if not row:
            raise PlantDoesNotExistError()

        return self._row_to_plant(row)
