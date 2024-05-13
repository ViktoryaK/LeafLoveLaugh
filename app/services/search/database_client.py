from app.cassandra_client import CassandraClient


class SearchDatabaseClient(CassandraClient):
    def get_tags(self, sunlight=None, moisture=None, indoor_spread_min=0, indoor_spread_max=100, indoor_height_min=0,
                 indoor_height_max=100, toxic_dogs=False, toxic_cats=False):
        query = f"SELECT plant_id, plant_name, plant_img FROM search_tags WHERE "
        if sunlight is not None:
            query += f"sunlight='{sunlight}' AND "
        if moisture is not None:
            query += f"moisture='{moisture}' AND "
        query += f"indoor_spread_min>={indoor_spread_min} AND "
        query += f"indoor_spread_max<={indoor_spread_max} AND "
        query += f"indoor_height_min>={indoor_height_min} AND "
        query += f"indoor_height_max<={indoor_height_max} AND "
        if toxic_dogs:
            query += f"toxic_dogs='No' AND "
        if toxic_cats:
            query += f"toxic_cats='No' AND "
        query = query[:-5] + " ALLOW FILTERING "
        print(query)
        return self._session.execute(query)  # TODO: refactor
