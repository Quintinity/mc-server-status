from mcstatus import MinecraftServer
from flask import Flask
from jinja2 import Template
import socket
import sys

EXTERNAL_HOSTNAME = "forge.vladmarica.com"
MC_SERVER_HOST = "127.0.0.1"
MC_SERVER_PORT = 25565

template = None
with open("page.jinja") as template_file:
    template = Template(template_file.read())

app = Flask(__name__)

@app.route("/")
def main():
    server_online = True
    query = None

    # Do a quick port check to see if something is running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((MC_SERVER_HOST, MC_SERVER_PORT))
    s.close()

    if result > 0:
       server_online = False
    else:
        mc_server = MinecraftServer.lookup(MC_SERVER_HOST + ":" + str(MC_SERVER_PORT))
        query = mc_server.query()

    return template.render(hostname=EXTERNAL_HOSTNAME, online=server_online, query=query)

app.run(host="0.0.0.0", port=80)
