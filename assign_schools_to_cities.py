import sys
import requests
import yaml
import sqlite3

data_file = sys.argv[1]
if not data_file.endswith(".yaml"):
    data_file += ".yaml"

print(f"Input: {data_file}")

# raw_download = requests.get(f"http://localhost:8080/data/{data_file}")
raw_download = requests.get(f"https://www.duosmium.org/data/{data_file}")
raw_download.encoding = "UTF-8"
raw_data = raw_download.text
sciolyff_yaml = yaml.safe_load(raw_data)

conn = sqlite3.connect("duosmium.sqlite3")

teams_info = sciolyff_yaml["Teams"]
# print(teams_info)

for team in teams_info:
    if "city" not in team or not team["city"]:
        statement = f"SELECT * FROM schools JOIN cities c on c.id = schools.city join states s on s.id = schools.state where schools.school = \"{team['school']}\" AND s.postal_code = '{team['state']}' AND schools.city NOT NULL"
        potential_schools = conn.execute(statement).fetchall()
        if len(potential_schools) != 1:
            continue
        print("Match found for", team["school"])
        team["city"] = potential_schools[0][6]

# print(sciolyff_yaml["Teams"])

with open(data_file, "w") as fil:
    fil.write("---\n")
    yaml.safe_dump(sciolyff_yaml, fil, indent=2, sort_keys=False, allow_unicode=True)
