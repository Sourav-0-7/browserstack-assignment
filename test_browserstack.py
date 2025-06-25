import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
REMOTE_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

capabilities_list = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Chrome Test"
        }
    },
    {
        "browserName": "Edge",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Edge Test"
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Safari Test"
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Firefox Test"
        }
    },
    {
        "browserName": "Chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "realMobile": "true",
            "osVersion": "13.0",
            "sessionName": "Mobile Test"
        }
    }
]

def run_browserstack_test(cap):
    name = cap.get("browserName") or cap["bstack:options"].get("deviceName", "Unnamed")
    try:
        print(f"➡️  Starting test: {name}")
        
        # Select the appropriate Options class based on browserName
        browser_name = cap.get("browserName", "").lower()
        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        elif browser_name == "edge":
            options = EdgeOptions()
        elif browser_name == "safari":
            options = SafariOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Set BrowserStack capabilities
        for key, value in cap.items():
            if key != "bstack:options":
                options.set_capability(key, value)
        options.set_capability("bstack:options", cap["bstack:options"])

        # Initialize WebDriver with options
        driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
        driver.get("https://elpais.com/opinion/")
        print(f"✅ [{name}] Title: {driver.title}")
        driver.quit()
    except Exception as e:
        print(f"❌ [{name}] Error running test: {e}")

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_browserstack_test, capabilities_list)