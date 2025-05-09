# 启动django项目
python manage.py runserver 127.0.0.1:8000

# 启动celery
celery -A hostmanager worker -l info

# 启动celery beat
celery -A hostmanager beat -l info 

# 主机增删查改接口
http://127.0.0.1:8000/api/hosts/
# 城市增删查改接口
http://127.0.0.1:8000/api/cities/
# 机房增删查改接口
http://127.0.0.1:8000/api/idcs/
# 探测主机是否 ping 可达接口
http://127.0.0.1:8000/api/hosts/ping/?host=127.0.0.1

# 需维护每台主机的 root 密码，每隔 8 小时随机修改每台主机的密码并记录
app.tasks.schedule_password_changes()
# 每天 00:00 按城市和机房维度统计主机数量，并把统计数据写入数据库
app.tasks.stat_host_count()
# 实现一个中间件，统计每个请求的请求耗时
hostmanager.middleware.RequestTimingMiddleware
