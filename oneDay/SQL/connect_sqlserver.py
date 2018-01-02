import pymssql

class MYSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    def __GetConnect(self):
        if not self.db:
            raise(NameError,'没有设置数据库信息')
        self.conn = pymssql.connect(host = self.host,user = self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur
    # def ExecQuery(self,sql):
    #     cur = self.__GetConnect()
    #     try:
    #         cur.execute(sql)
    #         resList = self.cur.fetchall()
    #         self.conn.close()
    #     except:
    #         self.conn.close()
    #         raise('')
    #     return resList

    def ExecNoQuery(self,sql):
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        except:
            self.conn.close()
            raise('')
