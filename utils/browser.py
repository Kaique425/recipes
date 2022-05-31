import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROME_DRIVE_NAME = "chromedriver"
CHROME_DRIVER_PATH = ROOT_PATH / "bin" / CHROME_DRIVE_NAME


def create_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == "True":
        chrome_options.add_argument("--headless")

    chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    os.environ.get("SELENIUM_HEADLESS")
    browser = create_browser("--headless")
    browser.get("http://www.youtube.com")
    sleep(1)
    browser.quit()
