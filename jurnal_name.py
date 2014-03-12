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

    def getkeys(self, jurl):
        baseurl = 'http://epub.cnki.net/kns/oldnavi/'
        jurl = baseurl + jurl
        html_doc = urllib.urlopen(jurl)
        soup = BeautifulSoup(html_doc)
        try:
            head = soup.find('strong', text=re.compile(u'该刊被以下数据库收录：'))
        except AttributeError:
            print 'no included'
            return []
        else:
            included = []
            while True:
                try:
                    head = head.next_sibling
                except AttributeError:
                    break
                if head is None or head.name == 'strong':
                    break
                elif head.name is None:
                    included.append(head)
        return included

    def getlist(self, soup, fput, pageid):
        j = 1
        heads = [u'中文名称', u'英文名称', u'曾用刊名',
                 u'主办单位', u'复合影响因子', u'综合影响因子', u'被引频次']
        for li in soup.find_all("div", class_="colPicText"):
            jnum = str(pageid * 10 + j)
            fput.write(jnum + '\n')
            temp = li.find('p')
            jurl = li.previousSibling.a.get('href')
            included = self.getkeys(jurl)

            def filt(h):
                if temp.find(text=re.compile(h)):
                    return temp.find(text=re.compile(h))
                else:
                    return h + u':暂无'

            print jnum, filt(heads[0]).encode('utf8')
            for k in map(lambda h: filt(h), heads):
                fput.write(k.strip().encode('utf8') + '\n')
            fput.write(u'该刊被以下数据库收录：'.encode('utf8') + '\n')
            if included == []:
                fput.write(u'暂无'.encode('utf8') + '\n')
            else:
                for icd in included:
                    fput.write(icd.encode('utf8') + '\n')
            j += 1

    def test_jurnal_name(self):
        fput = open('jurnalinfo.txt', 'wb')
        driver = self.driver
        link = self.base_url + \
            "/kns/oldnavi/n_list.aspx?NaviID=1&Field=cykm%24%25&DisplayMode=%u8be6%u7ec6%u65b9%u5f0f"
        driver.get(link)
        # can't input 1000 page
        # 999 before
        for pageid in range(993,999):
            driver.find_element_by_id("txtPageGoTo").clear()
            driver.find_element_by_id("txtPageGoTo").send_keys(str(pageid+1))
            driver.find_element_by_id("imgbtnGo").click()
            print pageid+1
            html_doc = driver.page_source
            soup = BeautifulSoup(html_doc)
            self.getlist(soup, fput, pageid)
        # 1000 later
        driver.find_element_by_id("txtPageGoTo").send_keys('999')
        driver.find_element_by_id("imgbtnGo").click()
        for pageid in range(999,1004):
            driver.find_element_by_id("lbNextPage").click()
            print pageid+1
            html_doc = driver.page_source
            soup = BeautifulSoup(html_doc)
            self.getlist(soup, fput, pageid)
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
