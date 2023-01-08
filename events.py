import csv
import os
import pandas as pd
import requests
import sqlite3

events_csv = requests.get("https://duosmium.org/results/events.csv").text
columns = ("Name",)
with open("events.csv", "w") as fil:
    fil.write(events_csv)

with open("events.csv", "r") as fil:
    reader = csv.reader(fil)
    events_data = [row for row in reader]

os.remove("events.csv")

# print(events_data)


conn = sqlite3.connect("duosmium.sqlite3")
conn.execute("DROP TABLE events;")
event_table_create = "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL UNIQUE);"
conn.execute(event_table_create)

for row in events_data:
    event = row[0]
    # print(event)
    conn.execute(f"INSERT INTO events (name) VALUES (\"{event}\");")

conn.commit()
