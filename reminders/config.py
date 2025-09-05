import logging
import os
import time
from typing import Any

from dotenv import dotenv_values

config: dict[str, Any] = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), ".env")),
    **os.environ,  # override loaded values with environment variables
}

# there's probably a more elegant way to do this but hey this works and took me hours
# log to both (dated) file & console
format: str = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    level=logging.DEBUG if config.get("DEBUG") else logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format=format,
    filename="data/{today}.log".format(today=time.strftime("%Y-%m-%d")),
)
formatter = logging.Formatter(format)
logger: logging.Logger = logging.getLogger()
# add 2nd handler for console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)
