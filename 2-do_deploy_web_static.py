#!/usr/bin/python3
''' point 1 create tgz '''
import os
from os.path import isfile
import datetime
from fabric.api import local, env, put, run
''' os.paht = routes to directories and files, create folders '''
''' fabric.api = create tgz files '''
''' datetime = in order to get current date and time '''


env.hosts = ['35.231.52.206', '54.226.104.83']
env.user = 'ubuntu'


def do_pack():
    ''' function to pack in tgz file '''
    if not os.path.exists('./versions'):
        os.mkdir('versions')
    if os.path.exists('./web_static'):
        now = datetime.datetime.now()
        b = "web_static_"
        ny = now.year
        nm = now.month
        nd = now.day
        nh = now.hour
        nmi = now.minute
        ns = now.second
        e = ".tgz"
        n = "{}{}{}{}{}{}{}{}".format(b, ny, nm, nd, nh, nmi, ns, e)
        tgzfile = local('tar -cvzf versions/{} web_static'.format(n))
        if tgzfile.failed:
            return None
        return 'versions/{}'.format(n)


def do_deploy(archive_path):
    ''' function to deploy archive '''
    if not isfile(archive_path):
        return False
    else:
        put("{}".format(archive_path), "/tmp/")
        n = archive_path
        n = n.replace("versions/", "")
        n = n.replace(".tgz", "")
        run('mkdir -p /data/web_static/releases/{}/'.format(n))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/\
'.format(n, n))
        run('rm /tmp/{}.tgz'.format(n))
        run('mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}/'.format(n, n))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(n))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current\
'.format(n))
        print("New version deployed!")
        return True
