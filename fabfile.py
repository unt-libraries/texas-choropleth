from fabric.api import local


def build():
    local('bower install --allow-root --config.interactive=false')
    local('./src/manage.py syncdb --noinput')
    local('./src/manage.py migrate')
    local('./src/manage.py loaddata texas.json')
    local('./src/manage.py loaddata licenses.json')
    local('./src/manage.py loaddata palettes.json')
