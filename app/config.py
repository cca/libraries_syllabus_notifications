import logging
import time

# there's probably a more elegant way to do this but hey this works and took me hours
# log to both (dated) file & console
format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format=format,
    filename='data/{today}.log'.format(today=time.strftime('%Y-%m-%d')),
)
formatter = logging.Formatter(format)
logger = logging.getLogger()
# add 2nd handler for console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)
