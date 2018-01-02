from crawel.DownLoader import DownLoader
from crawel.URLManager import URLManager
from crawel.Parser import Parser
from crawel.SaveData import SaveData
import urllib.parse
import time
import hashlib
import lxml.etree
import logging
from Email.Email import send_mail

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                        datefmt='%Y-%m-%d %A %H:%M:%S',
                        filename='log.log',
                        filemode='a')

URL = 'https://news.cnblogs.com/'

def get_urls():
    try:
        urls = DownLoader.get_urls(URL, '//*[@class="news_block"]//div[@class="content"]//h2/a/@href')
    except Exception as e:
        logging.error(e)
        logging.info('The format of the website may have been changed, please debug the inspection procedure!')
        send_mail('Online program error','Get the blog garden program error, please deal with it!')
        exit()
    for i in range(len(urls)):
        urls[i] = urllib.parse.urljoin(URL, urls[i])
    return urls

def get_html(url):
    html = DownLoader.get_html(url)
    return html

def task():
    # 得到urls
    urls = get_urls()
    # 加入urls的管理
    urlManage = URLManager()
    urlManage.add_new_urls(urls)
    # 开始下载
    count = 0
    while urlManage.new_url_size() > 0:
        url = urlManage.get_new_url()
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        url_md5 = m.hexdigest()
        try:
            html = get_html(url)
            parser = Parser(html)
            title = parser.get_need_str('//*[@id="news_title"]//text()')
            Author = parser.get_need_str('//*[@id="come_from"]//text()')
            Author = Author.replace('\t','').replace('来自:','').replace('\r','').replace('\n','')
            content = lxml.etree.tostring(parser.get_need_array('//*[ @ id = "news_body"]'),method='html',encoding='utf-8').decode('utf-8').replace("'",'"')
            keywords = parser.get_need_str('//*[@id="news_more_info"]/div/a//text()',seq=',')
            pub_time = parser.get_need_str('//*[@id="news_info"]/span[@class="time"]/text()').replace('发布于 ','')
            Source = Author
            Account_url = parser.get_need_str('//*[@id="link_source1"]/@href')
            Account = urllib.parse.urlsplit(Account_url).netloc.split('.')
            Account = Account[1] if len(Account) > 2 else Account[0]
            urllib.parse.urlsplit(url)
            id = urllib.parse.urlsplit(url).path.split('/')[-2]
            view_url = "https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=" + str(id)
            dct = eval(DownLoader.get_html(view_url))
            status = 0
            count = 0
        except Exception as e:
            logging.info(e)
            count += 1
            if count == 10:
                logging.info('The format of the website may have been changed, please debug the inspection procedure!')
                send_mail('Online program error', 'Get the blog garden program error, please deal with it!')
                exit()
            continue

        data = {
            'Url' : url,
            'Url_id' : url_md5,
            'Source' : '博客园',
            'Title' : title,
            'Author' : Author,
            'Content': content,
            'Keywords' : keywords,
            'PublishTime' : pub_time,
            'IsClean' : 0,
            'SourceType' : Source,
            'Account' : Account,
            'AccountUrl' : Account_url,
            'Comments' : dct["CommentCount"],
            'Favorites' : dct["BuryCount"],
            'ReadCounts' : dct["TotalView"],
            'Status' : status
        }
        sa = SaveData()
        try:
            sa.save(data)
        except Exception as e:
            if e.args[0] == 1:
                logging.info('database record repeat!')
            else:
                logging.error('Database inserts fail and not repeat! Program exit, send mail!')

        time.sleep(5)

if __name__ == '__main__':
    while True:
        task()
        time.sleep(120)
