"""
This has to upload and deploy everything, and also run ec2 instances
"""
#TODO: reservation.instances.public_dns_name
import logging
import threading
import time

from optparse import OptionParser

import boto
from fabric.api import local

logging.basicConfig(level='INFO')

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY  = ''
AMI_ID = ''
KEY_NAME = ''
TYPE = 'm1.small'
SECURITY_GROUP = 'default'

IDENTITY = ''
FABFILE_PATH = ''

class UploadProcessException(Exception):
    def __init__(self, error):
        self._error = error

    def __str__(self):
        return "Could not upload - %s" % self._error


class UploaderHandler(object):
    """
    This class will handle everything that has to do with deploying and
    uploading the fetching core process content, and creating the necessary
    ec2 instances
    """

    log = logging.getLogger(__name__)

    def __init__(self, instance_num):
        self.threads = []
        self.instance_ids = []
        self.instance_num = instance_num

        self.log.info("Connecting to EC2 server...")
        try:
            self.conn = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        except Exception, e:
            self.log.error("Unable to connect to amazon. e: %s", e)
            self.stop()
            raise UploadProcessException(e)


    def upload(self):
        """
        Main method that should be called from outside. It launches isntances
        and starts deploying threads
        """
        for i in range(0, self.instance_num):
            instance_dns = self._launch_ec2_instance(i)
            self.log.info("Starting deploy process #%d...", i)
            deployer = Deployer(i, instance_dns)
            deployer.start()
            self.threads.append(deployer)

    def _launch_ec2_instance(self, i):
        try:
            self.conn.run_instances(AMI_ID,
                                    key_name=KEY_NAME,
                                    instance_type=TYPE,
                                    security_groups=[SECURITY_GROUP])
            self.log.info("Started instance. Sleeping for a while.")
            time.sleep(60)

            #Get last reservation "[-1]", and the instance of that reservation
            while True:
                instance = self.conn.get_all_instances()[-1].instances[0]
                if instance.state == 'running':
                    #The instance may be running but not assigned with a dns yet
                    if instance.public_dns_name != '':
                        break
                self.log.info("Not ready yet...")
                time.sleep(10)

            instance.add_tag('Name', 'Fethcer_%d' % i)
            self.instance_ids.append(instance.id)

            return instance.public_dns_name
        except Exception, e:
            self.log.error("Unable to start instance. e: %s", e)
            self.stop()
            raise UploadProcessException(e)

    def stop(self):
        self.log.info("Terminating all #%d instances", len(self.instance_ids))
        self.conn.terminate_instances(instance_ids=self.instance_ids)
        self.conn.close()

    def wait(self):
        for thread in self.threads:
            thread.join()


class Deployer(threading.Thread):
    """
    Responsible of passing the core files to destination ip using fabric
    """

    log = logging.getLogger(__name__)

    def __init__(self, name, host):
        threading.Thread.__init__(self)

        self.name = "Deployer#%d" % name
        self.host = host

    def run(self):
        self.log.info("%s - Letting amazon make its status check on new instance. Sleeping 60s", self.name)
        time.sleep(60)

        self.log.info("%s - starting remote script", self.name)
        local("fab -i %s -f %s -u ubuntu -H %s start" % (IDENTITY, FABFILE_PATH, self.host))


if __name__ == "__main__":
    #Script usage should contain amount of threads to work with
    parser = OptionParser()
    parser.add_option('-i', '--instance-amount', dest="instance_amount", default=1)
    options, args = parser.parse_args()

    uploader = UploaderHandler(int(options.instance_amount))
    uploader.upload()
