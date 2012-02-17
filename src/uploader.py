"""
This has to upload and deploy everything, and also run ec2 instances
"""
#TODO: reservation.instances.public_dns_name
import logging
import threading

from boto.ec2.connection import EC2Connection

logging.basicConfig(level='DEBUG')

AWS_ACCESS_KEY=''
AWS_SECRET_KEY=''
AMI_ID=''
KEY_NAME=''
TYPE=''
SECURITY_GROUP=''

class UploaderHandler(object):
    """
    This class will handle everything that has to do with deploying and
    uploading the fetching core process content, and creating the necessary
    ec2 instances
    """

    log = logging.getLogger(__name__)

    def __init__(self, instance_num):
        self.threads = []
        self.instance_num = instance_num

        self.log.info("Connecting to EC2 server...")
        self.conn = EC2Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)


    def upload(self):
        for i in range(0, self.instance_num):
            self.launch_ec2_instance()
            self.log.info("Starting deploy process #%d...", i)
            deployer = Deployer(i) #TODO: add ip, and other parameters
            deployer.start()
            self.threads.append(deployer)

    def launch_ec2_instance(self):
        self.conn.run_instances(AMI_ID,
                                key_name=KEY_NAME,
                                instance_type=TYPE,
                                security_groups=[SECURITY_GROUP])

    def stop(self):
        #TODO:AVERIGUAR ESTO
        #Terminate instances
        pass

    def wait(self):
        for thread in self.threads:
            thread.join()


class Deployer(threading.Thread):
    """
    Responsible of passing the core files to destination ip using fabric
    """

    def __init__(self, name, host):
        threading.Thread.__init__(self)

        self.name = name
        self.host = host


    def run(self):
        self.log.info("%d - running remote fabric deploy script", self.name)
