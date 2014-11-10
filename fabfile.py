from fabric.api import local
from fabric.colors import green


def build():
    print(green("=====[ Installing Bowering Components ]====="))
    local('bower install --allow-root --config.interactive=false')
    print(green("\n=====[ Syncing Database ]====="))
    local('./src/manage.py syncdb --noinput')
    print(green("\n=====[ Running Database Migrations ]====="))
    local('./src/manage.py migrate')
    print(green("\n=====[ Loading Fixtures ]====="))
    local('./src/manage.py loaddata texas.json')
    local('./src/manage.py loaddata licenses.json')
    local('./src/manage.py loaddata palettes.json')
