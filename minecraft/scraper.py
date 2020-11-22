import datetime
import http
import json
import os
from typing import Dict

from influxdb import InfluxDBClient
from mcrcon import MCRcon

MINECRAFT_DB_NAME: str = "minecraft_server_data"
SERVER_ID: str = "server_id"

LOCAL_TIMEZONE = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo
RUN_TIME = datetime.datetime.now(tz=LOCAL_TIMEZONE).isoformat()

INFLUX_SERVER_ADDR = "localhost"
INFLUX_SERVER_PORT = 8086

MC_SERVER_ADDR = "localhost"
MC_SERVER_RCON_PORT = 25575
MC_SERVER_RCON_PASS = "password"


def is_valid_mojang_uuid(uuid: str) -> bool:
    allowed_chars = '0123456789abcdef'
    allowed_len = 32

    uuid = uuid.lower()

    if len(uuid) != allowed_len:
        return False
    if any(x not in allowed_chars for x in uuid):
        return False

    return True


def player_from_uuid(identifier: str) -> str:
    timestamp = None
    print("\n", identifier, "\n")
    valid = True

    # Handle the timestamp
    get_args = ""
    if timestamp is not None:
        get_args = "?at=" + str(timestamp)

    # Build the request path based on the identifier
    req = ""
    identifier = identifier.replace("-", "").replace("'", "")
    if is_valid_mojang_uuid(identifier):
        req = "/user/profiles/" + identifier + "/names" + get_args
    else:
        valid = False

    # Proceed only, when the identifier was valid
    if not valid:
        raise RuntimeError("Invalid uuid")
    # Request the player data
    http_conn = http.client.HTTPSConnection("api.mojang.com")
    http_conn.request(
        "GET",
        req,
        headers={
            'User-Agent': 'https://github.com/Sciencentistguy/minecraft-server-scripts',
            'Content-Type': 'application/json'})
    response: str = http_conn.getresponse().read().decode("utf-8")

    # In case the answer is empty, the user dont exist
    if not response:
        raise RuntimeError("User does not exist")
    # If there is an answer, fill out the variables
    # Parse the JSON
    json_data = json.loads(response)

    # Handle the response of the different requests on different ways
    # Request using username
    # The UUID
    uuid = identifier

    current_name = ""
    current_time = 0

    # Getting the username based on timestamp
    for name in json_data:
        # Prepare the JSON
        # The first name has no change time
        if 'changedToAt' not in name:
            name['changedToAt'] = 0

        # Get the right name on timestamp
        if current_time <= name['changedToAt'] and (timestamp is None or name['changedToAt'] <= timestamp):
            current_time = name['changedToAt']
            current_name = name['name']

    # The username written correctly
    username = current_name
    return username


def create_json_structure(measurement_name: str, tags: Dict[str, str], fields: Dict[str, str]):
    return [
        {
            "measurement": measurement_name,
            "tags": tags,
            "time": RUN_TIME,
            "fields": fields
        }
    ]


client = InfluxDBClient(host=INFLUX_SERVER_ADDR, port=INFLUX_SERVER_PORT)

client.create_database(MINECRAFT_DB_NAME)

client.switch_database(MINECRAFT_DB_NAME)

with MCRcon(MC_SERVER_ADDR, MC_SERVER_RCON_PASS, MC_SERVER_RCON_PORT) as rc:
    whitelist_response = rc.command("whitelist list")
    list_response = rc.command("list")

whitelist = whitelist_response[whitelist_response.find(
    ":") + 1:].replace(",", "").split()
print(whitelist)


online_players = list_response[list_response.find(
    ":") + 1:].replace(",", "").split()
print(online_players)


players_json = create_json_structure("players", {"server_id": SERVER_ID}, {
    "online_player_count": len(online_players),
    "online_players": ",".join(online_players)
})

print(players_json)

client.write_points(players_json)

whitelist_json = create_json_structure("whitelist", {"server_id": SERVER_ID}, {
    "whitelist_player_count": len(whitelist),
    "whitelist": ",".join(whitelist)
})

client.write_points(whitelist_json)

total_size = 0
start_path = 'world'
for path, dirs, files in os.walk(start_path):
    for f in files:
        fp = os.path.join(path, f)
        total_size += os.path.getsize(fp)
size_json = create_json_structure("world_size", {"server_id": SERVER_ID}, {
    "world_size": total_size
})
client.write_points(size_json)

os.chdir("world/stats")
for filename in os.listdir("."):
    print(filename)
    uuid = filename.replace(".json", "")
    playername = player_from_uuid(uuid)
    parsed_data: Dict[str, str] = {}
    if not filename.endswith("json"):
        continue
    with open(filename, "r") as f:
        print(f)
        stats_data = json.load(f)
        stats_data = stats_data["stats"]
        for cat, dat in stats_data.items():
            for stat, value in dat.items():
                parsed_data[cat + "/" + stat] = value
    influx_json = create_json_structure(
        "stats", {"server_id": SERVER_ID, "player": playername}, parsed_data)
    client.write_points(influx_json)
