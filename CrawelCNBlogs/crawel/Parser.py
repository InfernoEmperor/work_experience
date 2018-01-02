import lxml.etree
class Parser:
    def __init__(self,content):
        self.selector = lxml.etree.HTML(content)

    def get_need_array(self,xpath):
        """
        获取xpath返回结果为数组的第一个元素
        :param xpath: 
        :return: 
        """
        if xpath is None:
            raise(Exception('Parser get_need_array argument xpath is None'))
        return self.selector.xpath(xpath)[0]

    def get_need_str(self,xpath,seq = ''):
        '''
        获取xpath结果为字符串类型的数据
        :param xpath: 
        :return: 
        '''
        if xpath is None:
            raise(Exception('Parser get_need_str argument xpath is None'))
        return seq.join(self.selector.xpath(xpath))

