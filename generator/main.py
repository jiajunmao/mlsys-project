import pickle
from trace_gen import gen_trace
from util import postprocess_har

# ---------------------
num_worker = 48
num_user = 2000
mission_hour = 12
# ---------------------

mission_minutes = mission_hour*60
mission_seconds = mission_hour*60*60

# ---------------------

aggregate_har, sys = gen_trace("https://cc.gatech.edu", num_user, mission_minutes, num_worker)

f = open("user_{}_hour_{}_cc.gatech.edu.har".format(num_user, mission_hour), "wb")
pickle.dump(aggregate_har, f)
f.close()

test_pdf = postprocess_har(aggregate_har)

f = open("user_{}_hour_{}_cc.gatech.edu.pandas".format(num_user, mission_hour), "wb")
pickle.dump(test_pdf, f)
f.close()
