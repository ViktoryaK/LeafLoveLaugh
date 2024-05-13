from cassandra.cluster import Cluster


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def get_reviews(self):
        query = f"SELECT * FROM search_comments ORDER BY date DESC LIMIT 10"
        return self.session.execute(query)

    def post_review(self, data):
        values = [data["review_id"], data["plant_id"], data["review"], data["date"], data["user_id"], data["user_name"]]
        query = ("INSERT INTO search_comments (review_id, plant_id, review, date, user_id, "
                 "user_name) VALUES(?, ?, ?, "
                    "?, ?, ?)")
        prepared = self.session.prepare(query)
        try:
            self.session.execute_async(prepared, values)
        except AttributeError:
            print(f"Can't add row {values}")
