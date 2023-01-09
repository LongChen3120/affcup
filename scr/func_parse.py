

import func_detect
import func_request_find


def parse_config_browser(old_object, object, data, browser):
    # hàm đệ quy đọc cấu trúc config crawl cho những site dùng selenium, xuất ra result tương ứng
    old_vals = object
    for key, vals in object.items():
        if isinstance(vals, str) or isinstance(vals, int):
            result = func_detect.detect_browser_result(browser, old_vals)
            try:
                for _ in old_vals['replace']:
                    result = result.replace(_['old_val'], _['new_val'])
            except:
                pass
            try:
                result = result[old_vals['position']]
            except:
                pass
            return result
        elif isinstance(vals, dict):
            result = parse_config_browser(old_vals, vals, {}, browser)
            if result is not None:
                data[key] = result
            else:
                data[key] = None
        elif isinstance(vals, list):
            data[key] = []
            for obj in vals:
                temp = parse_config_browser(old_vals, obj, {}, browser)
                if temp:
                    data[key].append(temp)
                else:
                    continue
    return data


def parse_config_html(old_object, object, data, browser):
     # hàm đệ quy đọc cấu trúc config crawl cho những site dùng requests, response là html, xuất ra result tương ứng
    old_vals = object
    for key, vals in object.items():
        if isinstance(vals, str) or isinstance(vals, int):
            result = func_request_find.html_find_xpath(browser, old_vals['xpath'])
            result = func_detect.detect_type_result(result, old_vals)
            try:
                result = result[old_vals['position']]
            except:
                pass
            finally:
                return result
        elif isinstance(vals, dict):
            result = parse_config_html(old_vals, vals, {}, browser)
            if result is not None:
                data[key] = result
            else:
                data[key] = None
        elif isinstance(vals, list):
            data[key] = []
            for obj in vals:
                temp = parse_config_html(old_vals, obj, {}, browser)
                if temp:
                    data[key].append(temp)
                else:
                    continue
    return data


def parse_config_json(old_object, object, data, browser):
    # hàm đệ quy đọc cấu trúc config crawl cho những site dùng requests, response là json, xuất ra result tương ứng
    old_vals = object
    for key, vals in object.items():
        if isinstance(vals, str) or isinstance(vals, int):
            result = parse_response_json("", object['key'], object['parent_key'], browser)
            result = func_detect.detect_type_result(result, object)
            try:
                result = result[object['position']]
            except:
                pass
            return result
        elif isinstance(vals, dict):
            result = parse_config_json(old_vals, vals, {}, browser)
            if result is not None and result:
                data[key] = result
            else:
                data[key] = None
        elif isinstance(vals, list):
            data[key] = []
            for obj in vals:
                temp = parse_config_json(old_vals, obj, {}, browser)
                if temp:
                    data[key].append(temp)
                else:
                    continue
    return data


def parse_response_json(old_key, config_key, config_parent_key, object):
    # old_vals = object
    for key, vals in object.items():
        if isinstance(vals, str) or isinstance(vals, int):
            if key == config_key and old_key == config_parent_key:
                return vals
            else:
                pass
        elif isinstance(vals, dict):
            vals = parse_response_json(key, config_key, config_parent_key, vals)
            if vals:
                return vals

        elif isinstance(vals, list):
            for obj in vals:
                parse_response_json(key, config_key, config_parent_key, obj)
    

# def parse_config_2(old_object, object, data, browser):
#     # hàm đọc cấu trúc config, xuất ra result tương ứng
#     old_vals = object
#     for key, vals in object.items():
#         if isinstance(vals, str) or isinstance(vals, int):
#             result = crawl_data(browser, old_vals)
#             return result
#         elif isinstance(vals, dict):
#             result = parse_config(old_vals, vals, {}, browser)
#             if result:
#                 data[key] = result
#             else:
#                 continue
#         elif isinstance(vals, list):
#             data[key] = []
#             for obj in vals:
#                 temp = parse_config(old_vals, obj, {}, browser)
#                 if temp:
#                     data[key].append(temp)
#                 else:
#                     continue
#     return data


# def parse_html(response, config):
#     return crawl_lich_bxh.crawl_table(response, config)


# def parse_json(response, config):
#     list_data = []
#     for obj in response:
#         data_sample = config['data_sample'].copy()
#         new_obj = crawl_lich_bxh.get_all_key_json(obj, {})
#         for key, vals in config['data_sample'].items():
#             if vals == "obj_json":
#                 obj_config = config['obj_json'][key]
#                 data = new_obj[obj_config['key']]
#                 data = func_detect.detect_type_result(data, obj_config)
#             elif vals == "web":
#                 data = func_detect.detect_type_result(response, config[key])
#             else:
#                 data = crawl_lich_bxh.detect_key(key, vals, data_sample, data_sample['keyword'])
#                 data_sample[key] = data
#                 continue

#             if type(data) == list:
#                     del data_sample[key]
#                     for i in range(len(data)):
#                         data_sample[key + "_" + str(i)] = data[i]
#             else:
#                 data_sample[key] = data
#         list_data.append(data_sample)
#     return list_data
