from fabric.api import local

def deploy():
    local("scp -i ~/.ssh/id_mtengine /home/mmendez/para_amazon ubuntu@ec2-107-20-5-105.compute-1.amazonaws.com:/home/ubuntu/")




