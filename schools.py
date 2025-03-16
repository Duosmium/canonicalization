import os
import pandas as pd
import requests
import sqlite3

# schools_download = requests.get("http://localhost:8080/results/schools.csv")
schools_download = requests.get("https://duosmium.org/results/schools.csv")
schools_download.encoding = "UTF-8"
schools_csv = schools_download.text
columns = ["School", "City", "State"]
with open("schools.csv", "w") as fil:
    fil.write(schools_csv)
    schools_data = pd.read_csv("schools.csv", names=columns)

os.remove("schools.csv")

conn = sqlite3.connect("duosmium.sqlite3")
conn.execute("DROP TABLE schools;")
conn.execute("DROP TABLE cities;")
cities_table_create = "CREATE TABLE IF NOT EXISTS cities (id INTEGER PRIMARY KEY AUTOINCREMENT, city VARCHAR NOT NULL, state INTEGER NOT NULL, FOREIGN KEY (state) REFERENCES states(id) ON DELETE CASCADE);"
schools_table_create = "CREATE TABLE IF NOT EXISTS schools (id INTEGER PRIMARY KEY AUTOINCREMENT, school VARCHAR NOT NULL, nickname VARCHAR, city INTEGER, state INTEGER NOT NULL, FOREIGN KEY (city) REFERENCES cities(id) ON DELETE CASCADE, FOREIGN KEY (state) REFERENCES states(id) ON DELETE CASCADE);"
conn.execute(cities_table_create)
conn.execute(schools_table_create)

for row in schools_data.iterrows():
    school_name = str(row[1][0])
    school_city = str(row[1][1])
    school_state = str(row[1][2])
    school_state_id = conn.execute(f"SELECT id from states WHERE postal_code = '{school_state}';").fetchall()
    if not school_state_id:
        continue
    school_state_id = school_state_id[0][0]
    # print(school_name, school_city, school_state_id)
    if school_city != "nan":
        existing_city = conn.execute(f"SELECT id from cities WHERE city = \"{school_city}\" AND state = {school_state_id};").fetchall()
        if len(existing_city) == 0:
            conn.execute(f"INSERT INTO cities (city, state) VALUES (\"{school_city}\", {school_state_id});")
            existing_city = conn.execute(f"SELECT id from cities WHERE city = \"{school_city}\" AND state = {school_state_id};").fetchall()
        school_city_id = existing_city[0][0]
        conn.execute(f"INSERT INTO schools (school, city, state) VALUES (\"{school_name}\", {school_city_id}, {school_state_id});")
    else:
        conn.execute(
            f"INSERT INTO schools (school, state) VALUES (\"{school_name}\", {school_state_id});")

conn.commit()
