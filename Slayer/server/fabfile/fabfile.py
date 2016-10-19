from fabric.decorators import task
from fabric.operations import sudo, run


@task
def apt_get_update():
    """
    Runs 'apt-get update' command on remote machine
    """
    sudo('apt-get update')


@task
def apt_get(*packages):
    """
    Runs apt-get install command for all provided packages
    """
    sudo('apt-get -y -f install %s' % ' '.join(packages), shell=False)


@task
def git_pull():
    """
    Updates the repository
    """
    run("cd ~/125/; git pull origin master")


@task
def migrate():
    """
    Make migrations
    """
    run("cd ~/125/; source ./bin/activate; cd web; ./manage.py migrate --settings=web.prod_settings")


@task
def collectstatic():
    run("cd ~/125/; source ./bin/activate; cd web; ./manage.py collectstatic")


@task
def restart():
    """
    Restarts gunicorn & nginx 
    """
    sudo("supervisorctl restart 125; supervisorctl restart celery125; service nginx restart")


@task
def open_shell():
    """
    Opens shell
    """
    run("cd ~/125/; source ./bin/activate; cd web; ./manage.py shell --settings=web.prod_settings")


@task
def start_celery():
    """
    Script for starting celery
    """
    run("cd ~/125/; source ./bin/activate; cd web; celery -A web worker -l info")


