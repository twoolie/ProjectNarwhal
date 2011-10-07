from fabric.api import *
import platform
from os.path import join

@task
def dev_serve():
    with prefix('Scripts\\activate.bat' if platform.system()=="Windows" else 'source bin/activate'):
        local(join('compass watch example_project','static &'))
        local(join('python example_project','manage.py runserver'))

@task
deploy_epio(appname):
    """ fab deploy_epio:appname """
    env['appname']=appname
    lcd('example_project'), prefix('Scripts\\activate.bat' if platform.system()=="Windows" else 'source bin/activate'):
        local('python manage.py rebuild_solr_index')
        local('python manage.py collectstatic --no-input')
        local( ('mklink /D %(link)s %s(target)'
                if platform.system()=="Windows"
                else 'ln -s %(target)s %(link)s') % { 'link':'narwhal', 'target':'../narwhal' }
        local('epio upload -a %(appname)s'%env)
        local('epio django syncdb -a %(appname)s'%env)
        local('epio django migrate -a %(appname)s'%env)