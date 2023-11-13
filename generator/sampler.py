import numpy as np

# Parameters for between "session" access
def next_session():
    return np.random.normal(40, 20)

# Parameters for between clicks
def next_click():
    return np.random.normal(1, 0.5)

# A user will click at most 10 times, and at least 1 time for each session
def num_clicks():
    return np.random.randint(1, 10)