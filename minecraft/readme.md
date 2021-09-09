# Minecraft

A collection of systemd units and accompanying scripts related to administration of minecraft servers.

## rcon.py

A simple python program to execute server commands with RCON.

### Dependencies

- [mcrcon](https://pypi.org/project/mcrcon/)

### Setup

- The server must be configured to use RCON
  - In `server.properties`:
    - `enable-rcon=true`
    - `rcon.password=<password>`
    - `rcon.port=<port>`

### Usage

#### Syntax

`rcon.py [--args] <command...>`

`<command...>` is joined together with spaces, meaning that they need not be escaped in the command line invocation. This means the following commands are equivalent.

- `rcon.py "hello world"`
- `rcon.py hello\ world`
- `rcon.py hello world`

#### Arguments

| Environment variable | command line argument | Default value                                        |
| -------------------- | --------------------- | ---------------------------------------------------- |
| MC_SERVER_ADDR       | --url                 | No default. Must be provided for the program to work |
| MC_SERVER_RCON_PORT  | --port                | `25575`                                              |
| MC_SERVER_RCON_PASS  | --pass                | No default. Must be provided for the program to work |

## minecraft@.service

A systemd unit to run a minecraft server.

### Dependencies

- `rcon.py`
- `stop.sh`
- `reload.sh`

### Usage

- Place the server files in `/srv/mineraft/<server name>`
- Name the server jar `server.jar`
- Place (or symlink) `stop.sh` and `reload.sh` in the server directory.
- Replace the values of `MC_SERVER_ADDR`, `MC_SERVER_RCON_PASS` and `MC_SERVER_RCON_PORT` in `stop.sh` and `reload.sh`
- Enable/start the service with `systemctl enable --now minecraft@<server name>.service`
- To access the console (you shouldn't need to, just use `rcon.py`) you can run `tmux a -t mc-<server name>` as root

## minecraft_backup@.service + minecraft_backup@.timer

A systemd timer to run `backup.sh` every 15 minutes.

### Dependencies

- A [borg](https://github.com/borgbackup/borg) repository.
- `rcon.py`
- `backup.sh`

Usage:

- Place (or symlink) `backup.sh` in `/srv/minecraft/<server name>`
- Replace the values of `MC_SERVER_ADDR`, `MC_SERVER_RCON_PASS`, `MC_SERVER_RCON_PORT`, `SERVER_NAME`, and `BORG_REPO_DIR` in `backup.sh`.
- Enable/start the timer with `systemctl enable --now minecraft_backup@<server name>.timer`

## scraper.py / minecraft_stats@.service + minecraft_stats@.timer

A python program to take data from a minecraft server and store it in InfluxDB.

### Dependencies

- An [InfluxDB](https://github.com/influxdata/influxdb) server.
- `rcon.py`
- [python-influxdb](https://github.com/influxdata/influxdb-python)

Usage:

- Place (or link) `scraper.py` in `/srv/minecraft/<server name>`
- Replace the values of `MINECRAFT_DB_NAME`, `SERVER_ID`, `INFLUX_SERVER_ADDR`, `INFLUX_SERVER_PORT`, `MC_SERVER_ADDR`, `MC_SERVER_RCON_PORT` and `MC_SERVER_RCON_PASS` in `scraper.py`
- Enable/start the timer with `systemctl enable --now minecraft_stats@<server name>.timer`

---

`minecraft@.service` is derived from [this](https://github.com/agowa338/MinecraftSystemdUnit/), under the terms of the MIT licence.

Available under the terms of the Mozilla Public Licence, version 2.0
