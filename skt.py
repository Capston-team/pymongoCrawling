import re

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import time
import json

# SKT 이벤트 날짜 크롤링
def skt_date():
    url_date = "https://sktmembership.tworld.co.kr/mps/pc-bff/program/tday.do"
    response = requests.get(url_date)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    date_events = soup.find_all('div', attrs={"data-move-scroll": "DISCOUNT_20221005_WEEK_BENEFIT"})

    for event in date_events:
        title = event.find_all(attrs={'class': 'benefit-date'})

        # event에서 텍스트를 읽어옴, 제목을 읽어오는 것
        # title = str(title.select('span'))
        title = str(title)
        title = re.sub('<.+?>', '', title, 0).strip()
        title = re.sub("\\[", '', title, 0)
        title = re.sub("]", '', title, 0)
        title = title.split(', ')

        remove_word = "week1 혜택"
        remove_word2 = "유의 사항"
        remove_word3 = "Day2 혜택"

        # 해당 word가 title 리스트에서 remove_word, remove_word2에 해당한다면 제거
        for word in title:
            if remove_word in word:
                title.remove(word)
            if remove_word2 in word:
                title.remove(word)

        # title 리스트에 해당 인덱스의 문자열에 remove_word, remove_word2가 있다면 제거, 공백 제거 후 반환
        for i, word in enumerate(title):
            if remove_word in word:
                title[i] = word.strip(remove_word)
            if remove_word2 in word:
                title[i] = word.strip(remove_word2)

        return title


# SKT 이벤트 제목, 상세설명 크롤링
def skt_title():
    url = "https://sktmembership.tworld.co.kr/mps/pc-bff/program/tday.do"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    date_events = soup.find_all('div', attrs={"data-move-scroll": "DISCOUNT_20221005_WEEK_BENEFIT"})

    # 'p'태그를 가지고 class명이 title인 element를 모두 가져와 events에 저장함

    for event in date_events:
        description = str(event.select('.tday-info > .tit'))
        description = re.sub('<.+?>', '', description, 0).strip()
        description = re.sub("\\[", '', description, 0)
        description = re.sub("]", '', description, 0)
        description = description.split(', ')

        return description

    # # events에 저장된 element를 하나씩 뽑아내 출력함
    # for event in events:
    #     # event에서 텍스트를 읽어옴, 제목을 읽어오는 것
    #     title = event.get_text()
    #
    #     print(title)


def skt_image():
    context = ssl._create_unverified_context()
    result = urlopen("https://sktmembership.tworld.co.kr/mps/pc-bff/program/tday.do", context=context)
    soup = BeautifulSoup(result.read(), "html.parser")

    date_events = soup.find_all('div', attrs={"data-move-scroll": "DISCOUNT_20221005_WEEK_BENEFIT"})

    img_link = []

    for event in date_events:
        img = event.select('.img-box > img')

        for i in img:
            img_link.append(i['src'])

    return img_link





