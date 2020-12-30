import smtplib
from email.mime.text import MIMEText

mailto_list = ['sxu_sj@163.com']  #收件人(列表)
mail_host = "smtp.163.com"  #使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user = "***"  #用户名
mail_pass = "***"  #密码
mail_postfix = "163.com"  #邮箱的后缀，网易就是163.com


def send_mail(sub, content):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(['sxu_sj@163.com'])  #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  #连接服务器
        server.login(mail_user, mail_pass)  #登录操作
        server.sendmail(me, ['sxu_sj@163.com'], msg.as_string())
        server.close()
        return True
    except Exception as e:
        print('message sending failed!')
        return False
