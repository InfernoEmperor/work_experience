import requests
import lxml.etree

url = 'http://www.kejilie.com/'

def get_content_url(url):
    try:
        res = requests.get(url)
    except Exception as e:
        print('get url error:',e)
    html = lxml.etree.HTML(res.text)
    url_lst = html.xpath('//h3/a/@href')
    return url_lst

def get_content(content_url):
    res = requests.get(content_url)
    content = lxml.etree.HTML(res.text)
    return content

def get_resource_link(content):
    """
    :param content: 
    :return: 原文链接
    """
    link = content.xpath('//*[@title="原文"]//@href')[0]
    return link

def get_resource_name(content):
    """
    :param content: 
    :return 来源名称 
    """
    name = content.xpath('//article/div[1]/a[1]/span/text()')[0]
    return name

def get_publish_time(content):
    """
    :param content: 
    :return 发表时间: 
    """
    pub_time = content.xpath('//article/div[1]/span/time/@title')[0]
    return pub_time

def get_tag(content):
    """
    :param content: 
    :return 标签: 
    """
    tag = content.xpath('//article/a/span/text()')
    tag = ','.join(tag)
    return tag

if __name__ == '__main__':
    url_lst = get_content_url(url)
    for content_url in url_lst:
        content = get_content(content_url)
        original_link = get_resource_link(content)
        resource_name = get_resource_name(content)
        pub_time = get_publish_time(content)
        tag = get_tag(content)
        resource = "科技猎"
        if requests.get(original_link):
            status = 1   #表示可用
        else:
            status = 0
        result = {'OrgLink':original_link,'SourceName':resource_name,'PostTime':pub_time,'resource':resource,'Tag':tag,'Status':status}
        print(result)


