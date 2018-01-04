from SQL.connect_sqlserver import  MYSQL

class SaveData:
    def __init__(self):
        host = r'127.0.0.1'
        user = 'sa'
        passd = '******'
        database = 'BaseData2017'
        self.sqlserver = MYSQL(host, user, passd, database)

    def save(self,data):
        try:
            sql = 'INSERT INTO [BaseData2017].[dbo].[ArticleCrawler] ([Url], [Url_id],[Source], [Title], [Author], [Content], [Keywords], [PublishTime], [IsClean], [SourceType],[Account], [AccountUrl],[Comments], [Favorites], [ReadCounts],[Status]) VALUES (' + "'" + \
                  data["Url"] + "','" + data["Url_id"] + "','" + data["Source"] + "','" + data["Title"] + "','" + data[
                      "Author"] + "','" + data["Content"] + "','" + data["Keywords"] + "','" + \
                  data["PublishTime"] + "'," + str(data["IsClean"]) + ",'" + data["SourceType"] + "','" + data[
                      "Account"] + "','" + data['AccountUrl'] + "'," + str(data["Comments"]) + "," + str(
                data["Favorites"]) + "," + str(
                data["ReadCounts"]) + "," + str(data["Status"])  +');'
            self.sqlserver.ExecNoQuery(sql)
        except Exception as e:
            # logging.error('function push_sql insert ' + data['Url'] + ' error!')
            raise (e)

