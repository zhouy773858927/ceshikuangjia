import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config , DRIVER_PATH,DATA_PATH,REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner

class TestBaidu(unittest.TestCase):
    URL = Config().get('URL')
    excel =DATA_PATH + '/baidu.xlsx'
    logger.info("url is %s" % URL)
    locator_kw = (By.ID , 'kw')
    locator_su = (By.ID , 'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def sub_setUp(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + '\chromedriver.exe')
        self.driver.get(self.URL)

    def sub_tearDown(self):
        self.driver.quit()

    def test_search_0(self):
        datas = ExcelReader(self.excel).data#获取excel中的数据
        logger.info("%s is in excel "% datas)
        for d in datas:#遍历该excel中数据
            with self.subTest(data =d):#subTest参数化
                self.sub_setUp()
                #   *为可变参数
                self.driver.find_element(*self.locator_kw).send_keys(d["search"])
                self.driver.find_element(*self.locator_su).click()
                time.sleep(2)
                logger.info("now is search %s"% d["search"])
                links = self.driver.find_elements(*self.locator_result)
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()

if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    with open(report ,'wb') as  f:
        runner = HTMLTestRunner(f, verbosity=2 ,title='测试框架',description='修改过的测试报告')
        runner.run(TestBaidu("test_search_0"))