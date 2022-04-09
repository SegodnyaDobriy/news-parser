from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import csv

chrome_options = Options()  # чтобы браузер не открывался
chrome_options.add_argument('--headless')  # чтобы браузер не открывался
browser = webdriver.Chrome('/Users/User/Desktop/chromedriver',
                           options=chrome_options)  # ТОЛЬКО OPTIONS чтобы браузер не открывался
URL = 'https://vivalacloud.ru/category/articles/'
FILE = 'Pod news500.csv'


def parse():
    browser.get(URL)
    sleep(5)
    scroll()
    browser.find_element(By.ID, "loadmore").click()
    sleep(3)
    x = 0
    while x != 501:
        scroll()
        print('Скроллю страницу:' + str(x))
        x += 1
    sleep(3)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    items = soup.find_all('article', class_='post-block')
    pods = []
    for item in items:
        if 'Pod' in item.find('h3', class_='heading').get_text(strip=True):  # проверка, Pod это или что-то другое
            pods.append({
                'title': item.find('h3', class_='heading').get_text(strip=True),
                'png': item.find('img').get('src'),
                'link': item.find('a', class_='picture').get('href')
            })

    save_file(pods, FILE)


def scroll():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
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
