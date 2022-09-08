from time import sleep

import modules.config as config
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys  # and Krates
from selenium.webdriver.common.by import By

# from fake_useragent import UserAgent

# from pymailutils import Imap

class EmailManager():
    def __init__(self):
        self.sockets = []
        self.url = 'https://www.guerrillamail.com/'
        self.driver = self.open_browser_instance()
        self.generated_email = self.generate_email()

    def open_browser_instance(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')
        # ua = UserAgent()
        # user_agent = ua.random
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"')
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument('window-size=1200x600')
        return webdriver.Chrome(chrome_options=chrome_options, executable_path=config.Config['chromedriver_path'])
        

    def generate_email(self):
        print('Opening Browser')
        self.driver.get(self.url)

        print('Browser Opened')
        sleep(3)

        action_chains = ActionChains(self.driver)
        # fill the email value
        email_prefix = self.driver.find_element('id', 'inbox-id').get_attribute('innerText')
        email_suffix = self.driver.find_element(By.TAG_NAME, 'option').get_attribute('innerText')
        whole_email = email_prefix + "@" + email_suffix
        return whole_email

