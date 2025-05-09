import random
import string
from datetime import timezone

import paramiko
from celery import shared_task

from app.models import PasswordChangeLog, Host, HostStat


def random_password(length=16):
    '''
    随机密码
    :param length:
    :return:
    '''
    characters = string.ascii_letters + string.digits + string.punctuation
    # 确保密码中至少包含一个大写字母、一个小写字母、一个数字和一个特殊字符
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]
    password += random.choices(characters, k=length - 4)
    random.shuffle(password)
    return ''.join(password)


@shared_task
def change_root_password(host_id):
    try:
        host = Host.objects.get(id=host_id)
        old_password = host.password
        new_password = random_password()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host.ip_address, port=host.port, username=host.username, password=old_password)

        # 使用 invoke_shell 以交互方式执行 passwd 命令
        shell = ssh.invoke_shell()
        shell.send('passwd\n')
        shell.recv(1024)
        shell.send(f'{new_password}\n')
        shell.recv(1024)
        shell.send(f'{new_password}\n')
        shell.recv(1024)

        ssh.close()

        # 更新主机密码
        host.password = new_password
        host.save()

        # 记录密码变更日志
        PasswordChangeLog.objects.create(
            host=host,
            old_password=old_password,
            new_password=new_password,
            status='success',
            message='Password changed successfully.'
        )
    except Exception as e:
        # 记录失败的密码变更日志
        PasswordChangeLog.objects.create(
            host=host,
            old_password=old_password,
            new_password='',
            status='failure',
            message=str(e)
        )

@shared_task
def schedule_password_changes():
    '''
    需维护每台主机的 root 密码，每隔 8 小时随机修改每台主机的密码并记录
    :return:
    '''
    from .models import Host
    for host in Host.objects.all():
        change_root_password.delay(host.id)

@shared_task
def stat_host_count():
    '''
    每天 00:00 按城市和机房维度统计主机数量，并把统计数据写入数据库
    :return:
    '''
    from django.db.models import Count

    today = datetime.datetime.today()
    stats = (
        Host.objects
        .values('idc__city', 'idc')
        .annotate(host_count=Count('id'))
    )

    for stat in stats:
        city_id = stat['idc__city']
        idc_id = stat['idc']
        host_count = stat['host_count']
        HostStat.objects.create(
            city_id=city_id,
            idc_id=idc_id,
            host_count=host_count,
            stat_date=today
        )
