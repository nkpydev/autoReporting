import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains


def blocked(email):
    print("Exited from  ", email)
    f = open("blockeddata.txt", "a")
    f.write(email+"\n")
    f.close()


class Reporter:
    def __init__(self, email, passwd, proxy=''):
        self.flag = True
        self.email = email
        self.passwd = passwd
        chrome_options = webdriver.ChromeOptions()
        if proxy != '':
            chrome_options.add_argument('--proxy-server=%s' % proxy)
        self.driver = webdriver.Chrome("../drivers/chromedriver.exe", options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("https://mail.google.com/mail/")
        self.login()
        if self.flag:
            time.sleep(14)
            path = "//*[@id='owaSettingsButton'] | //*[@id='headerButtonsRegionId']"
            path += "/div/button/i[@data-icon-name='Settings']/.."
            stng = self.find_elements(ec.visibility_of_element_located((By.XPATH, path)))
            if not stng:
                blocked(self.email)
                self.next_op()
        else:
            self.next_op()

    def __del__(self):
        print('Destructor called, Reporter deleted.', self.email)

    def find_elements(self, v, timeout=40, times=0):
        try:
            times += 1
            ele = WebDriverWait(self.driver, timeout).until(v)
            if ele is not None:
                return ele
            else:
                return False
        except (WebDriverException, TimeoutException, Exception) as c:
            print("Exception times(" + str(times) + ") [" + str(v.locator) + "]", str(c))
            if times == 4:
                return False
            else:
                self.find_elements(v, timeout, times)

    def next_op(self):
        self.flag = False
        self.driver.close()
        del self.driver

    def login(self):
        user = self.find_elements(ec.presence_of_element_located((By.XPATH, "//*[@type='email']")))
        if user:
            user.send_keys(self.email)
            user.send_keys(Keys.ENTER)
            userpswd = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@type='password']")))
            time.sleep(2)
            if userpswd:
                userpswd.send_keys(self.passwd)
                userpswd.send_keys(Keys.ENTER)
                time.sleep(2)
                self.driver.get("https://mail.google.com/mail/u/0/h/")
                time.sleep(2)
                us_html = self.find_elements(
                    ec.visibility_of_element_located((By.XPATH, "//*[@id='maia-main']/form/p/input")))
                time.sleep(2)
                if us_html:
                    us_html.click()
                else:
                    self.driver.get("https://mail.google.com/mail/u/0/h/")
                    html = self.find_elements(
                        ec.visibility_of_element_located((By.XPATH, "//*[@id='maia-main']/form/p/input")))
                    time.sleep(2)
                    if html:
                        html.click()
            else:
                self.next_op()
        else:
            self.next_op()