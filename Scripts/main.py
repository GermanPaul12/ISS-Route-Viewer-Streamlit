from Scripts.keep_alive import keep_alive
from Scripts.iss import iss_checker
import time

while True:
    keep_alive()
    iss_checker()
    time.sleep(1)
