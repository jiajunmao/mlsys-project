import json
import pandas as pd

from browsermobproxy import Server
from selenium import webdriver

def is_json(fname):
    with open(fname) as f:
        try:
            json.load(f)
            return True
        except Exception:
            return False
        
def parse_har(har):
    entries = har['log']['entries']
    
    traces = []
    features = ['url', 'start_time', 'response_code', 'body_size', 'rtt']
    for req in entries:
        start_time = req['startedDateTime']
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

def get_driver_and_proxy(port):
    server = Server("/home/aaronmao/.bin/browsermob-proxy-2.1.4/bin/browsermob-proxy", {"port": port})
    server.start()
    proxy = server.create_proxy()

    profile  = webdriver.FirefoxProfile()
    options = webdriver.FirefoxOptions()
    options.proxy = proxy.selenium_proxy()
    driver = webdriver.Firefox(options=options)

    proxy.new_har("har")
    
    return driver, proxy, server
