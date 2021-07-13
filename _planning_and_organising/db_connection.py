import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

# conn = psycopg2.connect(
#     host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
#     dbname = "postgres",
#     user = "consultant@academy-de-course-2021-summer-prod-001",
#     password = "3eBXkuVvaJ5ncNGP",
#     port = 5432
# )

# conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# with conn.cursor() as cur:
#     cur.execute("CREATE DATABASE bikes_weather_db;")

# conn.close()

def create_schema(name):
#    global cur
    cur.execute("CREATE SCHEMA IF NOT EXISTS " + name + ";")

def create_table(name, column_list):
    create_str = "CREATE TABLE IF NOT EXISTS "
    create_str += schema + "." + name
    create_str += " (id SERIAL PRIMARY KEY"
    for column_name in column_list:
        create_str += ", " + column_name + " TEXT"
    create_str += ");"
    print(create_str)
    cur.execute(create_str)

def get_columns_in_json(file_path):
    with open(file_path, "r") as r_file:
        r_loaded = json.load(r_file)
    if type(r_loaded) == list:
        dict_ex = r_loaded[0]
        column_list = dict_ex.keys()
    else:
        stations = r_loaded["stations"]
        dict_ex = stations[0]
        column_list = dict_ex.keys()
    print(column_list)

key_in = input("file_path? ")
coulumns = get_columns_in_json("data/harmonized/" + key_in)#obs_2020-03.json")

# schema = "cleansed"
# db_name = "bikes_weather_db"

# conn = psycopg2.connect(
#     host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
#     dbname = db_name,
#     user = "consultant@academy-de-course-2021-summer-prod-001",
#     password = "3eBXkuVvaJ5ncNGP",
#     port = 5432
# )

# cur = conn.cursor()
# create_schema(schema)
# create_table(name, list(pi.keys())


# #CREATE SCHEMAS? WHICH ONES? WHICH TABLES IN WHICH SCHEMAS?

# #https://stackoverflow.com/questions/65584986/insert-json-data-into-postgresql-table-using-python

# cur.execute("CREATE TABLE IF NOT EXISTS BIKE_STATION (id serial PRIMARY KEY, num integer, data varchar);")

# conn.commit()