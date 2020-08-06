import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains


class Reporter:
    def __init__(self, email, passwd, proxy=''):
        self.email = email
        self.passwd = passwd
        chrome_options = webdriver.ChromeOptions()
        if proxy != '':
            chrome_options.add_argument('--proxy-server=%s' % proxy)
        self.driver = webdriver.Chrome("../drivers/chromedriver.exe", options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("https://mail.google.com/mail/")
        self.login()
        self.start_reporting()

    def __del__(self):
        print('Destructor called, Reporter deleted.')

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
        self.driver.close()
        del self

    def login(self):
        user = self.find_elements(ec.presence_of_element_located((By.XPATH, "//*[@type='email']")))
        if user:
            user.send_keys(self.email)
            user.send_keys(Keys.ENTER)
        else:
            self.next_op()
        userpswd = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@type='password']")))
        time.sleep(2)
        if userpswd:
            userpswd.send_keys(self.passwd)
            userpswd.send_keys(Keys.ENTER)
        else:
            self.next_op()
        time.sleep(2)
        self.driver.get("https://mail.google.com/mail/u/0/h/")
        time.sleep(2)
        us_html = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@id='maia-main']/form/p/input")))
        time.sleep(2)
        if us_html:
            us_html.click()
        else:
            self.driver.get("https://mail.google.com/mail/u/0/h/")
            html = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@id='maia-main']/form/p/input")))
            time.sleep(2)
            if html:
                html.click()

    def open_action(self, action=1):
        limit = randint(20, 35)
        times = 1
        selector = "ts"
        print("open_action [" + str(action) + "] = [" + selector + "] ", limit)
        while self.open_email(selector) is not False and times <= limit:
            if action == 1:
                self.archive("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/table[1]/tbody/tr/td["
                             "1]/input[4]")
                inbx = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@href='?&']")))
                if inbx:
                    inbx.click()
                time.sleep(2)
            else:
                self.legitime("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/table[1]/tbody/tr/td["
                              "1]/input[5]")
                spam = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@href='?&s=m']")))
                if spam:
                    spam.click()
                time.sleep(2)
            times += 1

    def select_action(self, action=1):
        time.sleep(2)
        emails = self.find_elements(ec.presence_of_all_elements_located(
            (By.XPATH, "//*[@type='checkbox']")))
        time.sleep(2)
        if emails and len(emails) > 1:
            while emails:
                limit = randint(10, 25)
                times = 1
                print("select_action [" + str(action) + "] = ", limit)
                for email in emails:
                    ActionChains(self.driver).move_to_element(email).click().perform()
                    times += 1
                    if times == limit:
                        break
                if times > 1:
                    if action == 1:
                        self.archive("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table["
                                     "1]/tbody/tr/td[1]/input[1]")
                    else:
                        self.legitime("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table["
                                      "1]/tbody/tr/td[1]/input[2]")
                time.sleep(4)
                emails = self.find_elements(ec.presence_of_all_elements_located((By.XPATH, "//*[@type='checkbox']")))

    def open_email(self, selector):
        time.sleep(2)
        emails = self.find_elements(ec.element_to_be_clickable((By.CLASS_NAME, selector)))
        time.sleep(2)
        if emails:
            emails.click()
            return True
        else:
            return False

    def archive(self, path):
        try:
            time.sleep(2)
            archv = self.find_elements(ec.element_to_be_clickable((By.XPATH, path)))
            if archv:
                archv.click()
            time.sleep(2)
        except Exception as c:
            print("Exception (archive) ", str(c))

    def legitime(self, path):
        try:
            time.sleep(2)
            legitimebtn = self.find_elements(ec.visibility_of_element_located(
                (By.XPATH, path)))
            if legitimebtn:
                legitimebtn.click()
            time.sleep(2)
        except Exception as c:
            print("Exception (legitime) ", str(c))

    def reporting(self, action=1):
        self.open_action(action)
        time.sleep(2)
        self.select_action(action)

    def start_reporting(self):
        try:
            time.sleep(2)
            self.reporting(1)
            time.sleep(2)
            spam = self.find_elements(ec.visibility_of_element_located((By.XPATH, "//*[@href='?&s=m']")))
            if spam:
                spam.click()
            time.sleep(2)
            self.reporting(2)
            time.sleep(2)
            self.driver.get("https://mail.google.com/mail/u/0/h/")
            time.sleep(2)
            self.reporting(1)
            time.sleep(5)
            self.next_op()
        except Exception as c:
            print("Exception (start_reporting) ", str(c))
            self.next_op()
