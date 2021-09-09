#!/bin/bash

export MC_SERVER_ADDR="localhost"
export MC_SERVER_RCON_PASS="password"
export MC_SERVER_RCON_PORT=25575

rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"red"},{"text":"]: Server shutting down in 5 seconds. Saving the world"}]'
rcon.py save-all
sleep 1
rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"red"},{"text":"]: Server shutting down in 4 seconds."}]'
sleep 1
rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"red"},{"text":"]: Server shutting down in 3 seconds."}]'
sleep 1
rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"red"},{"text":"]: Server shutting down in 2 seconds."}]'
sleep 1
rcon.py tellraw @a '["",{"text":"["},{"text":"Server","color":"red"},{"text":"]: Server shutting down in 1 second."}]'
sleep 1
rcon.py stop
sleep 5
