import requests
import lxml.etree
import urllib.parse
import time
import hashlib
import logging
from SQL.connect_sqlserver import MYSQL

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                        datefmt='%Y-%m-%d %A %H:%M:%S',
                        filename='log.log',
                        filemode='w')

url = 'http://www.kejilie.com/'
host = r'192.168.3.152:4000'
user = 'sa'
passd = '123.abc'
database = 'BaseData2017'
sqlserver = MYSQL(host,user,passd,database)

def get_content_url(url):
    try:
        res = requests.get(url)
    except Exception as e:
        logging.error('function get_content_url raise error:',e)
        logging.info('function get_content_url  get url again!!!')
        try:
            res = requests.get(url)
        except Exception as e:
            logging.error('function get_content_url get url error again:',e)
            logging.info('except exit!')
            exit()
    html = lxml.etree.HTML(res.text)
    url_lst = html.xpath('//h3/a/@href')
    now_url =set()
    for url in url_lst:
        sql = "select count(1) from BaseData2017.dbo.ArticleCrawler where Url='%s'"%url
        res = sqlserver.ExecQuery(sql)[0][0]
        if not res:
            now_url.add(url)
    logging.info('get url access!')
    return now_url

def get_content(content_url):
    try:
        res = requests.get(content_url)
    except Exception as e:
        logging.error('function get_content raise error:',e)
        logging.info('function get_content  get content_url again!!!')
        try:
            res = requests.get(content_url)
        except Exception as e:
            logging.error('function get_content get content_url error again:',e)
            logging.info('except exit!')
            exit()
    content = lxml.etree.HTML(res.text)
    return content

def get_text(content):
    try:
        html = content.xpath('//article/div[@class="so-content"]')[0]
    except:
        logging.info('function get_text xpath result is None!')
        return ''

    html = lxml.etree.tostring(html,method='html',encoding='utf-8')
    return html.decode('utf-8').replace("'",'"')

def get_resource_link(content):
    """
    :param content: 
    :return: 原文链接
    """
    try:
        link = content.xpath('//*[@title="原文"]//@href')[0]
    except:
        logging.info('function get_resource_link xpath result is None!')
        return None
    return link

def get_resource_name(content):
    """
    :param content: 
    :return 来源名称 
    """
    try:
        name = content.xpath('//article/div[1]/a[1]/span/text()')[0]
    except:
        logging.info('function get_resource_name xpath result is None!')
        return None
    return name

def get_publish_time(content):
    """
    :param content: 
    :return 发表时间: 
    """
    try:
        pub_time = content.xpath('//article/div[1]/span/time/@title')[0]
    except:
        logging.info('function get_publish_time xpath result is None!')
        return None
    return pub_time

def get_tag(content):
    """
    :param content: 
    :return 标签: 
    """
    tag = content.xpath('//article/a/span/text()')
    tag = ','.join(tag)
    return tag

def get_title(content):
    try:
        title = content.xpath('//article/h1/text()')[0]
    except:
        logging.info('function get_title xpath result is None!')
        return None
    return title

def get_resource_link(content):
    try:
        link = content.xpath('//*[@title="原文"]/@href')[0]
    except:
        logging.info('function get_resource_link xpath result is None!')
        return None
    return link

def push_sql(content):
    html_text = get_text(content)
    resource_name = get_resource_name(content)
    pub_time = get_publish_time(content)
    title = get_title(content)
    tag = get_tag(content)
    link = get_resource_link(content)
    eng_name = urllib.parse.urlsplit(content_url).path.split('/')[1]

    #构造md5
    m = hashlib.md5()
    m.update(content_url.encode('utf-8'))
    url_id = m.hexdigest()

    data = {
        'Url': content_url,
        'Url_id': url_id,
        'Source': '科技猎',
        'Title': title,
        'Author': resource_name,
        'Content': html_text,
        'Keywords': tag,
        'PublishTime': pub_time,
        'IsClean': 0,
        'SourceType': resource_name,
        'Account': eng_name,
        'AccountUrl': link,
        'Comments': 0,
        'Favorites': 0,
        'ReadCounts': 0,
    }
    try:
        sql = 'INSERT INTO [BaseData2017].[dbo].[ArticleCrawler] ([Url], [Url_id],[Source], [Title], [Author], [Content], [Keywords], [PublishTime], [IsClean], [SourceType], [Account], [AccountUrl],[Comments], [Favorites], [ReadCounts]) VALUES (' + "'" + \
              data["Url"] + "','" + data["Url_id"] + "','" + data["Source"] + "','" + data["Title"] + "','" + data[
                  "Author"] + "','" + data["Content"] + "','" + data["Keywords"] + "','" + \
              data["PublishTime"] + "'," + str(data["IsClean"]) + ",'" + data["SourceType"] + "','" + data[
                  "Account"] + "','" + data['AccountUrl'] + "'," + str(data["Comments"]) + "," + str(
            data["Favorites"]) + "," + str(
            data["ReadCounts"]) + ');'
        sqlserver.ExecNoQuery(sql)
    except:
        logging.error('function push_sql insert '+ sql +'error!')


if __name__ == '__main__':
    while True:
        url_lst = get_content_url(url)
        for content_url in url_lst:
            content= get_content(content_url)
            push_sql(content)
            time.sleep(5)
        time.sleep(120)