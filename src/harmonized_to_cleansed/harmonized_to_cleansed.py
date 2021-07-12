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
#-----------------------------------------------------------------
def create_schema(name):
#    global cur
    cur.execute("CREATE SCHEMA IF NOT EXISTS " + name + ";")
#-----------------------------------------------------------------
def create_table(schema, name, column_list):
    create_str = "CREATE TABLE IF NOT EXISTS "
    create_str += schema + "." + name
    create_str += " (c_id SERIAL PRIMARY KEY"
    for column_name in column_list:
        create_str += ", " + column_name + " TEXT"
    create_str += ");"
    print(create_str)
    cur.execute(create_str)
#-----------------------------------------------------------------
def populate_db_from_list_of_dict(schema, table_name, list_of_dict_to_add):

    for dict in list_of_dict_to_add:
        value_str = "'"
        for value in dict.values():
            value_str += str(value).replace("'", "") + "', '" # "'SN18700', 'OSLO - BLINDERN', '59.9423', '10.72'"
        value_str = value_str[:-3]
        print(value_str)
        create_str = "INSERT INTO " + schema + "." + table_name + " (" + ", ".join(dict.keys()) + ") VALUES (" + value_str + ");" #"id, name, latitude, longditude"

        cur.execute(create_str)
#-----------------------------------------------------------------
def get_list_of_dict_from_json(file_path):
    with open(file_path, "r") as r_file:
        r_loaded = json.load(r_file)
    if type(r_loaded) == list:  # to get columns from: obs_station_infor.json og obs_20*.json
        return r_loaded
    else:   # to get columns from: Frost stasjoninfo
        return r_loaded["stations"]
#-----------------------------------------------------------------
def get_columns_frost_json(file_path):
    with open(file_path, "r") as r_file:
        loaded_json = json.load(r_file)

    columns = []
    list_of_measurements = loaded_json["data"]
    example = list_of_measurements[0]
    for key, value in example.items():
        if type(value) != list: # and type(value) != dict:
            columns.append(key)
        elif type(value) == list: # L17
            for item in value: # L19-34 -contains one dictionarys and 6..
                if type(item) == dict: # L18
                    for key2, value2 in item.items():
                        if type(value2) != dict:
                            columns.append(key + "_" + key2)
                        else:   # L22
                            for key3, value3 in value2.items():
                                columns.append(key + "_" + key2 + "_" + key3)
                if type(item) != dict:
                    columns.append(key)
    print(columns)
    return columns

#-----------------------------------------------------------------    
def get_columns_from_frost_stations_json(file_path):
    with open(file_path, "r") as r_file:
        loaded_json = json.load(r_file)
    stations = loaded_json["stations"]
    dict_ex = stations[0]
    column_list = dict_ex.keys()
    print(column_list)
    return column_list
#-----------------------------------------------------------------
def get_columns_from_obs_json(file_path):
    with open(file_path, "r") as r_file:
        loaded_json = json.load(r_file)
    dict_ex = loaded_json[0]
    column_list = dict_ex.keys()
    print(column_list)
    return column_list
#-----------------------------------------------------------------
def create_schema_and_tables():
    create_schema(schema)

    frost_temp_columns = get_columns_frost_json("data/raw/weather_data_temperature.json")
    frost_perc_columns = get_columns_frost_json("data/raw/weather_data_precipitation.json")
    frost_weather_station_columns = get_columns_from_frost_stations_json("data/harmonized/harmonized_weather_stations.json")
    obs_bike_trip_columns = get_columns_from_obs_json("data/harmonized/obs_2021-06.json")
    obs_bike_station_columns = get_columns_from_obs_json("data/harmonized/obs_station_info.json")

    create_table(schema, "weather_station", frost_weather_station_columns)
    create_table(schema, "temperature", frost_temp_columns)
    create_table(schema, "rain", frost_perc_columns)
    create_table(schema, "bike_station", obs_bike_station_columns)
    create_table(schema, "bike_trip", obs_bike_trip_columns)

def populate_easy():
    frost_weather_station_data = get_list_of_dict_from_json("data/harmonized/harmonized_weather_stations.json")
    obs_bike_trip_data = get_list_of_dict_from_json("data/harmonized/obs_2021-06.json")
    obs_bike_station_data = get_list_of_dict_from_json("data/harmonized/obs_station_info.json")
    
    populate_db_from_list_of_dict(schema, "weather_station", frost_weather_station_data)
    populate_db_from_list_of_dict(schema, "bike_trip", obs_bike_trip_data)
    populate_db_from_list_of_dict(schema, "bike_station", obs_bike_station_data)

# file_name = input("File_name? ")
# coulumns = get_columns_in_json("data/harmonized/" + file_name) #obs_2020-03.json")
# table_name = "test_1"

# create_table(table_name, coulumns)

schema = "cleansed"
db_name = "bikes_weather_db"

conn = psycopg2.connect(
    host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
    dbname = db_name,
    user = "consultant@academy-de-course-2021-summer-prod-001",
    password = "3eBXkuVvaJ5ncNGP",
    port = 5432
)

cur = conn.cursor()

# create_schema_and_tables()
populate_easy()

conn.commit()
conn.close()