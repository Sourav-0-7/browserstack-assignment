import os
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor

BS_USER = os.getenv("BROWSERSTACK_USERNAME")
BS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
URL = "http://hub.browserstack.com/wd/hub"

caps_list = [
    {"os": "Windows", "os_version": "10", "browser": "Chrome", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Monterey", "browser": "Safari", "browser_version": "latest"},
    {"device": "Samsung Galaxy S22", "realMobile": "true", "os_version": "12.0"},
    {"device": "iPhone 13", "realMobile": "true", "os_version": "15"},
    {"os": "Windows", "os_version": "10", "browser": "Firefox", "browser_version": "latest"}
]

def run_test(cap):
    cap['browserstack.user'] = BS_USER
    cap['browserstack.key'] = BS_KEY
    cap['name'] = "Opinion Section Test"
    driver = webdriver.Remote(command_executor=URL, desired_capabilities=cap)
    driver.get("https://elpais.com/opinion/")
    print(f"{cap.get('browser','device')}: Title is '{driver.title}'")
    driver.quit()

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as ex:
        ex.map(run_test, caps_list)
