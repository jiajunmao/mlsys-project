import pickle
from trace_gen import gen_trace
from util import postprocess_har

# ---------------------
num_worker = 20
num_user = 200
mission_hour = 4
# ---------------------

mission_minutes = mission_hour*60
mission_seconds = mission_hour*60*60

# ---------------------

base_path = "cs.uchicago.edu"

aggregate_har, sys = gen_trace(base_path, num_user, mission_minutes, num_worker)

f = open("user_{}_hour_{}_{}.har".format(num_user, mission_hour, base_path), "wb")
pickle.dump(aggregate_har, f)
f.close()

test_pdf = postprocess_har(aggregate_har)

f = open("user_{}_hour_{}_{}.pandas".format(num_user, mission_hour, base_path), "wb")
pickle.dump(test_pdf, f)
f.close()
