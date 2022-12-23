import sys
sys.path.insert(0, '..\\affcup\\scr')
# print(sys.path)


import uvicorn

import db_handler

from fastapi import FastAPI


app = FastAPI()

# ----- GET

# check data
@app.post('/info')
def check_data(payload:dict = None):
    es = db_handler.connect_ES()
    query_search = {
        "size":200,
        "sort": [
            {
                "time": {
                    "order": "asc"
                }
            }
        ],
        "query":{
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
                "message":"invalid topic !",
                "code": 400,
                "data":"please add param: 'topic':'worldcup' or 'topic':'affcup'"
            }
    for key, vals in payload.items():
        if key == "topic" and vals:
            if vals == "worldcup":
                index_es = "worldcup"
            elif vals == "affcup":
                index_es = "lich_affcup"
            else:
                return {
                "message":"invalid topic !",
                "code": 400,
                "data":"please add param: 'topic':'worldcup' or 'topic':'affcup'"
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
                                                                "type":  vals
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
        if key == "time" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "time": {
                                                                    "query": vals,
                                                                    "operator": "and"
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
    result =  db_handler.search_doc(es, index_es, query_search)
    try:
        result['hits']['hits'][0]
        return {
            "message":"ok",
            "code": 200,
            "data":result['hits']['hits']
        }
    except:
        return {
            "message":"data not found !",
            "code": 404
        }


if __name__ == "__main__":
    uvicorn.run("api.api:app", host="192.168.19.163", port=8000, reload=True)
    

# import os
# print(os.listdir())
