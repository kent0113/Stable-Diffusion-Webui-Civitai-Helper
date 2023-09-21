import os

modules_path = os.path.dirname(os.path.realpath(__file__))
current_basedir = os.path.dirname(modules_path)


def basedir():
    """returns the base directory for the current script. For scripts in the main scripts directory,
    this is the main directory (where webui.py resides), and for scripts in extensions directory
    (ie extensions/aesthetic/script/aesthetic.py), this is extension's directory (extensions/aesthetic)
    """
    return current_basedir
