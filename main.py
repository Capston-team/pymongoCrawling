from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

sched = BlockingScheduler(timezone='Asia/Seoul')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_database():
    ca = certifi.where()

    CONNECTION_STRING = "mongodb+srv://YoungWoo:vbn752014&@capstone.qv9bkyx.mongodb.net/?retryWrites=true&w=majority&ssl=true"

    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    return client['event']


def skt_dict():
    url_date = "https://sktmembership.tworld.co.kr/mps/pc-bff/program/tday.do"
    response = requests.get(url_date)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    date_events = soup.find_all('div', attrs={"data-move-scroll": "DISCOUNT_20221005_WEEK_BENEFIT"})
    date_list = []
    for event in date_events:
        date = event.find_all(attrs={'class': 'benefit-date'})

        # event에서 텍스트를 읽어옴, 제목을 읽어오는 것
        # title = str(title.select('span'))
        date = str(date)
        date = re.sub('<.+?>', '', date, 0).strip()
        date = re.sub("\\[", '', date, 0)
        date = re.sub("]", '', date, 0)
        date = date.split(', ')

        remove_word = "week1 혜택"
        remove_word2 = "유의 사항"
        remove_word3 = "Day2 혜택"

        # 해당 word가 title 리스트에서 remove_word, remove_word2에 해당한다면 제거
        for word in date:
            if remove_word in word:
                date.remove(word)
            if remove_word2 in word:
                date.remove(word)

        # title 리스트에 해당 인덱스의 문자열에 remove_word, remove_word2가 있다면 제거, 공백 제거 후 반환
        for i, word in enumerate(date):
            if remove_word in word:
                date[i] = word.strip(remove_word)
            if remove_word2 in word:
                date[i] = word.strip(remove_word2)

        date_list = date

    title_list = []
    date_events = soup.find_all('div', attrs={"data-move-scroll": "DISCOUNT_20221005_WEEK_BENEFIT"})

    # 'p'태그를 가지고 class명이 title인 element를 모두 가져와 events에 저장함
    for event in date_events:
        description = str(event.select('.tday-info > .tit'))
        description = re.sub('<.+?>', '', description, 0).strip()
        description = re.sub("\\[", '', description, 0)
        description = re.sub("]", '', description, 0)
        description = description.split(', ')
        title_list = description


    context = ssl._create_unverified_context()
    result = urlopen("https://sktmembership.tworld.co.kr/mps/pc-bff/program/tday.do", context=context)
    soup = BeautifulSoup(result.read(), "html.parser")

    date_events = soup.find_all('div', attrs={"data-move-scroll": "DISCOUNT_20221005_WEEK_BENEFIT"})
    img_link = []

    for event in date_events:
        img = event.select('.img-box > img')

        for i in img:
            img_link.append(i['src'])

    return dict({'title': title_list, 'date': date_list, 'img': img_link})


def kt_dict():
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument("--disable-gpu")
    webdriver_options.add_argument('--disable-dev-shm-usage')
    webdriver_options.add_argument("--window-size=1920,1080")
    webdriver_options.add_argument("--disable-setuid-sandbox")
    webdriver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=webdriver_options)
    # driver = webdriver.Chrome(executable_path=r'/Users/10cm_mocha/Downloads/chromedriver', options=webdriver_options)
    driver.get('https://event.kt.com/html/event/ongoing_event_list.html')

    # 암시적 대기 - 페이지가 로드될 때까지 기다리다가 실행해라.
    driver.implicitly_wait(10)

    select_element = driver.find_element(by=By.ID, value="search-select")
    select_object = Select(select_element)

    select_object.select_by_value("02")
    driver.find_element(by=By.XPATH, value='//*[@id="cfmClContents"]/div[2]/div/div/div[1]/div[2]/button').click()
    time.sleep(2)

    next_button = driver.find_element(by=By.XPATH, value='//*[@id="cfmClContents"]/div[2]/div/div/div[3]/div/a[5]')

    title_list = []
    # title = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title")))
    title = driver.find_elements(by=By.CLASS_NAME, value="title")
    for element in title:
        title_list.append(element.text)

    date_list = []
    # date = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "date")))
    date = driver.find_elements(by=By.CLASS_NAME, value="date")
    for element in date:
        date_list.append(element.text)

    img_list = []
    # thumb = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "thumb")))
    thumb = driver.find_elements(by=By.CLASS_NAME, value="thumb")

    for element in thumb:
        img = element.find_element(by=By.TAG_NAME, value="img")
        img_list.append(img.get_attribute("src"))

    return dict({'title': title_list, 'date': date_list, 'img': img_list})


def lg_dict():
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument("--disable-gpu")
    webdriver_options.add_argument('--disable-dev-shm-usage')
    webdriver_options.add_argument("--window-size=1920,1080")
    webdriver_options.add_argument("--disable-setuid-sandbox")
    webdriver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=webdriver_options)
    # driver = webdriver.Chrome(executable_path=r'/Users/10cm_mocha/Downloads/chromedriver', options=webdriver_options)
    driver.get('https://www.lguplus.com/benefit-event/ongoing')

    driver.implicitly_wait(10)

    membership_btn = driver.find_element(by=By.XPATH,
                                         value='//*[@id="contentsSection"]/div/div[2]/div/div/div[1]/div[1]/ul/li[4]/a')
    membership_btn.click()
    time.sleep(2)
    # event_list = driver.find_elements(by=By.XPATH, value='//*[@id="contentsSection"]/div/div[2]/div/div/div[1]/div[3]/ul')

    title_list = []
    # titles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tit")))
    titles = driver.find_elements(by=By.CLASS_NAME, value="tit")

    for title in titles:
        title_list.append(title.text)

    # print(title_list)

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

    img_list = []
    images = driver.find_elements(by=By.CLASS_NAME, value="img-area")

    for img in images:
        img = img.find_element(by=By.TAG_NAME, value="img")
        img_list.append(img.get_attribute("src"))

    # print(img_list)

    return dict({'title': title_list, 'date': date_list, 'img': img_list})


@app.route('/')
@sched.scheduled_job('interval', hours=24)
def setEventList():
    print("setEventList 진입")
    dbname = get_database()
    print("DB 연결 완료")

    skt = dbname['skt']
    kt = dbname['kt']
    lg = dbname['lg']

    print(skt_dict())
    print(kt_dict())
    print(lg_dict())

    print("db에 업데이트 중...")
    skt.update_one({'_id': ObjectId('633007e552ef499751ceb548')}, {"$set": skt_dict()})
    kt.update_one({'_id': ObjectId('6330017d0af9348ced24899f')}, {"$set": kt_dict()})
    lg.update_one({'_id': ObjectId('6336ea180ad3309313d9bfc3')}, {"$set": lg_dict()})
    print("업데이트 완료")

    return 'setEventList - Successful update event list'


if __name__ == "__main__":
    sched.start()
    app.run(host="0.0.0.0")
