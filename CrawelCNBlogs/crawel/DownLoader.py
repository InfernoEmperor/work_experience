import requests
import lxml.etree

class DownLoader:
    @staticmethod
    def get_urls(url,xpath = None):
        try:
            html = requests.get(url)
            selector = lxml.etree.HTML(html.text)
            urls = selector.xpath(xpath)
        except:
            raise (Exception('DownLoader get_urls error!'))
        return urls

    @staticmethod
    def get_html(url):
        try:
            html = requests.get(url)
        except:
            raise (Exception('DownLoader get_html error!'))
        return html.text
