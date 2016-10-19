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
    run("cd ~/slayer/; git pull origin master")


@task
def migrate():
    """
    Make migrations
    """
    run("cd ~/slayer/; source ./bin/activate; cd web; ./manage.py migrate --settings=Slayer.prod_settings")


@task
def collectstatic():
    run("cd ~/slayer/; source ./bin/activate; cd web; ./manage.py collectstatic")


@task
def restart():
    """
    Restarts gunicorn & nginx 
    """
    sudo("supervisorctl restart slayer; service nginx restart")


@task
def open_shell():
    """
    Opens shell
    """
    run("cd ~/slayer/; source ./bin/activate; cd Slayer; ./manage.py shell --settings=Slayer.prod_settings")


@task
def start_celery():
    """
    Script for starting celery
    """
    run("cd ~/slayer/; source ./bin/activate; cd web; celery -A web worker -l info")


