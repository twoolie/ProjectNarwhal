from fabric.api import *
from fabric.contrib import files
import platform
from os.path import join
from argparse import ArgumentError

env.hosts = ['your_username@yourhost:yourport']
env.web_path = '/var/www/django'
env.log_root ='/var/log/apache'
env.project = 'example_project'

@task
def dev_serve():
    with prefix('Scripts\\activate.bat' if platform.system()=="Windows" else 'source bin/activate'):
        local(join('compass watch %(project)s','static &') % env)
        local(join('python %(project)s','manage.py runserver') % env)

@task
def bootstap_dev():
    """ Bootstrap your local development environment """
    local('git clone https://github.com/twoolie/ProjectNarwhal.git')
    with lcd('ProjectNarwhal'):
        local('virtualenv --distribute .')
        with prefix('Scripts\\activate.bat' if platform.system()=="Windows" else 'source bin/activate'):
            local('pip install -r requirements.txt')
            local(join('python %(project)s','manage.py syncdb --all') % env)
            local(join('python %(project)s','manage.py migrate --fake') % env)

@task
def bootstrap(hostname, path=env.web_path, **kwargs):
    """ Creates a virtualhost instance on the box you specify 
        `fab -H server1,server2 bootstrap:narwhal.example.com[,deploy_options...]` """
    
    run('mkdir -p %(path)s/%(hostname)s/' % locals())
    with cd('%(path)s/%(hostname)s/' % locals()):
        run('git init .')
    
    locals().update(kwargs)
    deploy(**locals()) # deploy script takes care of the rest

@task
def deploy(hostname, ref='master', path=env.web_path, apache_conf_path=None, distro=None, \
           log_root=env.log_root, thread_count=2, process_count=4):
    """ `fab -H server1,server2 deploy:narwhal.example.com` """
    if not apache_conf_path: apache_conf_path=find_apache_path(distro)
    
    local('git push -f ssh://%(host_string)s/%(path)s/%(hostname)s/ %(ref)s' % locals())
    with cd('%(path)s/%(hostname)s' % locals()):
        run('git checkout -f %(ref)s' % locals())
        run('pip install -r requirements.txt')
        with cd(env.project):
            files.upload_template('apache.conf', apache_conf_path+hostname,
                                  context=locals(), mode=0755, use_sudo=True)
            run('./manage.py collectstatic --noinput')
            run('./manage.py syncdb')
            run('./manage.py migrate')
            run('touch serve.wsgi') # restart the wsgi process

@task
def deploy_epio(appname):
    """ fab deploy_epio:appname """
    with lcd(env.project), prefix('Scripts\\activate.bat' if platform.system()=="Windows" else 'source bin/activate'):
        local('python manage.py collectstatic --noinput')
        local( ('mklink /D %(link)s %s(target)' if platform.system()=="Windows" else 'ln -s %(target)s %(link)s') \
                    % { 'link':'narwhal', 'target':'../narwhal' })
        local('python manage.py build_solr_schema > solr_schema.xml')
        local('epio upload -a %(appname)s'%locals())
        local('epio django syncdb -a %(appname)s'%locals())
        local('epio django migrate -a %(appname)s'%locals())
        local('epio django rebuild_index')


#-------- Utils ----------

def _join(*args):
    return "/".join(args)

def find_apache_path(distro):
    if not distro:
        distro = run('python -c "import platform; print platform.dist()[0]"')
    if distro in ('debian', 'ubuntu'):
        return '/etc/apache2/sites-enabled/'
    else:
        raise ArgumentError('Cannot automatically determine apache_conf_path')
