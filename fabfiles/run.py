"""
Simple Script which setups a new instance of amazon

It is in charge of:
    - Copying all core process .py files
    - Installing dependences
    - running the fetchers
"""

from fabric.api import run, cd, put, sudo

def start():
    _copy_files()
    _install_dependences()
    with cd("/home/ubuntu/process/"):
        run("python SaveInFileHandler.py -t 15 -s urls.txt")

def _copy_files():
    with cd("/home/ubuntu/"):
        run("mkdir process")

    #TODO: Add local path to files to copy
    put("", "/home/ubuntu/process")
    put("", "/home/ubuntu/process")

def _install_dependences():
    sudo("easy_install lxml")
    sudo("easy_install pika")
