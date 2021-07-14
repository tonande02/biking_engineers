import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
import geopy.distance

def get_obs_stations(cur):
    cur.execute(f"SELECT c_id, lat, lon FROM {SCHEMA}.bike_station")
    return cur.fetchall()

def get_weather_stations(cur):
    cur.execute(f"SELECT c_id, latitude as lat, longitude as lon FROM {SCHEMA}.weather_station")
    return cur.fetchall()

def find_list_with_closest(obs_stations, weather_stations):
    closest_ws = []
    for st in obs_stations:
        distances = []
        for ws in weather_stations:
            distance_st_ws = distance_between(st[1], st[2], ws[1], ws[2])
            distances.append((ws[0], distance_st_ws))
        closest_ws.append((st[0], sorted(distances, key=lambda tup: tup[1])[0][0]))
    return closest_ws

def distance_between(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    distance = geopy.distance.geodesic(coords_1, coords_2).km
    return distance

def add_closest_weather_st_to_obs_st_in_db(cur, obs_st_with_closest_weather_st):
    cur.execute(f"ALTER TABLE {SCHEMA}.bike_station ADD COLUMN IF NOT EXISTS cosest_weather_st_c_id INT;")
    for tup in obs_st_with_closest_weather_st:
        sql_str = f"UPDATE {SCHEMA}.bike_station SET cosest_weather_st_c_id = {tup[1]} WHERE c_id = {tup[0]};"
        cur.execute(sql_str)

#################################################################
SCHEMA = "cleansed"
DB_NAME = "biking_engineers"#"bikes_weather_db"#

def main():
    conn = psycopg2.connect(
        host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
        dbname = DB_NAME,
        user = "consultant@academy-de-course-2021-summer-prod-001",
        password = "3eBXkuVvaJ5ncNGP",
        port = 5432
    )

    cur = conn.cursor()
#-- DO THIS --

    obs_stations = get_obs_stations(cur)
    weather_stations = get_weather_stations(cur)
    obs_st_with_closest_weather_st = find_list_with_closest(obs_stations, weather_stations)
    add_closest_weather_st_to_obs_st_in_db(cur, obs_st_with_closest_weather_st)

#-- TO HERE --
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

