from selenium import webdriver
from typing import List
from sampler import next_click, next_session, num_clicks

class Event:
    
    def __init__(self, user: int, timestamp: int, path: str, remaining_click: int):
        self.user = user
        self.timestamp = timestamp
        self.path = path
        self.remaining_click = remaining_click
        
    def incr_time(self, time: int):
        self.timestamp += time
        
    def decr_click(self, num=1):
        self.remaining_click -= num
    
    def set_path(self, path: str):
        self.path = path
        
    def set_clicks(self, click: int):
        self.remaining_click = click
        
    def __repr__(self):
        return "time: {}, user {}, click {}, url {}".format(self.timestamp, self.user, self.remaining_click, self.path)
        
class System:
    
    def __init__(self, mission_time: int, base_path: str):
        self.mission_time = mission_time
        self.mq: List[Event] = []
        self.base_path = base_path
        self.har_buffer = []
        self.remaining_user = set()
        self.num_user = -1
        
    def push_event(self, event: Event):
        self.mq.append(event)
        
    def pop_event(self):
        return self.mq.pop(0)
    
    def init_mq(self, num_user: int):
        self.num_user = num_user
        for i in range(0, num_user):
            self.mq.append(Event(i, next_session(), "https://{}".format(self.base_path), num_clicks()))
            self.har_buffer.append([])
            self.remaining_user.add(i)
        