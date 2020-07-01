# Minecraft server administration scripts
A collection of scripts related to administration of minecraft servers
## rcon.py
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
* Syntax:
    * `rcon.py <command...>`
    * In `<command>`, spaces do not need to be escaped.

