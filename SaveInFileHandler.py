import os
import sys
import urlparse

import lxml.html
import crawle

class SaveInFileHandler(crawle.Handler):
    """
    This should imitate previos fetcher
    """

    def __init__(self, path, max_files=20000):
        """
            parameters:
            - path_to_save
            - max_files: max amount of files you allow on folder
            - folder_index: to keep track of how many folders were made
            - err_log
        """
        self.path_to_save = path
        self.max_files = max_files
        self.folder_index = 1
        if os.path.exists('%s/%d' % (self.path_to_save, self.folder_index)):
            print "You're trying to write over an existing file"
            sys.exit(1) # Better this than overwrite some important data
        else:
            os.makedirs('%s/%d' % (self.path_to_save, self.folder_index))
            self.err_log = open('%s/err.log' % self.path_to_save, 'a')
            self.processed_log = open('%s/proccessed.log' % self.path_to_save, 'a')
            self.wrong_frame = open('%s/wrong_frame.log' % self.path_to_save, 'a')


    def _get_frame_content(self, req_res):
        dom = lxml.html.document_fromstring(req_res.response_body)

        if dom.xpath('/html/body/iframe/@src') :
           return dom.xpath('/html/body/iframe/@src')[0]

        elif dom.xpath(".//frame/@src") :
           return dom.xpath(".//frame/@src")[0]

        return None

    def _get_file_name(self, req_res):
        """
        Calculates the name of the directory depending on the actual folder_index
        and the amount of files in that directory. If it reaches more than allowed,
        it creates another folder
        """
        files_amount = len(os.listdir('%s/%d/' % (self.path_to_save, self.folder_index)))
        if files_amount > 20000:
            self.folder_index += 1
            os.makedirs('%s/%d' % (self.path_to_save, self.folder_index))

        return '%s/%d/%d%s' % (self.path_to_save,
                               self.folder_index,
                               self.folder_index,
                               req_res.name)


    def process(self, req_res, queue):
        """
        Main process extended method to process response after doing the
        http request
        """
        if not req_res.response_status:
            print "Unexepected error in: %s. Error: %s" % (req_res.response_url,
                                                           req_res.error)
            print >> self.err_log, req_res.name
            return

        if req_res.response_status != 200:
            req_res.retries -= 1
            if req_res.retries <= 0 or req_res.response_status == 404:
                print "Discarding this url: %s" % req_res.name
                print >> self.err_log, req_res.name
            else:
                queue.put(req_res)
        else:

            try:
                iframe_url = self._get_frame_content(req_res)
            except Exception, e:
                print "Failed to get frame content"
                print >> self.err_log, req_res.name
                return

            if iframe_url:
                #It has frame. Should we try again with that url?
#                _,netloc,_,_,_,_ = urlparse.urlparse(iframe_url)
#                if netloc == '':
#                    print "URL INVALIDA!"
#                    print >> self.wrong_frame, iframe_url
#                    print >> self.processed_log, req_res.name
#                    file = open(self._get_file_name(req_res), 'w')
#                    file.write(req_res.response_body)
#                    file.close()
#                    return

                if req_res.retries <= 0:
                    print "Too many retries for this one: %s" % req_res.name
                    print >> self.err_log, req_res.name
                else:
                    print "Frame detected, putting %s back in queue" % req_res.name
                    parsed = urlparse.urlparse(iframe_url)
                    req_res.response_url = iframe_url
                    req_res.retries -= 1
                    queue.put(req_res)
            else:
                try:
                    file = open(self._get_file_name(req_res), 'w')
                    file.write(req_res.response_body)
                    file.close()
                except Exception, e:
                    print "Exception while trying to write fetched result of: %s" % e
                    print "Writing url in err.log"
                    print >> self.err_log, req_res.name
                    return
                print >> self.processed_log, req_res.name
                print "Success for %s" % req_res.name

if __name__ == "__main__":
    crawle.run_crawle(sys.argv, handler=SaveInFileHandler('./Things'))


