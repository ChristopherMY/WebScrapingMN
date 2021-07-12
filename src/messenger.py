import logging
from sys import maxsize
import traceback
import sys
from urllib.parse import uses_fragment
import requests
from selenium import webdriver
import selenium

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from bs4 import BeautifulSoup

from time import sleep, time


class MessengerElements:
    search = (By.CSS_SELECTOR, "#u_0_1_s2 > div > div > div > div > table > tbody > tr > td._1-9p._51m-.vTop > div > div:nth-child(1) > div > label > input")
    inputText = (By.CSS_SELECTOR,
                 "#js_em3 > div > div._4dw9 > div._4dv- > div > div > div > div > div > div > div > div > div > span > span")


class Messenger:
    browser = None
    size = 0
    time = 15
    timeout = 15

    logger = logging.getLogger('django.project.requests')
    selenium_retries = 0


    def __init__(self, wait, url):
        self.url = url

    def get_selenium_res(self, class_name):
            
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value,
                                OperatingSystem.LINUX.value]

            user_agent_rotator = UserAgent(software_names = software_names,
            operating_systems = operating_systems, limit=100)

            user_agent = user_agent_rotator.get_random_user_agent()

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1420,1080")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument(f"user-agent={user_agent}")
            executable_path=""

            PROXY = "http://209.45.61.108:3128"
            
            chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

            prox = Proxy()
            prox.proxy_type = ProxyType.MANUAL
            prox.auto_detect = False
            capabilities = webdriver.DesiredCapabilities.CHROME
            prox.http_proxy = PROXY
            prox.ssl_proxy = PROXY
            prox.add_to_capabilities(capabilities=capabilities)

            browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)

            browser.get(self.url)

            time_to_sleep = 90
            
            try:
                WebDriverWait(browser, time_to_sleep).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))                
            finally:
                browser.maximize_window()
                page_html = browser.page_source
                browser.close()
                return page_html

        except (TimeoutException, WebDriverException):
            self.logger.error(traceback.format_exc())
            sleep(6)
            self.selenium_retries += 1
            self.logger.info('Selenium retry #: ' + str(self.selenium_retries))
            return self.get_selenium_res(class_name)