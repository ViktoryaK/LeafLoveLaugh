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



if __name__ == "__main__":
    dbname = "postgres"
    user = "postgres"
    password = "987234"
    host = 'localhost'
    port = 5432

    client = PostgresClient(dbname, user, password, host, port)
    client.connect()

    client.cur.execute("SELECT * FROM Plants;")
    plants = client.cur.fetchall()
    print(plants)
    client.close()