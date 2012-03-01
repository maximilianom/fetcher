"""
Simple Script which setups a new instance of amazon

It is in charge of:
    - Copying all core process .py files
    - Installing dependences
    - running the fetchers
"""
import os
import random
import time

from fabric.api import run, cd, put, sudo, get

def start():
    _copy_files()
    _install_dependences()
    with cd("/home/ubuntu/process/"):
        run("python SaveInFileHandler.py -t 15")

    _retrieve_files()

def _copy_files():
    with cd("/home/ubuntu/"):
        run("mkdir process")

    put("SaveInFileHandler.py", "/home/ubuntu/process")
    put("crawle.py", "/home/ubuntu/process")

def _install_dependences():
    sudo("easy_install lxml")
    sudo("easy_install pika")

def _retrieve_files():
    #TODO: Add more efficient logic

    # Sleep random time to ensure consistency of the data
    time.sleep(random.randint(1,30))

    for i in range(1,100):
        if not os.path.exists('/home/ubuntu/results/%d' % i):
            os.mkdir('/home/ubuntu/results/%d' % i)
            get('/home/ubuntu/process/Results', '/home/ubuntu/results/%d' % i)
            break
