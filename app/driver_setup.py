from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

def initialize_driver():
    driver = webdriver.Chrome()
    chrome_options = ChromeOptions()
    return driver