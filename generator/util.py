import json
import pandas as pd
import datetime

from browsermobproxy import Server, Client
from selenium import webdriver
from dateutil.parser import parse

def is_json(fname):
    with open(fname) as f:
        try:
            json.load(f)
            return True
        except Exception:
            return False
        
def postprocess_har(aggregate_har):
    test_pdf = parse_har(aggregate_har)
    test_pdf.sort_values(by=['start_time'])
    
    test_pdf['relative'] = test_pdf.start_time.astype(np.int64) // 10 ** 9
    test_pdf['relative'] = test_pdf['relative'] - min(test_pdf['relative'])
    test_pdf = test_pdf.sort_values(by=['relative'])
    
    return test_pdf

def parse_har(list_of_har):
    traces = []
    for har_tup in list_of_har:
        # TODO: fix this relative time calculation
        time = har_tup[0]
        har = har_tup[1]
        entries = har['log']['entries']
    
        features = ['url', 'start_time', 'response_code', 'body_size', 'rtt']
        for req in entries:
            # TODO: fix this relative time
            start_time = parse(req['startedDateTime'])
            start_time += datetime.timedelta(minutes=time)
            url = req['request']['url']
            response_code = req['response']['status']
            body_size = req['response']['bodySize']
            rtt = req['time']
            
            traces.append((url, start_time, response_code, body_size, rtt))
        
    return pd.DataFrame(traces, columns=features)

def write_har(har, filename='har.json'):
    f = open(filename, "w")
    json.dump(har, f)
    f.close()

def get_driver(proxy):
    options = webdriver.FirefoxOptions()
    options.proxy = proxy.selenium_proxy()
    options.add_argument("-headless") 
    driver = webdriver.Firefox(options=options)

    return driver

def get_proxy(port=8080):
    server = Server("/home/aaronmao/.bin/browsermob-proxy-2.1.4/bin/browsermob-proxy", {"port": port})
    server.start()
    proxy = server.create_proxy()
    
    return proxy, server
