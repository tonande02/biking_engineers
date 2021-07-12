import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(
    host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
    dbname = "postgres",
    user = "consultant@academy-de-course-2021-summer-prod-001",
    password = "3eBXkuVvaJ5ncNGP",
    port = 5432
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

with conn.cursor() as cur:
    cur.execute("CREATE DATABASE bikes_weather_db;")

conn.close()

conn = psycopg2.connect(
    host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
    dbname = "bikes_weather_db",
    user = "consultant@academy-de-course-2021-summer-prod-001",
    password = "3eBXkuVvaJ5ncNGP",
    port = 5432
)

cur = conn.cursor()

#CREATE SCHEMAS? WHICH ONES? WHICH TABLES IN WHICH SCHEMAS?

#https://stackoverflow.com/questions/65584986/insert-json-data-into-postgresql-table-using-python

cur.execute("CREATE TABLE IF NOT EXISTS BIKE_STATION (id serial PRIMARY KEY, num integer, data varchar);")

conn.commit()