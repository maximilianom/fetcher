import sys


class UrlConverter(object):

    def __init__(self, base_file_name, new_file_name, num):
        self.fileToChange = open(base_file_name, 'r')
        self.fileToWrite = open(new_file_name, 'w')
        self.counter = int(num)

    def mutate(self):
        count = 0
        urls = self.fileToChange.read().split()
        for url in urls:
            if not url.startswith('http://'):
                url = 'http://%s' % url

            self.fileToWrite.write(url + '\n')
            count += 1
            print count
            if count == self.counter:
                break

        self.fileToWrite.close()
        self.fileToChange.close()

if __name__ == '__main__':
    converter = UrlConverter('iframe.log', 'httpiframe', sys.argv[1])
    converter.mutate()









