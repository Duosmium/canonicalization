from thefuzz import fuzz
import sqlite3


def name_matches(school_1, school_2):
    return fuzz.partial_ratio(school_1[1], school_2[1]) >= 95


def different_city(school_1, school_2):
    return school_1[2] and school_2[2] and school_1[2] != school_2[2]


conn = sqlite3.connect("duosmium.sqlite3")
states = conn.execute("SELECT * FROM STATES;").fetchall()
all_matches = {}
for state in states:
    schools = conn.execute(f"SELECT schools.id, school, c.city, schools.state FROM schools LEFT OUTER JOIN cities c on schools.city = c.id WHERE schools.state = {state[0]};").fetchall()
    school_data = [school for school in schools]
    for i, school in enumerate(schools):
        sublist = school_data[:i]
        matches = [s for s in sublist if name_matches(school, s) and not different_city(school, s)]
        if matches:
            all_matches[school] = matches

for m in all_matches:
    def format_school(school):
        school_state = states[m[3] - 1][1]
        output = school[1] + " ("
        if school[2]:
            output += school[2] + ", "
        output += school_state + ")"
        return output
    for match in all_matches[m]:
        print(f"{format_school(m)} is similar to {format_school(match)}.")


