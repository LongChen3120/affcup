import sys
import json
import time
import logging
import datetime

import func
import utils
import func_action
import func_detect
import func_request_find
from config import config_env
import db_handler


log_main = logging.getLogger(config_env.NAME_LOG_1)
log_ram = logging.getLogger(config_env.NAME_LOG_2)


def crawl_info_match(match, config):
    # hàm crawl detail một trận đấu
    data = {}
    step_crawl = config['step_crawl']
    for step in step_crawl:
        if step == "send_request":
            browser = func_detect.detect_type_crawl(config['send_request'])
        else:
            try:
                result = detect_step(step, browser, config, match)
                data.update(result)
            except:
                pass
    # browser.close()
    return data, browser


def crawl_loop(browser, match, config):
    data = {}
    step_crawl = config['step_crawl_loop']
    for step in step_crawl:
        try:
            result = detect_step(step, browser, config, match)
            data.update(result)
        except:
            pass
    return data


def detect_step(step, browser, config, match):
    if step == "send_key":
        key = match['detail_team_0']['name'] + " vs " + match['detail_team_1']['name']
        log_main.info("send_key")
        func_detect.detect_type_action(browser, config['send_key'], key)
    elif step == "click_search":
        log_main.info("click_search")
        func_detect.detect_type_action(browser, config['click_search'], match)
    elif step == "click_match":
        log_main.info("click_match")
        func_detect.detect_type_action(browser, config['click_match'], match)
    elif step == "click_thong_ke":
        log_main.info("click_thong_ke")
        func_detect.detect_type_action(browser, config['click_thong_ke'], match)
    elif step == "crawl_thong_ke":
        log_main.info("crawl_thong_ke")
        return func_detect.detect_type_action(browser, config['crawl_thong_ke'], match)
    elif step == "click_doi_hinh":
        log_main.info("click_doi_hinh")
        func_detect.detect_type_action(browser, config['click_doi_hinh'], match)
    elif step == "crawl_doi_hinh":
        log_main.info("crawl_doi_hinh")
        return  func_detect.detect_type_action(browser, config['crawl_doi_hinh'], match)
    elif step == "click_timelines":
        log_main.info("click_timelines")
        return  func_detect.detect_type_action(browser, config['click_timelines'], match)
    elif step == "crawl_timelines":
        log_main.info("crawl_timelines")
        return  func_detect.detect_type_action(browser, config['crawl_timelines'], match)


def format_data(match, data, config):
    for key in match:
        try:
            match[key] = data[key]
        except:
            pass
    try:
        if match['detail_team_0']['name'] == data['detail_team_0']['name']:
            match['detail_team_0'].update(data['doi_hinh_team_0'])
            match['detail_team_1'].update(data['doi_hinh_team_1'])
        else:
            match['detail_team_0'].update(data['doi_hinh_team_1'])
            match['detail_team_1'].update(data['doi_hinh_team_0'])
    except:
        pass
    return match
    

def crawl(id_match):
    # hàm crawl detail của một trận đấu và tự động lưu vào db
    # truyền vào id trận đấu

    # tìm kiếm trận đấu theo id
    es = db_handler.connect_ES()
    match = db_handler.find_by_id(es, config_env.INDEX_ES, id_match)['hits']['hits'][0]

    # tìm config của trận đấu
    config = db_handler.check_config(match['_source']['topic'])

    # crawl thông tin chi tiết trận đấu
    data, browser = crawl_info_match(match['_source'], config)
    browser.close()

    # format đầu ra
    data = format_data(match['_source'], data, config)
    # print(data)

    # # lưu dữ liệu vào db
    # db_handler.up_log()
    # print(data)
    db_handler.update_by_id(es, config_env.INDEX_ES, id_match, data)


def crawl2(id_match):
    # hàm crawl detail của một trận đấu và tự động lưu vào db
    # truyền vào id trận đấu

    # tìm kiếm trận đấu theo id
    es = db_handler.connect_ES()
    match = db_handler.find_by_id(es, config_env.INDEX_ES, id_match)['hits']['hits'][0]

    # tìm config của trận đấu
    config = db_handler.check_config(match['_source']['topic'])

    time_crawl = 0
    try:
        # crawl thông tin chi tiết trận đấu
        log_main.info(f"crawl detail id {id_match}")
        data, browser = crawl_info_match(match['_source'], config)
        while time_crawl < 200:
            log_ram.warning(f"Start crawl: == RAM USE: {func.get_ram()} MB ==")
            try:
                # format đầu ra
                log_main.info("format data")
                data = format_data(match['_source'], data, config)

                # lưu dữ liệu vào db
                log_main.info("update to db")
                db_handler.update_by_id(es, config_env.INDEX_ES, id_match, data)
            except:
                pass
            if data['status'] == "Kết thúc":
                log_main.info("end crawl")
                log_main.info(f"data crawl detail:{data}")
                break
            else:
                time.sleep(1 * 60)
                time_crawl += 1
                log_main.info(f"__loop: {time_crawl}")
                data = crawl_loop(browser, match, config)
    except:
        pass
    finally:
        browser.close()

# crawl("1645af523f04b4b93a18bc620ccfd0c9")
# crawl2("4064377f826b3c990b407a8a92cf27c0")
