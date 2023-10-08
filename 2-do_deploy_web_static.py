#!/usr/bin/python3
from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['52.3.241.118', '54.173.33.44']
env.user = 'ubuntu'


def do_pack():
    """
    Creates a .tgz file from the content of the web_static directory.
    """
    now = datetime.now()
    time = now.strftime("%Y%m%d%H%M%S")
    name = "versions/web_static_" + time + ".tgz"

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
    if os.path.exists(archive_path):

        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True
    return False
