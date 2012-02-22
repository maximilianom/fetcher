from fabric.api import run, cd

def start():
    cd("/home/ubuntu/process/")
    run("python -t 15 -s urls.txt")
