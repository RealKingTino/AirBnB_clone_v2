#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os.path

"""generates a .tgx file"""


def do_pack():
    """Generates a .tgz file"""
    now = datetime.now()
    time = now.strftime("%Y%m%d%H%M%S")
    name = "versions/web_static_" + time + ".tgz"

    if not os.path.exists("versions"):
        local("mkdir -p versions")

    stat = local("tar -cvzf {} web_static".format(name))

    if stat.succeeded:
        return name
    else:
        return None
