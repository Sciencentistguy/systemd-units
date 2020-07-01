#!/bin/bash

export MC_SERVER_ADDR="localhost"
export MC_SERVER_RCON_PASS="password"
export MC_SERVER_RCON_PORT=25575

BACKUP_NAME="World backup $(date +'<%Y-%m-%d|%H.%M.%S>').tar.xz"
BACKUP_DIR="<path/to/backup/location>"

BACKUP_USER="user"
BACKUP_GROUP="group"

rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"dark_red"},{"text":"]: World backup starting (There may be lag)"}]'
rcon.py save-off
rcon.py save-all
sleep 2
tar cv world/ | pixz >"$BACKUP_DIR/$BACKUP_NAME"
chown jamie:jamie "$BACKUP_DIR/$BACKUP_NAME"
rcon.py save-on
rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"dark_red"},{"text":"]: World backup finished"}]'
