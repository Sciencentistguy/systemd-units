#!/bin/python
import argparse
import os
import sys

from mcrcon import MCRcon


parser = argparse.ArgumentParser()

parser.add_argument("--port", "-p", type=int, help="The RCON port of the server")
parser.add_argument("--url", "-u", type=str, help="The IP or URL of the server")
parser.add_argument("--password", "-p", type=str, help="The RCON password of the server")
parser.add_argument("command", type=str, nargs="+", help="The command to run")
cmd_args = parser.parse_args()

url = os.getenv("MC_SERVER_ADDR")
if cmd_args.url is not None:
    url = cmd_args.url

port = os.getenv("MC_SERVER_RCON_PORT")
if cmd_args.port is not None:
    url = cmd_args.port
if port is None:
    port = 25575

password = os.getenv("MC_SERVER_RCON_PASS")
if cmd_args.password is not None:
    url = cmd_args.password

if password is None:
    raise RuntimeError("A password is required")

if url is None:
    raise RuntimeError("A url is required")


with MCRcon(url, password, port) as rc:
    print(" ".join(sys.argv[1:]))
    resp = rc.command(" ".join(sys.argv[1:]))
    print(resp)
