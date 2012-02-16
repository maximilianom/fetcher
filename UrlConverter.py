
class UrlConverter(object):

    def __init__(self, base_file_name):
        self.fileToChange = open(base_file_name, 'r')

    def mutate(self):
        count = 0
        fp = open("urls.txt", "w")
        urls = self.fileToChange.read().split()
        for url in urls:
            if not url.startswith('http://'):
                url = 'http://%s' % url

            fp.write(url + '\n')
            count += 1
            print count

        fp.close()
        self.fileToChange.close()

if __name__ == '__main__':
    converter = UrlConverter('error.csv')
    converter.mutate()









