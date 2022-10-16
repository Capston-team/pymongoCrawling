import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

webdriver_options = webdriver.ChromeOptions()
webdriver_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
webdriver_options.add_argument('--no-sandbox')
webdriver_options.add_argument('--headless')
# webdriver_options.add_argument("--disable-gpu")
webdriver_options.add_argument('--disable-dev-shm-usage')
# webdriver_options.add_argument("--window-size=1920,1080")
# webdriver_options.add_argument("--disable-setuid-sandbox")
# webdriver_options.add_experimental_option('excludeSwitches', ['enable-logging'])


# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=webdriver_options)
driver = webdriver.Chrome(executable_path=r'/Users/10cm_mocha/Downloads/chromedriver', options=webdriver_options)
driver.get('https://www.lguplus.com/benefit-event/ongoing')

driver.implicitly_wait(10)

membership_btn = driver.find_element(by=By.XPATH, value='//*[@id="contentsSection"]/div/div[2]/div/div/div[1]/div[1]/ul/li[4]/a')
membership_btn.click()
time.sleep(2)

event_list = driver.find_elements(by=By.XPATH, value='//*[@id="contentsSection"]/div/div[2]/div/div/div[1]/div[3]/ul')


def lg_title():
    title_list = []
    # titles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tit")))
    titles = driver.find_elements(by=By.CLASS_NAME, value="tit")

    for title in titles:
        title_list.append(title.text)

    # print(title_list)
    return title_list


def lg_date():
    date_list = []
    remove_text = ['기타', '휴대폰', '인터넷/IPTV', '스마트홈', '멤버십', '소상공인', '액세서리', '로밍', '모바일']
    # dates = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "date")))
    dates = driver.find_elements(by=By.CLASS_NAME, value="date")

    for date in dates:
        dateStr = str(date.text).replace("\n", "")

        for text in remove_text:
            dateStr = dateStr.replace(text, "")

        date_list.append(dateStr)

    # print(date_list)
    return date_list


def lg_image():
    img_list = []

    images = driver.find_elements(by=By.CLASS_NAME, value="img-area")

    for img in images:
        img = img.find_element(by=By.TAG_NAME, value="img")
        img_list.append(img.get_attribute("src"))

    # print(img_list)
    return img_list


print(lg_title())
print(lg_date())
print(lg_image())

driver.quit()