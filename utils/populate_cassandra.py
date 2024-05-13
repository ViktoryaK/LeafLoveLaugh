import pandas as pd


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        from cassandra.cluster import Cluster
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def insert_search(self, table, values, i):

        data = [i, values[1], values[2], values[3], values[4]]
        indoor_spread = values[8]
        indoor_height = values[9]
        data.append(float(indoor_spread.split()[0]))
        data.append(float(indoor_spread.split()[2]))
        data.append(float(indoor_height.split()[0]))
        data.append(float(indoor_height.split()[2]))
        data.append(values[10])
        data.append(values[11])
        query = ("INSERT INTO %s (plant_id, plant_name, plant_img, sunlight, moisture, indoor_spread_min, indoor_spread_max, indoor_height_min,"
                 " indoor_height_max, toxic_dogs, toxic_cats) VALUES(?, ?, ?, "
                 "?, ?, ?, ?, ?, ?, ?, ?)" % table)
        prepared = self.session.prepare(query)
        try:
            self.session.execute_async(prepared, data)
        except AttributeError:
            print(f"Can't add row {data}")

if __name__ == "__main__":
    host = 'localhost'
    port = 9042
    keyspace = 'lll_search'
    table_1 = 'search_tags'

    file_path = "data/plants_clean_40.csv"

    dataframe = pd.read_csv(file_path)

    client = CassandraClient(host, port, keyspace)
    client.connect()
    for index, row in dataframe.iterrows():
        client.insert_search(table_1, list(row), index)
    client.close()
