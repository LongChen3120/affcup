import re
import os
import logging
import datetime
import hashlib

import psutil

from logging.handlers import TimedRotatingFileHandler


def set_log(logger_name, log_file):
    rootlogger = logging.getLogger(logger_name)
    rootlogger.setLevel(logging.INFO)
    timed_rotating = TimedRotatingFileHandler(log_file,
                                       when="h",
                                       interval=24,
                                       backupCount=5,
                                       encoding='utf-8'
                                       )
    timed_rotating.setLevel(logging.INFO)
    timed_rotating.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
    
    rootlogger.addHandler(timed_rotating)


def regex_extract(obj, config):
    regex = config['re']
    result = re.findall(regex, obj)
    return result


def remove_space(string):
    return re.sub('\s+', ' ', string)


def get_time_run(time_start, time_match):
    # hàm xác định thời gian chạy so với thời gian bắt đầu trận đấu
    return (time_start + datetime.timedelta(minutes=time_match))


def convet_time_start(time_start):
    return datetime.datetime.strptime(time_start, "%Y-%m-%dT%H:%M:%S.%f")


def get_ram():
    process_id = os.getpid()
    process = psutil.Process(process_id)
    # log_ram.warning(f"__Process id: {process_id}; Ram use: {int(process.memory_info().rss)/1024}")
    return int(process.memory_info().rss)/1024


def encryption_text_to_numb(text):
    return str(int(hashlib.md5(text.encode()).hexdigest(), 16))[0:6]


def encryption_text_to_code(text):
    return hashlib.md5(text.encode()).hexdigest()


