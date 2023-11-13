import pickle
from trace_gen import gen_trace
from util import postprocess_har

# ---------------------
num_worker = 36
num_user = 3000
mission_hour = 5
# ---------------------

mission_minutes = mission_hour*60
mission_seconds = mission_hour*60*60

# ---------------------

aggregate_har, sys = gen_trace(num_user, mission_minutes, num_worker)

test_pdf = postprocess_har(aggregate_har)

f = open("user_{}_hour_{}_cs.uchicago.edu.pandas".format(num_user, mission_hour), "wb")
pickle.dump(test_pdf, f)
f.close()