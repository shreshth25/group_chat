import json
import datetime
import re

def fetch(cursor, Q, params={}, to_dict=False, append=[]):
    query = cursor.execute(Q, params)
    dataCursor = query.fetchall()
    data = []
    for row in dataCursor:
        data.append(dict(row))
    if to_dict:
        return data
    return json.dumps(data, default=dateConvertor)


def fetchOne(cursor, Q, params=None, to_dict=False, append=[]):
    if not params:
        params = {}
    query = cursor.execute(Q, params)
    data = query.fetchone()
    if data:
        data = dict(data)
        if to_dict:
            return data
        return json.dumps(data, default=dateConvertor)
    else:
        return {}


def dateConvertor(o):
    print(type(o))
    if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
        return o.__str__()


def email_validation(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    return False