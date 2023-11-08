from selenium import webdriver
from browsermobproxy import Client
from sampler import next_click, next_session, num_clicks
from gen_types import Event, System
import random

def process_event(driver: webdriver.Firefox, proxy: Client, event: Event, system: System):
    # We check whether this event is beyond mission time
    if event.timestamp > system.mission_time:
        return
    
    # Set the har
    proxy.new_har("user-{}".format(event.user))
    
    print("Visiting page {}".format(event.path))
    # Get the current page
    driver.get(event.path)
    
    # Get all the href on the page
    elems = driver.find_elements("xpath", "//a[@href]")
    clickable_links = []
    for elem in elems:
        clickable_links.append(elem.get_attribute("href"))
    
    print("There are {} clickable links on this page".format(len(clickable_links)))
    # We "choose" randomly from the list of clickable links
    # 1. we check whether there is any clicks left for this 
    if event.remaining_click > 0:
        # We get the next path
        while True:
            rand_idx = random.randint(0, len(clickable_links)-1)
            next_path = clickable_links[rand_idx]
            
            if system.base_path in next_path:
                break
        
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
        
    system.push_event(event)