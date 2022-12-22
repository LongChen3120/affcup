import re
import sys
import json
import logging
import datetime

import requests

import db_handler
import func
import utils
import func_parse
import func_action
import func_detect
import func_request_find
import func_input_to_ouput
from config import config_env

from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


log_main = logging.getLogger(config_env.NAME_LOG_1)
log_ram = logging.getLogger(config_env.NAME_LOG_2)


def save_data_lich_thi_dau(es, config, config_src, list_data):
    for data in list_data:
        if data['time'] > datetime.datetime.now():
            temp = format_data_lich_thi_dau(config, config_src, data)
            text = utils.unicode_to_kodauvagach_viet_lien(temp['detail_team_0']['name']) + "_" + utils.unicode_to_kodauvagach(temp['detail_team_1']['name']) + "_" + temp['time']
            _id = func.encryption_text_to_code(text)
            result = db_handler.find_by_id(es, config_env.INDEX_ES, _id)
            if result['hits']['total']['value'] > 0:
                del temp['create_date']
                db_handler.update_by_id(es, config_env.INDEX_ES, _id, temp)
            else:
                db_handler.insert_ES(es, config_env.INDEX_ES, _id, temp)
    log_main.info("save lich thi dau")


def save_data_bang_xep_hang(es, config, config_src, list_data):
    for data in list_data:
            temp = format_data_bang_xep_hang(config, config_src, data)
            text = utils.unicode_to_kodauvagach_viet_lien(temp['group']) + "_" + utils.unicode_to_kodauvagach(temp['team'])
            _id = func.encryption_text_to_code(text)
            result = db_handler.find_by_id(es, config_env.INDEX_ES, _id)
            if result['hits']['total']['value'] > 0:
                del temp['create_date']
                db_handler.update_by_id(es, config_env.INDEX_ES, _id, temp)
            else:
                db_handler.insert_ES(es, config_env.INDEX_ES, _id, temp)
    log_main.info("save bang xep hang")


def format_data_lich_thi_dau(config, config_src, data):
    data_out = config_env.data_football_lich()
    data_out['type'] = config_src['lich_thi_dau']['type']
    data_out['topic'] = config['topic']
    data_out['domain'] = config_src['domain']
    data_out['url'] = config_src['lich_thi_dau']['url']
    data_out['create_date'] = datetime.datetime.now()
    for key in data_out:
        if key == "time":
            data_out['time'] = datetime.datetime.strftime(data['time'], "%Y-%m-%dT%H:%M:%S.%f")
        else:
            try:
                data_out[key] = data[key]
            except:
                pass
    data_out['keyword'] = [config['topic'], data['detail_team_0']['name'], data['detail_team_1']['name']]
    data_out['keyword_unsign'] = [utils.unicode_to_kodauvagach(i) for i in data_out['keyword']]
    return data_out


def format_data_ket_qua():
    pass


def format_data_bang_xep_hang(config, config_src, data):
    data_out = config_env.data_football_bxh()
    data_out['type'] = config_src['bang_xep_hang']['type']
    data_out['topic'] = config['topic']
    data_out['domain'] = config_src['domain']
    data_out['url'] = config_src['bang_xep_hang']['url']
    data_out['create_date'] = datetime.datetime.now()
    for key in data_out:
        try:
            data_out[key] = data[key]
        except:
            pass
    data_out['keyword'] = [config['topic'], data['group'], data['team']]
    data_out['keyword_unsign'] = [utils.unicode_to_kodauvagach(i) for i in data_out['keyword']]
    return data_out


def crawl():
    # hàm crawl lịch

    # tìm đọc config
    es = db_handler.connect_ES()
    col_config_crawl_sport = db_handler.connect_col_config_crawl_sport()
    col_lich_sport = db_handler.connect_col_lich_sport()
    db_handler.update_config()
    list_config = col_config_crawl_sport.find({})

    # crawl thông tin lịch và bxh
    for config in list_config:
        if config['end_league'] is False:
            for config_src in config['src']:
                response = func_detect.detect_type_crawl(config_src)
                response = func_detect.detect_type_response(response, config_src)
                for key in ["lich_thi_dau", "bang_xep_hang"]:
                    try:
                        if config_src[key]['type_crawl'] == 0:
                            data = config_src[key]
                            del data['type_crawl']
                        else:
                            if config_src[key]['url'] != config_src['url']:
                                response = func_detect.detect_type_crawl(config_src[key])
                                response = func_detect.detect_type_response(response, config_src[key])
                            for i in config_src[key]['way']:
                                response = response[i]

                            if config_src[key]['type_response'] == 1:
                                result = func_request_find.html_find_xpath(response, config_src[key]['xpath'])
                                data = func_detect.detect_type_result(result, config_src[key])
                            elif config_src[key]['type_response'] == 2:
                                data = []
                                for obj in response:
                                    temp = func_parse.parse_config_json({}, config_src[key]['data'], {}, obj)
                                    data.append(temp)
                    except:
                        log_main.exception("crawl_lich_bxh - message:", exc_info=True)
                    
                    if key == 'lich_thi_dau':
                        data = save_data_lich_thi_dau(es, config, config_src, data)
                    elif key == 'bang_xep_hang':
                        data = save_data_bang_xep_hang(es, config, config_src, data)