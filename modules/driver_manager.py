from selenium import webdriver


class WebDriverManager:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = webdriver.Chrome()
        return cls._driver
