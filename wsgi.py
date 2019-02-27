import sys
from os.path import abspath
from os.path import dirname
from bbs import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app

"""
建立一个软连接（右边指向左边）
ln -s /var/www/my_bbs/my_bbs.conf /etc/supervisor/conf.d/my_bbs.conf

➜  ~ cat /etc/supervisor/conf.d/my_bbs.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn_conf.py
directory=/var/www/my_bbs
autostart=true
autorestart=true




/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:8000
--pid /tmp/blog.pid
"""