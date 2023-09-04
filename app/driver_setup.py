from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def initialize_driver():
    driver = webdriver.Chrome()
    chrome_options = ChromeOptions()
    return driver, chrome_options