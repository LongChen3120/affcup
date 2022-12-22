import time

import func_request_find

from selenium.webdriver.common.keys import Keys

def action_click(browser, config):
    # config truyen vao la config doi tuong
    func_request_find.browser_find_xpath(browser, config['xpath']).click()
    # browser.find_element(By.XPATH, config['xpath']).click()
    # time.sleep(config['time_sleep'])



def click_thong_so(browser):
    func_request_find.browser_find_xpath(browser, "//*[@class= 'PPjCfd tb_noscroll tb_tc']/li[3]").click()


def action_get_attribute(browser, config):
    list_result = []
    elements = func_request_find.browser_finds_xpath(browser, config['xpath']) 
    for element in elements:
        result = element.get_attribute(config['attribute'])
        if result:
            list_result.append(result)
    return list_result


def action_scroll_down():
    pass


def action_send_keys(browser, config, key):
    # config truyen vao la config doi tuong
    func_request_find.browser_find_xpath(browser, config['xpath']).send_keys(key)


def action_enter(browser, config):
    func_request_find.browser_find_xpath(browser, config['xpath']).send_keys(Keys.RETURN)
    time.sleep(config['time_sleep'])

