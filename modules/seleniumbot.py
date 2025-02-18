""" author: feezyhendrix

    main function botcore
 """

from time import sleep
from random import randint

import modules.config as config
# importing generated info
import modules.generateaccountinformation as accnt
from modules.storeusername import store
# from .activate_account import get_activation_url
# library import
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys  # and Krates
import requests
import re
from modules.email_manager import EmailManager
# from fake_useragent import UserAgent

# from pymailutils import Imap

class AccountCreator():
    account_created = 0
    def __init__(self, use_custom_proxy, use_local_ip_address):
        self.sockets = []
        self.use_custom_proxy = use_custom_proxy
        self.use_local_ip_address = use_local_ip_address
        self.url = 'https://www.instagram.com/accounts/emailsignup/'
        self.__collect_sockets()


    def __collect_sockets(self):
        r = requests.get("https://www.sslproxies.org/")
        matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised_list = [m1.replace("<td>", "") for m1 in matches]
        for socket_str in revised_list:
            self.sockets.append(socket_str[:-5].replace("</td>", ":"))

    def createaccount(self, proxy=None):
        chrome_options = webdriver.ChromeOptions()
        if proxy != None:
            chrome_options.add_argument('--proxy-server=%s' % proxy)

        # chrome_options.add_argument('headless')
        # ua = UserAgent()
        # user_agent = ua.random
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"')
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument('window-size=1200x600')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=config.Config['chromedriver_path'])
        print('Opening Browser')
        driver.get(self.url)

        print('Browser Opened')
        sleep(5)

        action_chains = ActionChains(driver)
        sleep(5)
        account_info = accnt.new_account()
        email_manager = EmailManager()
        generated_email = email_manager.generated_email
        print(generated_email)
        # fill the email value
        print('Filling email field')
        email_field = driver.find_element('name', 'emailOrPhone')
        print(email_field)
        sleep(1)
        action_chains.move_to_element(email_field)
        print(account_info["email"])
        email_field.send_keys(generated_email)

        sleep(2)

        # fill the fullname value
        print('Filling fullname field')
        fullname_field = driver.find_element('name', 'fullName')
        action_chains.move_to_element(fullname_field)
        fullname_field.send_keys(account_info["name"])

        sleep(2)

        # fill username value
        print('Filling username field')
        username_field = driver.find_element('name', 'username')
        action_chains.move_to_element(username_field)
        username_field.send_keys(account_info["username"])

        sleep(2)

        # fill password value
        print('Filling password field')
        password_field = driver.find_element('name', 'password')
        action_chains.move_to_element(password_field)
        passW = account_info["password"]
        print(passW)
        password_field.send_keys(str(passW))
        sleep(1)

        sleep(2)

        submit = driver.find_element("css selector", "button[type='submit']")
        action_chains.move_to_element(submit)
        sleep(2)
        submit.click()

        sleep(3)
        try:

            month_button = driver.find_element("xpath", '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select')
            month_button.click()
            print(account_info["birthday"])
            print(account_info["birthday"].split(" "))
            print(account_info["birthday"].split(" ")[0])
            month_button.send_keys(account_info["birthday"].split(" ")[0])
            sleep(1)
            day_button = driver.find_element("xpath", '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select')
            day_button.click()
            
            
            print(account_info["birthday"].split(" ")[1].replace(",", ""))
            day_button.send_keys(account_info["birthday"].split(" ")[1].replace(",", ""))
            sleep(1)
            year_button = driver.find_element("xpath", '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select')
            year_button.click()
            year_button.send_keys(account_info["birthday"].split(" ")[2])

            sleep(2)
            next_button = driver.find_element("xpath", '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[6]')
            next_button.click()
            print("Sleeping 100 secs")
            sleep(100)

        except Exception as e :
            print(e)
            pass


        sleep(4)
        # After the first fill save the account account_info
        store(account_info)
        
        """
            Currently buggy code.
        """
        # Activate the account
        # confirm_url = get_activation_url(account_info['email'])
        # logging.info("The confirm url is {}".format(confirm_url))
        # driver.get(confirm_url)

        #driver.close()

    def creation_config(self):
        try:
            if self.use_local_ip_address == False:
                if self.use_custom_proxy == False:
                    for i in range(0, config.Config['amount_of_account']):
                        if len(self.sockets) > 0:
                            current_socket = self.sockets.pop(0)
                            try:
                                self.createaccount(current_socket)
                            except Exception as e:
                                print('Error!, Trying another Proxy {}'.format(current_socket))
                                self.createaccount(current_socket)

                else:
                    with open(config.Config['proxy_file_path'], 'r') as file:
                        content = file.read().splitlines()
                        for proxy in content:
                            amount_per_proxy = config.Config['amount_per_proxy']

                            if amount_per_proxy != 0:
                                print("Creating {} amount of users for this proxy".format(amount_per_proxy))
                                for i in range(0, amount_per_proxy):
                                    try:
                                        self.createaccount(proxy)

                                    except Exception as e:
                                        print("An error has occured" + e)

                            else:
                                random_number = randint(1, 20)
                                print("Creating {} amount of users for this proxy".format(random_number))
                                for i in range(0, random_number):
                                    try:
                                        self.createaccount(proxy)
                                    except Exception as e:
                                        print(e)
            else:
                for i in range(0, config.Config['amount_of_account']):
                            try:
                                self.createaccount()
                            except Exception as e:
                                print(e)
                                print('Error!, Check its possible your ip might be banned')
                                self.createaccount()


        except Exception as e:
            print(e)

def runbot():
    account = AccountCreator(config.Config['use_custom_proxy'], config.Config['use_local_ip_address'])
    account.creation_config()
