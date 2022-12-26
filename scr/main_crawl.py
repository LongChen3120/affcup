import sys
import json
import time
import logging
import datetime

import func
import db_handler
import crawl_detail
import crawl_lich_bxh
from config import config_env

import queue
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler



def call_api_set_lich_tuong_thuat(time_start, doc):
    time_start_crawl = func.get_time_run(time_start, -30)
    time_start_crawl = datetime.datetime.strftime(time_start_crawl, "%Y-%m-%dT%H:%M:%S.%f")
    payload = config_env.PAYLOAD_SCHEDULE_CRAWL
    payload['start_time'] = str(time_start_crawl)
    payload['site'] = doc['_source']['domain']
    payload['kwargs']['schedule_data'][0]['schedule_id'] = doc['_id']
    payload['kwargs']['schedule_data'][0]['team_0'] = doc['_source']['detail_team_0']['name']
    payload['kwargs']['schedule_data'][0]['team_1'] = doc['_source']['detail_team_1']['name']
    log_main.info(f"__payload:{payload}")
    try:
        res = requests.post(config_env.API_SCHEDULE_CRAWL, headers=config_env.HEADER, json=payload)
        log_main.warning(f"__response: {res.text}\nstart run crawl thuong thuat luc:{time_start_crawl},")
    except:
        log_main.warning("exception: ", exc_info=True)


def crawl_handler(id_match):
    check_job()
    # try:
    #     crawl_lich_bxh.crawl()
    # except:
    #     log_main.exception(f"message: exception when crawl lich", exc_info=True)
    # try:
    #     crawl_detail.crawl2(id_match)
    # except:
    #     log_main.exception(f"message: exception when crawl detail", exc_info=True)
    # finally:
    #     db_handler.up_log()


def check_job():
    list_job = scheduler.get_jobs()
    while len(list_job) < 5:
        list_match = db_handler.find_next_match(es, config_env.INDEX_ES, list_job[-1].next_run_time)
        log_main.info(f"check_time: {list_job[-1].next_run_time},\nlist match:{[i['_id'] for i in list_match]}")
        for match in list_match:
            time_start = func.convet_time_start(match['_source']['time'])
            # call_api_set_lich_tuong_thuat(time_start, match)
            time_run = func.get_time_run(time_start, 5)
            add_job(match['_id'], time_run)
            list_job = scheduler.get_jobs()


def add_job(id_match, time_run):
    log_main.info(f"next run at: {time_run}")
    trigger = CronTrigger(year=time_run.year, month=time_run.month, day=time_run.day, hour=time_run.hour, minute=time_run.minute, second=time_run.second)
    scheduler.add_job(crawl_handler, trigger=trigger, args=[id_match], max_instances=10, name=f"job: {id_match}")
    log_main.info("list jobs:")
    for job in scheduler.get_jobs():
        log_main.info(job)
    # log_main.info(f"add job ok, list jobs:\n{scheduler.get_jobs()}")


def scheduler_run(list_match):
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    for match in list_match:
        time_start = func.convet_time_start(match['_source']['time'])
        # call_api_set_lich_tuong_thuat(time_start, match)
        time_run = func.get_time_run(time_start, 5)
        add_job(match['_id'], time_run)
    
    while True:
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            print("exiting...")
            scheduler.shutdown()
            sys.exit()


if __name__ == '__main__':
    func.set_log(config_env.NAME_LOG_1, config_env.PATH_LOG_1)
    func.set_log(config_env.NAME_LOG_2, config_env.PATH_LOG_2)
    log_main = logging.getLogger(config_env.NAME_LOG_1)
    log_ram = logging.getLogger(config_env.NAME_LOG_2)
    log_main.propagate = False
    log_ram.propagate = False
    db_handler.update_config()
    es = db_handler.connect_ES()
    
    list_match = db_handler.find_next_match(es, config_env.INDEX_ES, datetime.datetime.now())
    scheduler_run(list_match)

    