from selenium import webdriver
from browsermobproxy import Client
from sampler import next_click, next_session, num_clicks
from concurrent.futures import ThreadPoolExecutor
from typing import List
from util import get_proxy, get_driver
from gen_types import Event, System
import random
import traceback
import time
import pickle

def watchdog(sys: System):
    last_time = -1
    while len(sys.mq) != 0:
        ts = time.time()
        if int(ts) % 60 == 0 and int(ts) // 60 != last_time:
            last_time = int(ts) // 60
            print("Time at MQ tip {}".format(sys.mq[0].timestamp))
            print("{} events left in MQ".format(len(sys.mq)))
            
            f = open("user_{}_hour_{}_{}.har.checkpoint".format(sys.num_user, sys.mission_time//60, sys.base_path), "wb")
            pickle.dump(sys.har_buffer, f)
            f.close()

def worker(sys: System, drivers: List[webdriver.Firefox], proxy: Client, worker_idx: int):
    while len(sys.mq) != 0:
        curr_event = sys.pop_event()
        # print("Processing event {}".format(curr_event))
        process_event(drivers[worker_idx], proxy, curr_event, sys)
        
def gen_trace(base_path, num_user, mission_minutes, num_worker=48):
    # random_walk_page(driver, "https://cs.uchicago.edu", 5)
    # har = proxy.har # returns a HAR JSON blob
    proxy, server = get_proxy(8100)
    pool = ThreadPoolExecutor(num_worker+1)

    drivers = []
    for i in range(0, num_worker):
        print("Starting driver {}".format(i))
        drivers.append(get_driver(proxy))
        
    try:
        sys = System(mission_minutes, base_path)
        sys.init_mq(num_user)
        
        print("Initialized, generating trace")

        futures = []
        for worker_idx in range(num_worker):
            futures.append(pool.submit(worker, sys, drivers, proxy, worker_idx))
        
        # Append the watch dog thread
        futures.append(pool.submit(watchdog, sys))
        
        for fut in futures:
            fut.result()
    except:
        traceback.print_exc()
    finally:
        for i in range(0, num_worker):
            drivers[i].quit()
        server.stop()
    
    print("Done, aggregating har")
    
    aggregate_har = []
    for hars in sys.har_buffer:
        aggregate_har += hars
        
    print("Har aggregated")
    return aggregate_har, sys

def process_event(driver: webdriver.Firefox, proxy: webdriver.Proxy, event: Event, system: System):
    try:
        # We check whether this event is beyond mission time
        if event.timestamp > system.mission_time:
            system.remaining_user.remove(event.user)
            print("User {} done, remaining {} users".format(event.user, len(system.remaining_user)))
            return
        
        # Set the har
        proxy.new_har("user-{}".format(event.user))
        
        # print("Visiting page {}".format(event.path))
        # Get the current page
        driver.get(event.path)
    except:
        # This means that the driver cannot get the page, usually means that the link is not a webpage
        # We then return to the previous webpage, and retry for this event (do not increment time)
        # NOTE: should we increment time?
        event.set_path("https://{}".format(system.base_path))
        system.push_event(event)
        return
    
    try:
        # Push the recorded har into system's har buffer
        system.har_buffer[event.user].append((event.timestamp, proxy.har))
        
        # Get all the href on the page
        elems = driver.find_elements("xpath", "//a[@href]")
        # Dedup links
        clickable_links = set()
        for elem in elems:
            try:
                clickable_links.add(elem.get_attribute("href"))
            except:
                pass
        
        # Remove the current path
        clickable_links.discard(event.path)
        clickable_links.discard(event.path + "/")
        temp_links = []
        for link in clickable_links:
            if system.base_path in link:
                temp_links.append(link)
        
        clickable_links = temp_links
            
        # print("There are {} clickable links on this page".format(len(clickable_links)))
        # print(clickable_links)
        # We "choose" randomly from the list of clickable links
        # 1. we check whether there is any clicks left for this
        if len(clickable_links) == 0:
            # This means that this page has no out going links. We return the home page
            # We also do not increment time, but should we?
            event.set_path("https://{}".format(system.base_path))
            system.push_event(event)
            return

        if event.remaining_click > 0:
            # We get the next path
            tries = 0
            while True:
                rand_idx = random.randint(0, len(clickable_links)-1)
                next_path = clickable_links[rand_idx]
                # print("Choosing {} idx with url {}".format(rand_idx, clickable_links[rand_idx]))
                
                tries += 1
                
                if system.base_path in next_path:
                    break
                elif tries > 20:
                    raise Exception("Cannot find a valid path")
            
            # We get time until next click
            next_click_interval = next_click()
            
            # Update event properties
            event.decr_click()
            event.incr_time(next_click_interval)
            event.set_path(next_path)
        else:
            # This means that we should prep for the next event
            next_session_interval = next_session()
            new_clicks = num_clicks()
            
            event.set_clicks(new_clicks)
            event.incr_time(next_session_interval)
            
        # DO NOT put this in finally block as finally will execute after return, causing infinite MQ
        # Push the new event into system
        # print("Pushing event {}".format(event))
        system.push_event(event)
    except:
        traceback.print_exc()
        # Push the new event into system
        # print("Pushing event {}".format(event))
        system.push_event(event)
