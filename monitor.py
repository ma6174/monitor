#!/usr/bin/env python
# coding=utf-8

"""
监控当前进程，获取进程信息和服务器状态
psutil.STATUS_RUNNING
psutil.STATUS_SLEEPING
psutil.STATUS_DISK_SLEEP
psutil.STATUS_STOPPED
psutil.STATUS_TRACING_STOP
psutil.STATUS_ZOMBIE
psutil.STATUS_DEAD
psutil.STATUS_WAKE_KILL
psutil.STATUS_WAKING
psutil.STATUS_IDLE
psutil.STATUS_LOCKED
psutil.STATUS_WAITING

返回信息示例：

{
    'load': '0.04, 0.27, 0.46', #负载
    'status': 'running', # 状态
    'now': '2013-08-15 19:45:06', # 当前时间
    'ip': '192.168.1.1', # IP地址
    'pid': 5120, # 进程号
    'username': 'ma6174', # 用户名
    'cmdline': 'python2.7 monitor.py', # 命令行
    'create_time': '2013-08-15 19:45:03', # 程序开始时间
    'path': '/home/ma6174/test/', # 程序执行路径
    'cpu_used': 0.0, # CPU占用率
    'ppid': 5119, # 父进程
    'vms': '13.52', # 虚拟内存
    'rss': '5.68' # 物理内存
}

"""

import os
import psutil
import time
import subprocess
from socket import socket, SOCK_DGRAM, AF_INET

def check_pid_alive(pid):
    """检查pid是否在存在"""
    try:
        return psutil.Process(pid).is_running()
    except:
        return False

def getLocalIP():
    """获取当前主机IP"""
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(('taobao.com', 0))
    return s.getsockname()[0]


def getProcessInfo(pid):
    """获取进程信息"""
    try:
        p = psutil.Process(pid)
        cpu_used = p.get_cpu_percent()
        cmdline = " ".join(p.cmdline)
        rss, vms = p.get_memory_info()
        rss, vms = "%.2f"%(rss/1024.0/1024.0), "%.2f"%(vms/1024.0/1024.0)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.create_time))
        username = p.username
        for i in range(100):
            status = str(p.status)
            if status == "running":
                break
            time.sleep(0.01)
    except:
        return False
    return dict(
        cpu_used=cpu_used,
        cmdline=cmdline,
        rss=rss,
        vms=vms,
        create_time=create_time,
        username=username,
        status=status,
    )

def getSystemLoad():
    """获取系统负载"""
    p = subprocess.Popen("uptime", stdout=subprocess.PIPE)
    p.wait()
    out = p.stdout.read().split(":")[-1].strip()
    return out

def getLocalInfo():
    """获取程序信息"""
    ip = getLocalIP()
    pid = os.getpid()
    ppid = os.getppid()
    path = os.getcwd()
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    load = getSystemLoad()
    result = dict(
        pid=pid,
        ppid=ppid,
        path=path,
        ip=ip,
        now=now,
        load=load,
    )
    return result


def getRunningStatus(pid):
    """总的调用"""
    localinfo = getLocalInfo()
    localinfo["pid"]=pid
    processinfo = getProcessInfo(localinfo["pid"])
    if processinfo:
        total = localinfo.copy()
        total.update(processinfo)
        return total
    return False


if __name__ == '__main__':
    pid = os.getpid()
    while True:
        print getRunningStatus(pid)
        time.sleep(0.5)
