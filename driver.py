import sys
import random
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ReadTimeoutError

from locs import geeksforgeeks_locs, github_locs, google_locs, yahoo_locs

targets = {
    "github.com": github_locs,
    "geeksforgeeks.org": geeksforgeeks_locs,
    "google.com": google_locs,
    "yahoo.com": yahoo_locs,
}

def wait_for_page_load(driver, timeout=30):
   def page_loaded(driver):
       return driver.execute_script("return document.readyState") == "complete"

   wait = WebDriverWait(driver, timeout)
   wait.until(page_loaded)

def main():
    driver = webdriver.Firefox()

    keys = list(targets.keys())

    indexes = {}
    totalLen = 0

    for key in keys:
        indexes[key] = 0
        totalLen += len(targets[key])

    queue = []

    while (sum(indexes.values()) < totalLen):
        incompleteKeys = []
        for i in range(0, len(keys)):
            if indexes[keys[i]] < len(targets[keys[i]]):
                incompleteKeys.append(keys[i])
                
        randomKey = random.choice(incompleteKeys)
        
        queue.append((randomKey, targets[randomKey][indexes[randomKey]]))
        indexes[randomKey] += 1

    while len(queue) > 0:
        target = queue.pop(0)
        targetDomain = target[0]
        targetURL = target[1]
        print(target[1], file=sys.stderr)
        print(f"{target[0]}, {time.time():.9f}, {target[1]}, start")
        try: 
            driver.get(targetURL)
            wait_for_page_load(driver)
        except ReadTimeoutError:
            print(f"{target[1]} ReadTimeoutError", file=sys.stderr)
        except:
            print(f"{target[1]} Other Error", file=sys.stderr)
        time.sleep(5)
        print(f"{target[0]}, {time.time():.9f}, {target[1]}, end")
        time.sleep(5)



if __name__ == "__main__":
    main()
