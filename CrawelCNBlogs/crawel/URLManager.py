import hashlib

class URLManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    def has_new_url(self):
        return self.new_url_size() != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        m =hashlib.md5()
        m.update(new_url.encode('utf-8'))
        if self.old_url_size() > 60:
            self.old_urls.pop()
        self.old_urls.add(m.hexdigest())
        return new_url

    def add_new_url(self,url=None):
        if url is None:
            raise(Exception('url is None'))
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        url_md5 = m.hexdigest()
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)


    def add_new_urls(self,urls):
        if urls is None or len(urls)== 0:
            raise(Exception('urls is None'))
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)