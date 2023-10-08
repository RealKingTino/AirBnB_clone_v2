#!/usr/bin/python3
from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = ['/path/to/your/ssh/key']  # Replace with your SSH key path

def do_pack():
    """
    Creates a .tgz file from the content of the web_static directory.
    """
    now = datetime.now()
    time = now.strftime("%Y%m%d%H%M%S")
    name = "versions/web_static_" + time + ".tgz"
    if os.path.isdir("versions") is False:
        local("mkdir -p versions")

    stat = local("tar -cvzf {} web_static".format(name))
    if stat.succeeded:
        return name
    else:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers using the do_deploy function.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.replace('.tgz', '').replace('web_static_', '')
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_filename, folder_name))

        run('rm /tmp/{}'.format(archive_filename))

        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))

        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        run('rm -rf /data/web_static/current')

        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
