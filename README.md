启动django项目
python manage.py runserver 127.0.0.1:8000

启动celelry
celery -A hostmanager worker -l info

启动celery beat
celery -A hostmanager beat -l info 
