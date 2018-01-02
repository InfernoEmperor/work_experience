import pymssql

class MYSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    def __GetConnect(self):
        if not self.db:
            raise(Exception('No database information is set'))
        self.conn = pymssql.connect(host = self.host,user = self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (Exception( "Database connection failed"))
        else:
            return cur
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            resList = self.cur.fetchall()
            self.conn.close()
        except:
            self.conn.close()
            raise('')
        return resList

    def ExecNoQuery(self,sql):
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        except pymssql.IntegrityError:
            self.conn.close()
            raise(Exception(1))
        except Exception as e:
            self.conn.close()
            raise (e)
