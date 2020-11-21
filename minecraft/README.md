# Minecraft server administration scripts
A collection of scripts related to administration of minecraft servers
## `rcon.py`
A simple python program to execute server commands with RCON.

Requirements:
* [mcrcon](https://pypi.org/project/mcrcon/)

Usage:
* The server must be configured to use RCON
* In `server.properties`:
    * `enable-rcon=true`
    * `rcon.password=<password>`
    * `rcon.port=<port>`
* Passing arguments:
    * All arguments (The server address, RCON port and RCON password) can either be passed as command line args or as environment variables.
    * Command line arguments will override environment variables.
    * The syntax for passing arguments on the command line is as follows:
        * `rcon.py --url <address>`
        * `rcon.py --port <port>`
        * `rcon.py --password <password>`
    * The relevant environment variables are:
        * `MC_SERVER_ADDR`
        * `MC_SERVER_RCON_PORT`
        * `MC_SERVER_RCON_PASS`
* Syntax:
    * `rcon.py <command...>`
    * In `<command>`, spaces do not need to be escaped.

## `minecraft@.service`, `stop.sh`, `reload.sh`
A systemd unit file for running a minecraft server.

Requirements:
* `rcon.py`

Usage:
* Place the server files in `/srv/mineraft/<server name>`
* Name the server jar `server.jar`
* Place `stop.sh` and `reload.sh` in the server directory.
* Replace the values of `MC_SERVER_ADDR`, `MC_SERVER_RCON_PASS` and `MC_SERVER_RCON_PORT` in `stop.sh` and `reload.sh`
* Enable/start the service with `systemctl enable --now minecraft@<server name>.service`
* To access the console (you shouldn't need to, just use `rcon.py`) you can run `tmux a -t mc-<server name>` as root

## `minecraft_backup@.service`, `minecraft_backup@.timer`, `backup.sh`
A systemd timer to run `backup.sh` every 15 minutes.

Requirements:
* `rcon.py`
* A `borg` repository. See the [borg docs](https://borgbackup.readthedocs.io/en/stable/index.html) for information.

Usage:
* Place `backup.sh` in `/srv/minecraft/<server name>`
* Replace the values of `MC_SERVER_ADDR`, `MC_SERVER_RCON_PASS`, `MC_SERVER_RCON_PORT`, `SERVER_NAME`, and `BORG_REPO_DIR` in `backup.sh`.
    * `SERVER_NAME` is used in the name of the backup in borg
* Enable/start the timer with `systemctl enable --now minecraft_backup@<server name>.timer`

## `scraper.py`, `minecraft_stats@.service`, `minecraft_stats@.timer`
A python program to take data from a minecraft server and store it in InfluxDB.

Requirements:
* An InfluxDB server.
* `rcon.py`
* [python-influxdb](https://github.com/influxdata/influxdb-python)
* [mcrcon](https://pypi.org/project/mcrcon/)

Usage:
* Place `scraper.py` in `/srv/minecraft/<server name>`
* Replace the values of `MINECRAFT_DB_NAME`, `SERVER_ID`, `INFLUX_SERVER_ADDR`, `INFLUX_SERVER_PORT`, `MC_SERVER_ADDR`, `MC_SERVER_RCON_PORT` and `MC_SERVER_RCON_PASS` in `scraper.py`
* Enable/start the timer with `systemctl enable --now minecraft_stats@<server name>.timer`

---
### Credits
* `minecraft@.service` is modified from [this](https://github.com/agowa338/MinecraftSystemdUnit/).
