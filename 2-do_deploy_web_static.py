#!/usr/bin/python3
from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['52.3.241.118', '54.173.33.44']
env.user = 'ubuntu'
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers using the do_deploy function.
    """
    try:
        if not os.path.isfile(archive_path):
            return False
        put(archive_path, "/tmp/")
        archived_file = os.path.basename(archive_path)
        newest_version = "/data/web_static/releases/{}".format(archived_file[:-4])
        run("rm -rf {}".format(newest_version))
        run("mkdir -p {}".format(newest_version))
        run("tar -xzf /tmp/{} -C {}".format(archived_file, newest_version))
        run("rm /tmp/{}".format(archived_file))
        run("mv {}/web_static/* {}/".format(newest_version, newest_version))
        run("rm -rf {}/web_static/".format(newest_version))
        run("rm -rf /data/web_static/current")
        run("ln -sf {} {}".format(newest_version, "/data/web_static/current"))
    except Exception:
        return False

    return True
