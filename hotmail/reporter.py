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
        self.driver.get("https://outlook.live.com/owa/?nlp=1")
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
                # self.change_setting()
                self.start_reporting()
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
        self.driver.quit()
        del self.driver

    def login(self):
        user = self.find_elements(ec.presence_of_element_located((By.ID, "i0116")))
        if user:
            user.send_keys(self.email)
            user.send_keys(Keys.ENTER)
            userpswd = self.find_elements(ec.visibility_of_element_located((By.ID, "i0118")))
            time.sleep(2)
            if userpswd:
                userpswd.send_keys(self.passwd)
                sign_in = self.find_elements(ec.element_to_be_clickable((By.ID, "idSIButton9")))
                time.sleep(2)
                if sign_in:
                    sign_in.click()
                else:
                    self.next_op()
            else:
                self.next_op()
        else:
            self.next_op()

    def change_setting(self):
        # //*[@id='headerButtonsRegionId']/div/button/i[@data-icon-name='Settings']/..  #setting
        # aria-label="Settings"
        # Newest messages on top
        # /html/body/div[8]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div
        # Reading pane
        # /html/body/div[8]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[4]/div[2]/div/div/div[1]/div
        # darkMode
        # //*[@id='options-quick-darkMode']/div[2]/div/button
        # quick_focused
        # //*[@id='options-quick-focused']/div[2]/div/button
        # sender_image
        # //*[@id='options-quick-senderImage']/div[2]/div/button
        # date_headers
        # //*[@id='options-quick-dateHeaders']/div[2]/div/button
        # inline_previews
        # //*[@id='options-quick-inlinePreviews']/div[2]/div/button
        # message_preview
        # //*[@id='options-quick-messagePreview']/div[2]/div/button
        # close settings
        # /html/body/div[8]/div/div/div/div[1]
        time.sleep(14)
        path = "//*[@id='owaSettingsButton'] | //*[@id='headerButtonsRegionId']"
        path += "/div/button/i[@data-icon-name='Settings']/.."
        stng = self.find_elements(ec.visibility_of_element_located((By.XPATH, path)))
        if stng:
            stng.click()
            time.sleep(5)
            path = "//*[@id='CustomFlexPane_OwaSettings']/div/div/div[2]/div/div[6]"
            path += "/div[2]/div/div/div[2]/div | /html/body/div[8]/div/div/div/div[2]/div[3]/div/div/div/div/div[2]/"
            path += "div/div[3]/div[2]/div/div/div[1]/div"
            newest = self.find_elements(ec.element_to_be_clickable((By.XPATH, path)))
            if newest:
                newest.click()
                time.sleep(4)
                path = "//*[@id='CustomFlexPane_OwaSettings']/div/div/div[2]/div/div[7]/div[2]"
                path += "/div/div/div[1]/div | /html/body/div[8]/div/div/div/"
                path += "div[2]/div[3]/div/div/div/div/div[2]/div/div[4]/div[2]/div/div/div[1]/div"
                reading_pane = self.find_elements(ec.visibility_of_element_located((By.XPATH, path)))
                if reading_pane:
                    reading_pane.click()
                    time.sleep(2)
                    dark_mode = self.find_elements(
                        ec.element_to_be_clickable((By.XPATH, "//*[@id='options-quick-darkMode']/div[2]/div/button")))
                    if dark_mode and dark_mode.get_attribute("aria-checked") == "false":
                        dark_mode.click()
                    time.sleep(2)
                    focused = self.find_elements(
                        ec.element_to_be_clickable((By.XPATH, "//*[@id='options-quick-focused']/div[2]/div/button")))
                    if focused and focused.get_attribute("aria-checked") == "true":
                        focused.click()
                    time.sleep(2)
                    # sender_image = self.find_elements(
                    # ec.element_to_be_clickable((By.XPATH, "//*[@id='options-quick-senderImage']/div[2]/div/button")))
                    # if sender_image and sender_image.get_attribute("aria-checked") == "true":
                    #     sender_image.click()
                    # time.sleep(2)
                    # date_headers = self.find_elements(
                    # ec.element_to_be_clickable((By.XPATH, "//*[@id='options-quick-dateHeaders']/div[2]/div/button")))
                    # if date_headers and date_headers.get_attribute("aria-checked") == "true":
                    #     date_headers.click()
                    # time.sleep(2)
                    # inline_previews = self.find_elements(ec.element_to_be_clickable((By.XPATH,
                    # "//*[@id='options-quick-inlinePreviews']/div[2]/div/button")))
                    # if inline_previews and inline_previews.get_attribute("aria-checked") == "false":
                    #     inline_previews.click()
                    # time.sleep(2)
                    # message_preview = self.find_elements(
                    # ec.element_to_be_clickable((By.XPATH,
                    # "//*[@id='options-quick-messagePreview']/div[2]/div/button")))
                    # if message_preview and message_preview.get_attribute("aria-checked") == "false":
                    #     message_preview.click()
                    # time.sleep(2)
                    if stng:
                        stng.click()
                else:
                    self.next_op()
            else:
                self.next_op()
        else:
            self.next_op()

    def open_action(self, action=1):
        # //*[@class='_1t7vHwGnGnpVspzC4A22UM']/div/div/div/div   click on email
        limit = randint(20, 35)
        times = 1
        selector = "//*[@class='_3HQ_h7iVcVeOo03bOFpl__']|//*[@class='_2miAFnGHXlWwulyUmLEbzZ']"
        if action == 1:
            selector = "//*[@class='_1mLYmTUS21AGg7NMqFD_vN']|//*[@class='_2miAFnGHXlWwulyUmLEbzZ']"
        print("open_action [" + str(action) + "] = [" + selector + "] ", limit)
        while self.open_email(selector) is not False and times <= limit:
            if action == 1:
                self.archive()
            else:
                self.legitime()
            times += 1

    def select_action(self, action=1):
        # //*[@class='_1t7vHwGnGnpVspzC4A22UM']/div/div/div/div/div[1]/div    select radio_btn
        time.sleep(2)
        emails = self.find_elements(ec.presence_of_all_elements_located(
            (By.XPATH, "//*[@class='ms-Check Gf34lTXaawF-k_uax2cC root-84']|//*[@class='_2mUsG1A3iMqm06ISyGknWQ']")))
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
                        self.archive()
                    else:
                        self.legitime()
                time.sleep(4)
                by_xpath = "//*[@class='ms-Check Gf34lTXaawF-k_uax2cC root-84']|//*[@class='_2mUsG1A3iMqm06ISyGknWQ']"
                emails = self.find_elements(ec.presence_of_all_elements_located((By.XPATH, by_xpath)))

    def open_email(self, selector):
        time.sleep(2)
        emails = self.find_elements(ec.element_to_be_clickable((By.XPATH, selector)))
        time.sleep(2)
        if emails:
            emails.click()
            return True
        else:
            return False

    def archive(self):
        # //*[@id='app']/div/div[2]/div/div[1]/div[3]/div[1]/div/div/div/div/div[1]/div/button/div/
        # i[@data-icon-name="Archive"]/../../..  #Archiver
        try:
            time.sleep(2)
            path = "//*[@id='app']/div/div[2]/div/div[1]/div[3]/div[1]/div/div/div"
            path += "/div/div[1]/div/button/div/i[@data-icon-name='Archive']/../../.."
            archv = self.find_elements(ec.element_to_be_clickable((By.XPATH, path)))
            if archv:
                archv.click()
            time.sleep(2)
        except Exception as c:
            print("Exception (archive) ", str(c))

    def legitime(self):
        # dropdwn
        # //*[@id='app']/div/div[2]/div/div[1]/div[3]/div[1]/div/div/div/div/div[1]/div/button[@name='Not junk']/..
        # |//*[@id='app']/div/div[2]/div/div[1]/div[3]/div[1]/div/div/div/div/div[1]/div/
        # button[@name='Courrier légitime']/..
        # /html/body/div[*]/div/div/div/div/div/div/ul/li[1]  #Courrier légitime button
        try:
            time.sleep(2)
            path = "//*[@id='app']/div/div[2]/div/div[1]/div[3]/div[1]/div/div/div/div/div[1]"
            path += "/div/button[@name='Not junk']/..|//*[@id='app']/div/div[2]/div/div[1]/div[3]/"
            path += "div[1]/div/div/div/div/div[1]/div/button[@name='Courrier légitime']/.."
            legitimedrp = self.find_elements(ec.visibility_of_element_located((By.XPATH, path)))
            if legitimedrp:
                legitimedrp.click()
            time.sleep(2)
            legitimebtn = self.find_elements(ec.visibility_of_element_located(
                (By.XPATH, "/html/body/div[*]/div/div/div/div/div/div/ul/li[1]")))
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
            # //*[@data-icon-name='Blocked']/..
            self.driver.get("https://outlook.live.com/mail/junkemail")
            time.sleep(2)
            self.reporting(2)
            time.sleep(2)
            self.driver.get("https://outlook.live.com/mail/inbox")
            time.sleep(2)
            self.reporting(1)
            time.sleep(5)
            self.next_op()
            return
        except Exception as c:
            print("Exception (start_reporting) "+self.email, str(c))
            self.next_op()
            return
