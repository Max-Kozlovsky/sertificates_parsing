import time

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def get_url():
    browser.get('https://pub.fsa.gov.ru/rss/certificate')
    start_parsing = input('После окончания настроек нажмите ENTER')
    time.sleep(1)
    target = browser.find_element(By.XPATH, "//div[contains(@class, 'wtHolder')]")
    actions = ActionChains(browser)
    actions.move_to_element(target)
    for _ in range(5):
        actions.send_keys(Keys.END)
    actions.perform()

    time.sleep(1)
    links = browser.find_elements(By.XPATH, "//td[3]/a[contains(@data-href, '/rss/certificate/view')]")
    for link in links:
        try:
            print(link.get_attribute('data-href'))
        except StaleElementReferenceException:
            pass


option = Options()
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/100.0.4896.127 Safari/537.36")
browser = webdriver.Chrome(options=option)
try:
    get_url()
finally:
    browser.quit()
