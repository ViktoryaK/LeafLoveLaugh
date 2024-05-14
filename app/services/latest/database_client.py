from typing import ClassVar
from uuid import UUID
from app.cassandra_client import CassandraClient


class LatestDatabaseClient(CassandraClient):
    _table_name: ClassVar[str] = "latest_reviews"

    def get_reviews(self):
        query = f"SELECT * FROM {self._table_name} LIMIT 10"
        return self._session.execute(query)

    def post_review(self, data):
        values = [UUID(data["review_id"]), data["plant_id"], data["review"], data["date"], data["user_name"]]
        query = (f"INSERT INTO {self._table_name} (review_id, plant_id, review, date, "
                 "user_name) VALUES(?, ?, ?, "
                 "?, ?)")
        prepared = self._session.prepare(query)
        try:
            self._session.execute_async(prepared, values)
        except AttributeError:
            print(f"Can't add row {values}")
