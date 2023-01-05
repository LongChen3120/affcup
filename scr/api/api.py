import sys
import copy
sys.path.insert(0, 'C:\\Users\\Admin\\Documents\\crawl_football\\scr')
# print(sys.path)

import uvicorn

import db_handler

from fastapi import FastAPI


app = FastAPI()

# ----- GET

# check data
@app.post('/info')
def check_data(payload: dict = None):
    es = db_handler.connect_ES()
    query_search = {
        "size": 200,
        "sort": [
            {
                "time": {
                    "order": "asc"
                }
            }
        ],
        "query": {
            "bool": {
                "must": [

                ]
            }
        }
    }
    try:
        payload['topic']
    except:
        return {
            "message": "invalid topic !",
            "code": 400,
            "data": "please add param: 'topic':'worldcup' or 'topic':'affcup'"
        }
    for key, vals in payload.items():
        if key == "topic" and vals:
            if vals == "worldcup":
                index_es = "worldcup"
            elif vals == "affcup":
                index_es = "lich_affcup"
            else:
                return {
                    "message": "invalid topic !",
                    "code": 400,
                    "data": "please add param: 'topic':'worldcup' or 'topic':'affcup'"
                }
        if key == "team_0" and vals:
            query_search["query"]["bool"]["must"].append({
                "match": {
                    "detail_team_0.name": {
                        "query": vals,
                        "operator": "and"
                    }
                }
            })
        if key == "team_1" and vals:
            query_search["query"]["bool"]["must"].append({
                "match": {
                    "detail_team_1.name": {
                        "query": vals,
                        "operator": "and"
                    }
                }
            })
        if key == "type" and vals:
            query_search["query"]["bool"]["must"].append({
                "match": {
                    "type": vals
                }
            })
        if key == "round" and vals:
            query_search["query"]["bool"]["must"].append({
                "match": {
                    "round": {
                        "query": vals,
                        "operator": "and"
                    }
                }
            })
        if key == "time(chính xác: yyyy-mm-dd)" and vals:
            query_search["query"]["bool"]["must"].append({
                "match": {
                    "time": {
                        "query": vals,
                        "operator": "and"
                    }
                }
            })
        if key == "time(trước ngày: yyyy-mm-dd)" and vals:
            query_search["query"]["bool"]["must"].append({
                "range": {
                    "time": {
                        "lt": vals
                    }
                }
            })
        if key == "time(sau ngày: yyyy-mm-dd)" and vals:
            query_search["query"]["bool"]["must"].append({
                "range": {
                    "time": {
                        "gt": vals
                    }
                }
            })
        if key == "id" and vals:
            query_search["query"]["bool"]["must"].append({
                "match": {
                    "_id": vals
                }
            })
    # return payload
    # return query_search
    print(query_search)
    try:
        query_search_2 = copy.deepcopy(query_search)
        temp = query_search_2['query']['bool']['must'][1]['match']['detail_team_0.name']['query']
        query_search_2['query']['bool']['must'][1]['match']['detail_team_0.name']['query'] = \
        query_search_2['query']['bool']['must'][2]['match']['detail_team_1.name']['query']
        query_search_2['query']['bool']['must'][2]['match']['detail_team_1.name']['query'] = temp
    except:
        return db_handler.search_doc(es, index_es, query_search)

    for i in [query_search, query_search_2]:
        result = db_handler.search_doc(es, index_es, i)
        if result['hits']['total']['value'] != 0:
            return {
                "message": "ok",
                "code": 200,
                "data": result['hits']['hits']
            }
        else:
            continue
    return {
        "message": "data not found !",
        "code": 404
    }


if __name__ == "__main__":
    import logging
    import os
    logging.basicConfig(filename="log_api.log", level=logging.INFO)
    logging.info(f"{os.listdir()}")
    uvicorn.run("api.api:app", host="192.168.19.187", port=8000, reload=True)
