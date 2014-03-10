# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import re
import urllib
from bs4 import BeautifulSoup


class JurnalName(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://epub.cnki.net/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def getlist(self, soup, fput):
        # link = 'http://epub.cnki.net/kns/oldnavi/n_list.aspx?NaviID=1&Field=cykm$%&DisplayMode=%E8%AF%A6%E7%BB%86%E6%96%B9%E5%BC%8F'
        heads = [u'中文名称', u'英文名称', u'曾用刊名',
                 u'主办单位', u'复合影响因子', u'综合影响因子', u'被引频次']
        for li in soup.find_all("div", class_="colPicText"):
            temp = li.find('p')

            def filt(h):
                if temp.find(text=re.compile(h)):
                    return temp.find(text=re.compile(h))
                else:
                    return h + u':暂无'

            for k in map(lambda h: filt(h), heads):
                fput.write(k.strip().encode('utf8') + '\n')
            fput.write('\n')

    def test_jurnal_name(self):
        fput = open('jurnalinfo.txt', 'wb')
        driver = self.driver
        link = self.base_url + \
            "/kns/oldnavi/n_list.aspx?NaviID=1&Field=cykm%24%25&DisplayMode=%u8be6%u7ec6%u65b9%u5f0f"
        driver.get(link)
        for pageid in range(1, 1004):
            driver.find_element_by_id("txtPageGoTo").clear()
            driver.find_element_by_id("txtPageGoTo").send_keys(str(pageid))
            driver.find_element_by_id("imgbtnGo").click()
            print pageid
            html_doc = driver.page_source
            soup = BeautifulSoup(html_doc)
            self.getlist(soup, fput)
        fput.close()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
