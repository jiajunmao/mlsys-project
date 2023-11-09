# mlsys-project

## Getting started
You will need the following environment setup
- Python 3
- Java 8
- Selenium
- Selenium Firefox Driver + Firefox
- Browsermob Proxy
    - You would need **java 8** to run the `browsermob-proxy`. Also remember to change the path to your `browsermob-proxy` installation in `util.py`
    - Anything above Java 8 will fail the browsermob executable as there are new changes in how reflection works

## User assumption
Our user is not that smart. He separates his browsing activity into multiple sessions. Each browsing **session** consists of a series of **bursty clicks**. The exact number of clicks is generated from `sampler.py::num_clicks (A random integer from 1 to 10)`. Between each bursty click is when our hypothetical user read the website hypothetically. The time taken to read the website is generated from `sampler.py::next_click (1 minute mean, 1/2 minute stddev Gaussian)`. Between **each session**, our user takes a tea break. The length of tea break is generated from `sampler.py::next_session (60 minutes mean, 20 minutes stddev Gaussian)`. The user takes his final rest when his browsing session has reached `mission_time` specified in the `System` class.

## Project arch
We can have multiple, mutually independent, not so smart user introduced above browsing the web at the same time. Currently this is set in `scratch.ipynb`'s `num_user` variable. Together they will contribute to the total access pattern of our hypothetical site.

To make the generator work efficiently, we adopt a MQ based producer/consumer multithreading strategy where each browser click is abstracted into an `Event (gen_types.py)` that sits in `System.mq` variable. We also spawn a number of workers `num_worker (scratch.ipynb)`. Each worker will spawn a independent selenium headless browser and consume events from the message queue.



## List of files
- `generator/`: where the trace generator is located
    - `gen_types.py`: some classes that spare me the headache of remembering the structure of tuples
    - `sampler.py`: currently implement some **very naive** assumptions of user behavior when browsing web
    - `crawler.py`: where we process the simulated browser event
- `scripts/`: some helper bash script
    - `recursive_wget.sh`: download all asset from a static site (only site hosted assets, not going to download externally linked assets such as google font)
    - `download.sh`: I have already crawled four sites, `cs.uchicago.edu/uchicago.edu/cc.gatech.edu/gatech.edu`. Running this script will download the zip for these four sites