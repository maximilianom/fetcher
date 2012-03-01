"""
This module contains the behaviour of both the uploader and
writer module. It should be replaced with a django view later on.
"""

import logging
import os

from optparse import OptionParser

from uploader import UploaderHandler
from writer import WriterHandler

class Fetcher(object):

    #TODO: Add handlers and proper logger configuration
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.addHandler(sh)

    def __init__(self, queue_name, host="localhost"):
        self._queue_name = queue_name
        self._host = host

    def fetch(self, seed_content):
        """
        Main method that should be called from outside
        """
        self.log.info("Initiating both uploader and writer handlers.")
        try:
            os.makedirs('../Results')
            writer = WriterHandler(self._host, self._queue_name, seed_content=seed_content)
            #This uploader will raise a default of 2 amazon instances for fetching purposes
            uploader = UploaderHandler()

            self.log.info("Starting writer task.")
            writer.start()

            self.log.info("Starting uploader task.")
            uploader.start()

            self.log.info("Waiting for uploader to finish.")
            uploader.wait()

            self.log.info("Stopping uploader.")
            uploader.stop()
        #TODO: Change exception handling
        except Exception, e:
            self.log.error("Couldn't process. e: %s", e)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-n", '--host-name', dest="host_name", default="localhost")
    parser.add_option("-q", '--queue-name', dest="queue_name", default="test")
    parser.add_option("-s", "--seed-content", dest="seed_content", default="urls.txt")

    options, args = parser.parse_args()

    fetcher = Fetcher(options.queue_name)
    fetcher.fetch(options.seed_content)
