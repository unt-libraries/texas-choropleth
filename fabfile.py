from fabric.api import local, run
from fabric.colors import green
from fabric.contrib import django
from fabric.decorators import task


@task
def run_tests(test='src'):
    django.settings_module('texas_choropleth.settings.test')
    local('./src/manage.py test {0}'.format(test))


def build():
    print(green("[ Installing Bowering Components ]"))
    local('bower install --allow-root --config.interactive=false')

    print(green("\n[ Syncing Database ]"))
    local('./src/manage.py syncdb --noinput')

    print(green("\n[ Running Database Migrations ]"))
    local('./src/manage.py migrate')

    print(green("\n[ Loading Fixtures ]"))
    local('./src/manage.py loaddata texas.json')
    # local('./src/manage.py loaddata licenses.json')
    local('./src/manage.py loaddata palettes.json')


@task
def build_dev():
    django.settings_module('texas_choropleth.settings.local')
    build()


@task
def build_prod():
    django.settings_module('texas_choropleth.settings.production')
    build()

    print(green("\n [ Collecting Staticfiles ]"))
    local('./src/manage.py collectstatic --noinput')
