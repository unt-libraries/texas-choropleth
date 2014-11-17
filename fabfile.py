from fabric.api import local, run
from fabric.colors import green, blue
from fabric.contrib import django
from fabric.decorators import task
from fabric.state import output

output['running'] = False

@task
def local_manage(param=''):
    """
    A wrapper for executing Django commands from the docker host or client.
    """
    local('fig run --rm web ./src/manage.py {0}'.format(param))


@task
def manage(param=''):
    """
    Wrapper for Django commands.
    """
    local('./src/manage.py {0}'.format(param))


@task
def run_tests(test='src'):
    """
    Wrapper for running tests.
    """
    django.settings_module('texas_choropleth.settings.test')
    local('./src/manage.py test {0}'.format(test))


def build():
    """
    Base function for building the application.
    """
    print(blue("\n[ Syncing Database ]"))
    local('./src/manage.py syncdb --noinput')
    print(green(">[DONE]\n"))

    print(blue("\n[ Running Database Migrations ]"))
    local('./src/manage.py migrate')
    print(green(">[DONE]\n"))

    print(blue("\n[ Loading Fixtures ]"))
    local('./src/manage.py loaddata texas.json')
    local('./src/manage.py loaddata palettes.json')
    print(green(">[DONE]\n"))

    print(blue("\n[ Installing Node Modules ]"))
    local('npm install --silent')
    print(green(">[DONE]\n"))

    print(blue("\n[ Installing Bowering Components ]"))
    local('npm run postinstall --silent')
    print(green(">[DONE]\n"))


@task
def build_dev():
    """
    Build the application for a development environment.
    """
    django.settings_module('texas_choropleth.settings.local')
    build()


@task
def build_prod():
    """
    Build the application for the production environment.
    """
    django.settings_module('texas_choropleth.settings.production')
    build()

    print(blue("\n [ Collecting Staticfiles ]"))
    local('./src/manage.py collectstatic --noinput')
    print(green(">[DONE]\n"))
