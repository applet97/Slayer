from fabric.decorators import task
from fabric.state import env

import common
import docker
import install

env.repository = "https://github.com/applet97/Slayer.git"
env.user = "ubuntu"
env.hosts = ["18.195.8.85"]
env.key_filename = "~/slayer.pem"
env.filename = "docker-compose.yml"