import psycopg2
import pandas as pd


class PostgresClient:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print("Error Postgres connect", e)

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def insert_data(self, table, values, i):
        self.cur.execute(
            f"INSERT INTO {table} (Scientific_Name, Common_Name, img_name, Sunlight, Moisture," 
        "Soil_Indicator, Plant_Spread, Plant_Height, Indoor_Spread, Indoor_Height, Toxic_Dogs, Toxic_Cats, "
        "Plant_Habit, Plant_Type, Indoor_Flowering, Hanging, Bloom_Period, Humidity, Air_Purifying, "
        f"Ph_Soil, Bloom_Description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            values
        )
        self.conn.commit()


if __name__ == "__main__":
    dbname = "postgres2"
    user = "postgres"
    password = "987234"
    host = 'localhost'
    port = 5432
    table_1 = 'Plants'

    file_path = "data/plants_clean_40.csv"

    dataframe = pd.read_csv(file_path)
    dataframe = dataframe.drop("Unnamed: 21", axis=1)
    dataframe = dataframe.drop("Unnamed: 22", axis=1)

    client = PostgresClient(dbname, user, password, host, port)
    client.connect()
    for index, row in dataframe.iterrows():
        client.insert_data(table_1, list(row), index)
    client.close()
