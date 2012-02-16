import time
import threading

import pika
from pika.adapters import BlockingConnection

pika.log.setup(color=True)

class BlockingReader(threading.Thread):
    def __init__(self, host, queue):
        threading.Thread.__init__(self)

        self.queue = queue
        self.parameters = pika.ConnectionParameters(host)
        pika.log.info("Establishing connection")
        self.connection = BlockingConnection(self.parameters)

        self.channel = self.connection.channel()
        pika.log.info("About to declare queue")

        self.channel.queue_declare(queue="test", durable=True,
                                   exclusive=False, auto_delete=False)
        pika.log.info("Queue declared")

    def read(self):
        pika.log.info("Reading single message")
        method, header, body = self.channel.basic_get(queue=self.queue)
        pika.log.info("Message received!")
        pika.log.info("Body: %s" % body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(3)

    def run(self):
        while self.connection.is_open:
            self.read()

    def stop(self):
        self.connection.close()



if __name__ == "__main__":
    threads = []
    for num in range(0,3):
        threads.append(BlockingReader('localhost', 'test'))

    for thread in threads:
        thread.start()

    time.sleep(40)
    for thread in threads:
        thread.join()

