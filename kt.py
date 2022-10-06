import os

from selenium.webdriver.chromium.service import ChromiumService
from webdriver_manager.core.utils import ChromeType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


webdriver_options = webdriver.ChromeOptions()
webdriver_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
webdriver_options.add_argument('--no-sandbox')
webdriver_options.add_argument('--headless')
webdriver_options.add_argument("--disable-gpu")
webdriver_options.add_argument('--disable-dev-shm-usage')
webdriver_options.add_argument("--window-size=1920,1080")
webdriver_options.add_argument("--disable-setuid-sandbox")
webdriver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=webdriver_options)
driver = webdriver.Chrome(executable_path=r'/Users/10cm_mocha/Downloads/chromedriver', options=webdriver_options)
driver.get('https://event.kt.com/html/event/ongoing_event_list.html')

# 암시적 대기 - 페이지가 로드될 때까지 기다리다가 실행해라.
driver.implicitly_wait(10)

select_element = driver.find_element(by=By.ID, value="search-select")
select_object = Select(select_element)

select_object.select_by_value("02")
driver.find_element(by=By.XPATH, value='//*[@id="cfmClContents"]/div[2]/div/div/div[1]/div[2]/button').click()
time.sleep(2)

next_button = driver.find_element(by=By.XPATH, value='//*[@id="cfmClContents"]/div[2]/div/div/div[3]/div/a[5]')


def kt_title():
    title_list = []
    # title = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title")))
    title = driver.find_elements(by=By.CLASS_NAME, value="title")
    for element in title:
        title_list.append(element.text)

    return title_list


def kt_date():
    date_list = []
    # date = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "date")))
    date = driver.find_elements(by=By.CLASS_NAME, value="date")
    for element in date:
        date_list.append(element.text)

    return date_list


def kt_image():
    img_list = []
    # thumb = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "thumb")))
    thumb = driver.find_elements(by=By.CLASS_NAME, value="thumb")

    for element in thumb:
        img = element.find_element(by=By.TAG_NAME, value="img")
        img_list.append(img.get_attribute("src"))

    return img_list


driver.quit()

