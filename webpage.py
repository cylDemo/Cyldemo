"""
selenium基类
存放了selenium基类东东封装方法
"""
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from config.conf import cm
from utils.times import sleep
from utils.logger import log


class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)


    def get_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            log.info("打开网址：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)


    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        print('locator元素：', locator)
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """查找多个相同元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format({locator, number}))
        return number

    def input_text(self, locator, txt):
        """输入（输入前先清空）"""
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        log.info("输入文本：{}".format(txt))

    def is_click(self, locator):
        """点击"""
        self.find_element(locator).click()
        sleep(3)
        log.info("点击元素：{}".format(locator))

    def elements_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text

    @property
    def get_source(self):
        """获取页面源代码（已转义）"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)
        log.info('刷新页面成功！')

    def move_to_element(self, locator):
        """移动至目标元素悬停"""
        element_text = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element_text)
        action.perform()

    @property
    def get_resource_no_escape(self):
        """获取未转义的页面源代码"""
        url = self.driver.current_url
        re = requests.get(url)
        return re.text

    @property
    def back(self):
        """页面后退"""
        self.driver.back()

    @property
    def forware(self):
        """页面前进"""
        self.driver.forware()


















