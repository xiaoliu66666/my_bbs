# session所需的密钥
SECRET_KEY = "dca55fc1-c08d-490c-8177-0777ed4e700e"
DEBUG = True

# 写入session的id
CMS_USER_ID = "9de35bfb-2524-4894-9b08-49260df4d12a"
FRONT_USER_ID = "9de35bfb-2524-4894-9b08-49260df4d12a"

# 数据库配置
DB_USERNAME = "root"
DB_PASSWORD = "5323128+1s"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "sbbs"

DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 发送邮件的服务器配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False
MAIL_USERNAME = "767550269@qq.com"
MAIL_PASSWORD = "lgqkqhxiztibbdag"
MAIL_DEFAULT_SENDER = "767550269@qq.com"


