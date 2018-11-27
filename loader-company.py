"""

this fiel loads fast the 5y stocks data
"""

from multiprocessing import Pool
import requests as rq
import pandas as pd
import numpy as np
import json
import os

def get_list():
    if os.path.exists('symbols.json'):
        with open('symbols.json',mode='r') as f:
            return json.load(f)
    try:
        data = rq.get('https://api.iextrading.com/1.0/ref-data/symbols').json()
        with open('symbols.json',mode='w') as f:
            json.dump(data, f)
        return data
    except Exception as ex:
        print('error', ex)
        pass
def get_data(symbol):
    s = symbol
    symbol = symbol.replace('#','_')
    dr = os.path.join('company',symbol[0])
    if not os.path.exists(dr):
        os.mkdir(dr)
    path = os.path.join(dr, symbol+'.json')
    if os.path.exists(path) and os.stat(path).st_size > 0:
        return
    try:
        #data = rq.get('https://api.iextrading.com/1.0/stock/'+s+'/stats').json()
        resp = rq.get('https://api.iextrading.com/1.0/stock/'+s+'/company')
        print(symbol, resp.status_code)
        if (resp.status_code != 200):
            return 
        data = resp.json()
        with open(path,mode='w') as f:
            json.dump(data, f)
    except Exception as ex:
        print(ex)
        pass

def load_symbol(s):
    get_data(s['symbol'])

if __name__ == '__main__':
    p = Pool(20)
    p.map(load_symbol, get_list())