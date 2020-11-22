#!/bin/bash

export MC_SERVER_ADDR="localhost"
export MC_SERVER_RCON_PASS="password"
export MC_SERVER_RCON_PORT=25575

BACKUP_DIR="<path/to/borg/repository>"
SERVER_NAME="server_to_end_all_servers"


rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"dark_red"},{"text":"]: World backup starting (There may be lag)"}]'
rcon.py save-off
rcon.py save-all
sleep 2
borg create -C lzma "$BACKUP_DIR::$SERVER_NAME-{now}" .
rcon.py save-on
rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"dark_red"},{"text":"]: World backup finished"}]'
echo Pruning backups older than 1 week
borg prune --keep-within 1w  --keep-daily 365 "$BACKUP_DIR"
