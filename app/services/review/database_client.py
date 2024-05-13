from typing import ClassVar

from app.cassandra_client import CassandraClient


class ReviewDatabaseClient(CassandraClient):
    _table_name: ClassVar[str] = "reviews"

    def get_reviews_for_plant(self, plant_id: int):
        query = f"SELECT user_name, review, date FROM {self._table_name} WHERE plant_id = {plant_id} ORDER BY date"
        return self._session.execute(query)

    def post_review(self, values):
        query = (f"INSERT INTO {self._table_name} (review_id, plant_id, review, date, user_id, "
                 "user_name) VALUES(?, ?, ?, "
                 "?, ?, ?)")
        prepared = self._session.prepare(query)
        try:
            self._session.execute_async(prepared, values)
        except AttributeError:
            print(f"Can't add row {values}")
