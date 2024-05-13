from typing import Optional

from cassandra.cluster import Cluster, Session


class CassandraClient:
    def __init__(self, host: str, port: int, keyspace: str):
        self._host: str = host
        self._port: int = port
        self._keyspace: str = keyspace
        self._session: Optional[Session] = None

    def connect(self):
        self._session = Cluster([self._host], port=self._port).connect(self._keyspace)

    def execute(self, query):
        self._session.execute(query)

    def close(self):
        self._session.shutdown()
