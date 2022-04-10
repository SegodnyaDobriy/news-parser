from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import csv

chrome_options = Options()  # чтобы браузер не открывался
chrome_options.add_argument('--headless')  # чтобы браузер не открывался
browser = webdriver.Chrome('/Users/User/Desktop/chromedriver', options=chrome_options)  # ТОЛЬКО OPTIONS чтобы браузер не открывался
URL = 'https://vivalacloud.ru/category/articles/'
FILE = 'Pod news500.csv'


def parse():
    browser.get(URL)
    sleep(5)  # жду прогрузки страницы
    scroll()  # скроллю, чтобы увидеть кнопку "Еще посты"
    browser.find_element(By.ID, "loadmore").click()  # нажимаю на кнопку "Еще посты"
    sleep(3)  # жду прогрузки новостей

    for pages in range(1, 501):  # 500  - оптимальное количество страниц
        scroll()
        print('Скроллю страницу:' + str(pages))

    sleep(3)  # жду подргузки последней страницы
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    items = soup.find_all('article', class_='post-block')
    pods = []
    for item in items:
        if 'Pod' in item.find('h3', class_='heading').get_text(strip=True):  # проверка, есть ли "Pod" в названии новости
            pods.append({
                'title': item.find('h3', class_='heading').get_text(strip=True),  # заголовок новости
                'png': item.find('img').get('src'),                               # картинка Pod'а
                'link': item.find('a', class_='picture').get('href')              # ссылка на новость
            })

    save_file(pods, FILE)


def scroll():
    SCROLL_PAUSE_TIME = 0.5

    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(SCROLL_PAUSE_TIME)

        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def save_file(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Шапка', 'Картинка', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['png'], item['link']])


parse()

# это мой первый кринге
