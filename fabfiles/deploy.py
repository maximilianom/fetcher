"""
Simple Script which deploys the main application into production

Usage:
    fab -i ~/.ssh/amazon_id -u ubuntu -f deploy.py -H *Host de amazon* run
"""


from fabric.api import run, put, cd

def run():
    pass
