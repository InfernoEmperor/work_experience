

import pymssql

class MYSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    def __GetConnect(self):
        if not self.db:
            raise(Exception('没有设置数据库信息'))
        self.conn = pymssql.connect(host = self.host,user = self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (Exception( "连接数据库失败"))
        else:
            return cur

    def ExecNoQuery(self,sql):
        cur = self.__GetConnect()
        # try:
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        # except IntegrityError as e:
        #      self.conn.close()
        #      raise (e)



host = r'192.168.3.152:4000'
user = 'sa'
passd = '123.abc'
database = 'BaseData2017'
sqlserver = MYSQL(host, user, passd, database)

data = {
            'Url' : 'https://news.cnblogs.com/n/585552/',
            'Url_id' : 'caa3df68adfb80ba70d04ef1e01fa493',
            'Source' : '博客园',
            'Title' : '',
            'Author' : '',
            'Content': '',
            'Keywords' : '',
            'PublishTime' : '2017-12-22 09:05:00.000',
            'IsClean' : 0,
            'SourceType' : '',
            'Account' : '',
            'AccountUrl' : '',
            'Comments' : 0,
            'Favorites' : 0,
            'ReadCounts' : 0,
            'Status' : 0
        }

from sqlalchemy.exc import IntegrityError

sql = 'INSERT INTO [BaseData2017].[dbo].[ArticleCrawler] ([Url], [Url_id],[Source], [Title], [Author], [Content], [Keywords], [PublishTime], [IsClean], [SourceType],[Account], [AccountUrl],[Comments], [Favorites], [ReadCounts],[Status]) VALUES (' + "'" + \
                  data["Url"] + "','" + data["Url_id"] + "','" + data["Source"] + "','" + data["Title"] + "','" + data[
                      "Author"] + "','" + data["Content"] + "','" + data["Keywords"] + "','" + \
                  data["PublishTime"] + "'," + str(data["IsClean"]) + ",'" + data["SourceType"] + "','" + data[
                      "Account"] + "','" + data['AccountUrl'] + "'," + str(data["Comments"]) + "," + str(
                data["Favorites"]) + "," + str(
                data["ReadCounts"]) + "," + str(data["Status"])  +');'
try:
    sqlserver.ExecNoQuery(sql)
except pymssql.IntegrityError as e:
    print(True)