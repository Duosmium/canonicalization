from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import sqlite3


conn = sqlite3.connect("duosmium.sqlite3")
locator = Nominatim(user_agent="myGeocoder")
geocode = RateLimiter(locator.geocode, min_delay_seconds=0.5)

schools_list = conn.execute("SELECT school, c.city, s.state FROM schools LEFT OUTER JOIN cities c on c.id = schools.city JOIN states s on s.id = schools.state WHERE s.postal_code = \"NV\"").fetchall()
output = []
for school in schools_list:
    name, city, state = school
    if city is not None and city != 'nan':
        output.append(school)
        continue
    address = f"{name}, {state}"
    location = locator.geocode(address, exactly_one=True, addressdetails=True)
    if location is None:
        print(f"{name} is missing a location.")
        continue
        # .get("city", f"Look up the city of {name} ({state}) yourself.")
    city = location.raw["address"].get("city", location.raw["address"].get("town", location.raw["address"].get("village", location.raw["address"].get("hamlet", None))))
    print(name, city)
