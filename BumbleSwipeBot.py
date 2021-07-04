from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from secrets import username, password

import xpaths

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.likes=0

    def open_login(self):
        self.driver.get('https://bumble.com/get-started')
        self.facebook_login()

    def facebook_login(self):
        #we will only login using fb credentials. fb creds are stored in secrets.py, you can enter your creds
        fb_login_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,xpaths.fb_login_btn_xpath)))
        fb_login_btn.click()
        self.handle_fb_login_popup()
        #try reclick on this button incase it didnt login
        try:
            fb_login_btn.click()
        except Exception:
            print("fb login btn click didnt work for 2nd time")
        self.swipe_it_away()
        
    def handle_fb_login_popup(self):
        base_window = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath(xpaths.fb_popup_email_inp_xpath)
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath(xpaths.fb_popup_pass_inp_xpath)
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath(xpaths.fb_popup_login_btn_xpath)
        login_btn.click()
        #for 2FA approvals
        sleep(20)
        self.driver.close()
        self.driver.switch_to.window(base_window)
        
    def swipe_it_away(self):
        while True:
            sleep(1)
            try:
                self.like()
            except Exception:
                print("shutting down... no more likes left for the day")
                sleep(30)
                self.driver.close()

    def like(self):
        self.likes=self.likes+1
        print("liked "+str(self.likes))
        like_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,xpaths.like_btn_xpath)))
        like_btn.click()
 
bot = TinderBot()
bot.open_login()