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

    """get settings"""
    start_parsing = input('После окончания настроек нажмите ENTER')
    time.sleep(2)

    """pagination"""
    count_elements = browser.find_element(By.XPATH, "//span[contains(@class, 'ng-star-inserted')]").text.split()[-1]
    print(f"Обнаружено {count_elements} сертификатов на {int(count_elements) // 10 + 1} страницах")

    """scrap certificate links"""
    links = browser.find_elements(By.XPATH, "//td[3]/a[contains(@data-href, '/rss/certificate/view')]")
    link_list = [link.get_attribute('data-href') for link in links]
    target = browser.find_element(By.XPATH, "//a[contains(@href, '/rss/certificate/view')]")
    target.click()
    actions = ActionChains(browser)
    actions.move_to_element(target)
    actions.send_keys(Keys.END)
    try:
        actions.perform()
    except StaleElementReferenceException:
        pass
    time.sleep(2)
    add_links = browser.find_elements(By.XPATH, "//td[3]/a[contains(@data-href, '/rss/certificate/view')]")
    for new_link in add_links:
        if new_link.get_attribute('data-href') not in link_list:
            link_list.append(new_link.get_attribute('data-href'))
    link_list = [HOST + link for link in link_list]
    for elem in link_list:
        url = requests.get(elem + '/applicant', verify=False)
        soup = BeautifulSoup(url.content, 'html.parser')
        print(soup)
        break
        # driver = webdriver.Chrome()
        # driver.get(elem + '/applicant')
        # driver.implicitly_wait(10)
        # production = driver.find_element(By.XPATH,
        #                                  "//div/div[3]/div[contains(@class, 'card-view-toolbar__info-text vertical-text-break')]").text
        # appplicant = driver.find_element(By.XPATH,
        #                                  "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[1]/fgis-card-info-row[1]/div[2]/span").text
        # i_number = driver.find_element(By.XPATH,
        #                                "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[1]/div/div[2]/div/fgis-card-info-row/div[2]/span").text
        # surname = driver.find_element(By.XPATH,
        #                               "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[4]/fgis-card-info-row[1]/div[2]/span").text
        # name = driver.find_element(By.XPATH,
        #                            "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[4]/fgis-card-info-row[2]/div[2]/span").text
        # second_name = driver.find_element(By.XPATH,
        #                                   "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-edit-row-two-columns[5]/fgis-card-info-row[1]/div[2]/span").text
        # telephone = driver.find_element(By.XPATH,
        #                                 "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[4]/div/div[2]/div/fgis-card-edit-row[1]/div[2]/fgis-field-complex-input-multi/div/div/span").text
        # mail = driver.find_element(By.XPATH,
        #                            "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[4]/div/div[2]/div/fgis-card-edit-row[2]/div[2]/fgis-field-complex-input-multi/div/div/span").text
        # register = driver.find_element(By.XPATH,
        #                                "/html/body/fgis-root/div/fgis-rss-view-certificate/div/div/div/div/fgis-rss-view-application-applicant/fgis-card-block/div/div[2]/div/fgis-card-block[1]/div/div[2]/div/fgis-card-edit-row-two-columns[1]/fgis-card-info-row[1]/div[2]/span").text
        # register_link = elem
        # print(production, appplicant, i_number, surname, name, second_name, telephone, mail, register, register_link)


HOST = 'https://pub.fsa.gov.ru'
option = Options()
option.add_argument('--start-maximized')
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/100.0.4896.127 Safari/537.36")
browser = webdriver.Chrome(options=option)
try:
    get_url()
finally:
    browser.quit()
