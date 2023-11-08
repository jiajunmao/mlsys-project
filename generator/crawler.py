from selenium import webdriver
import random

def random_walk_page(driver: webdriver.Firefox, page_path: str, remain_clicks: int):
    print("Visiting page {}, {} clicks remaining".format(page_path, remain_clicks))
    # Get the current page
    driver.get(page_path)
    
    # Get all the href on the page
    elems = driver.find_elements("xpath", "//a[@href]")
    clickable_links = []
    for elem in elems:
        clickable_links.append(elem.get_attribute("href"))
    
    print("There are {} clickable links on this page".format(len(clickable_links)))
    # If we still want to click
    if remain_clicks != 0:
        # We choose randomly from the list of clickable links
        rand_idx = random.randint(0, len(clickable_links))
        random_walk_page(driver, clickable_links[rand_idx], remain_clicks - 1)