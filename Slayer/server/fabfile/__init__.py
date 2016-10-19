import fabfile

from fabric.decorators import task
from fabric.state import env

env.repository = "https://github.com/aibaq/slayer.kz"
env.user = "user_125"
env.hosts = ["195.16.90.30"]
#env.key_filename = "~/iDocs.pem"
#env.filename = "docker-compose.yml"

@task
def prod():
    """
    ! DON'T USE ! Sets kz environment.
    """
    env.hosts = ["195.16.90.30"]
    env.user = "user_125"
    env.key_filename = None
    env.password = "1590751"

