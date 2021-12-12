# from bs4 import BeautifulSoup
from datetime import date
import requests
import time
from random import randint
import datetime


class EditDate:
    @staticmethod
    def edit_date(date_time):
        month = {"января": '.01.', "февраля": '.02.', "марта": '.03.',
                 "апреля": '.04.', "майя": '.05.', "июня": '.06.',
                 "июля": '.07.', "августа": '.08.', "сентября": '.09.',
                 "октября": '.10.', "ноября": '.11.', "декабря": '.12.'}
        for key in month:
            if key in date_time:
                return date_time[:2] + month[key] + str(date.today().year) + ' ' + date_time.rstrip()[-5:]


class Neftegaz:
    def __init__(self):
        self.url = 'https://neftegaz.ru/news/'

    @staticmethod
    def get_lst(data):
        soup = BeautifulSoup(data, 'lxml')
        all_news = soup.find('div', class_='js-ajax-content').find_all('div', class_='news_week__item')
        lst = []
        for news in all_news:
            # date_time = news.find('div', class_='date').text
            date_time = EditDate.edit_date(news.find('div', class_='date').text)
            # category = news.find('div', class_='category_link').text.replace('\n', '')
            title = news.find('div', class_='title').text
            url = news.find('div', class_='title').find('a').get('href')
        lst.append([date_time, 'neftegaz.ru', title, url])
        return lst


class Angi:
    def __init__(self):
        self.url = 'https://www.angi.ru/section/90886-%D0%9D%D0%B5%D1%84%D1%82%D1%8C%20%D0%B8%20%D0%B3%D0%B0%D0%B7/'

    @staticmethod
    def get_lst(data):
        soup = BeautifulSoup(data, 'lxml')
        all_news = soup.find_all('div', ['newslink', 'newslink primary'])
        lst = []
        for news in all_news:
            # date_time = news.find('div', class_='date').text
            date_time = EditDate.edit_date(news.find('div', class_='date').text)
            url = 'https://www.angi.ru/' + news.find('a').get('href')
            title = news.find('a').text
            # news_text = news.find('div', class_='newstext').text
            lst.append([date_time, 'angi.ru', title, url])
        return lst


class Guardinfo:
    @staticmethod
    def get_lst():
        print('Парсим Guardinfo...')
        lst = []
        lst_url = ['https://guardinfo.online/',
                   'https://guardinfo.online/page/2/',
                   'https://guardinfo.online/page/3/']
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_id = soup.find_all('article')
                for id_ in all_id:
                    date_time = id_.find('time').text
                    url = id_.find('h2', class_='entry-title').find('a').get('href')
                    title = id_.find('h2', class_='entry-title').find('a').text
                    lst.append([date_time, 'guardinfo.online', title, url])
            except ConnectionError:
                print(f'guardinfo.online: Соединение разорвано')
            time.sleep(randint(5, 10))
        return lst


class Ria:
    @staticmethod
    def get_lst():
        print('Парсим Ria...')
        url = 'https://ria.ru/incidents/'
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        count = 0
        lst = []
        switch = 0
        while count <= 100:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_item = soup.find_all('div', class_='list-item')
                for item in all_item:
                    time_ = item.find('div', class_='list-item__date').text
                    if 'Вчера,' in time_:
                        yesterday = datetime.date.today()- datetime.timedelta(1)
                        time_ = f"{yesterday.strftime('%d.%m.%Y')} {time_}".replace('Вчера, ', '')
                    else:
                        time_ = f"{str(datetime.date.today().strftime('%d.%m.%Y'))} {time_}"
                    title = item.find('a', class_='list-item__title color-font-hover-only').text.strip()
                    url_item = item.find('a', class_='list-item__title color-font-hover-only').get('href')
                    lst.append([time_, 'ria.ru', title, url_item])
                    count += 1
            except ConnectionError:
                print(f'Ria.ru: Соединение разорвано')

            try:  # get url next page
                if switch == 0:
                    url_next_page = soup.find('div', class_='list-more').get('data-url')
                    switch = 1
                else:
                    url_next_page = soup.find('div', class_='list-items-loaded').get('data-next-url')
            except AttributeError as e:
                print(e)
                break
            url = 'https://ria.ru/incidents/' + url_next_page[20:]

            time.sleep(randint(5, 10))
        return lst


class Sarnovosti:
    @staticmethod
    def get_lst():
        print('Парсим Sarnovosti...')
        lst_url = ['https://sarnovosti.ru/news/',
                   'https://sarnovosti.ru/news/?PAGEN_1=2',
                   'https://sarnovosti.ru/news/?PAGEN_1=3',
                   'https://sarnovosti.ru/news/?PAGEN_1=4',
                   'https://sarnovosti.ru/news/?PAGEN_1=5']
        lst = []
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_news = soup.find_all('div', class_='news-block item--animated isInView')

                for news in all_news:
                    time_ = news.find('time').text
                    if len(time_) == 5:
                        date_time = f"{datetime.date.today().strftime('%d.%m.%Y')} {time_}"
                    else:
                        month = {"января": '.01.', "февраля": '.02.', "марта": '.03.',
                                 "апреля": '.04.', "майя": '.05.', "июня": '.06.',
                                 "июля": '.07.', "августа": '.08.', "сентября": '.09.',
                                 "октября": '.10.', "ноября": '.11.', "декабря": '.12.'}
                        for key in month:
                            if key in time_[6:]:
                                dt = datetime.datetime.strptime(
                                    f'{time_[6:9].strip()}{month[key]}{datetime.date.today().year}',
                                    '%d.%m.%Y').date().strftime('%d.%m.%Y')
                        date_time = f'{dt} {time_[:5]}'
                    title = news.find('a', class_='news-block__title').text.strip()
                    url = f"{'https://sarnovosti.ru'}{news.find('a', class_='news-block__title').get('href')}"
                    lst.append([date_time, 'sarnovosti.ru', title, url])
            except ConnectionError:
                print(f'Sarnovosti: Соединение разорвано')
            time.sleep(randint(5, 10))
        return lst


class Ufa1:
    @staticmethod
    def get_lst():
        print('Парсим Ufa1...')
        lst_url = ['https://ufa1.ru/text/',
                   'https://ufa1.ru/text/?page=2',
                   'https://ufa1.ru/text/?page=3']
        lst = []
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_article = soup.find_all('article')

                for article in all_article:
                    date_time = article.find('time').get('datetime')
                    date_time = f"{datetime.datetime.strptime(date_time[:10], '%Y-%m-%d').date().strftime('%d.%m.%Y')} {date_time[11:]}"
                    # print(date_time)
                    title = article.find('h2', class_='G1ez').find('a').text
                    # print(title)
                    url = f"https://ufa1.ru{article.find('h2', class_='G1ez').find('a').get('href')}"
                    # print(url)
                    lst.append([date_time, 'ufa1', title, url])

            except ConnectionError:
                print(f'Ufa1: Соединение разорвано')
            time.sleep(randint(5, 10))
        return lst


class Tatar_inform:
    @staticmethod
    def get_lst():
        print('Парсим Tatar_inform...')
        lst_url = ['https://www.tatar-inform.ru/news',
                   'https://www.tatar-inform.ru/news?page=2',
                   'https://www.tatar-inform.ru/news?page=3',
                   'https://www.tatar-inform.ru/news?page=4',
                   'https://www.tatar-inform.ru/news?page=5']
        lst = []
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_li = soup.find_all('li', class_='underline-list__item')
                for li in all_li:
                    time_ = li.find('div', class_='list-item__date').text.strip().split()
                    # print(time_)
                    month = {"января": '.01.', "февраля": '.02.', "марта": '.03.',
                             "апреля": '.04.', "майя": '.05.', "июня": '.06.',
                             "июля": '.07.', "августа": '.08.', "сентября": '.09.',
                             "октября": '.10.', "ноября": '.11.', "декабря": '.12.'}
                    for key in month:
                        if key in time_[1]:
                            date_time = f"{datetime.datetime.strptime(f'{time_[0]}{month[key]}{time_[2]}', '%d.%m.%Y').date().strftime('%d.%m.%Y')} {time_[3]}"
                            # print(date_time)
                    title = li.find('div', class_='list-item__content').find('a').text.strip()
                    url = li.find('div', class_='list-item__content').find('a').get('href')
                    # print(url)
                    lst.append([date_time, 'Tatar_inform', title, url])

            except ConnectionError:
                print(f'Tatar_inform: Соединение разорвано')
            time.sleep(randint(5, 10))
        return lst


class Fourvsar:
    @staticmethod
    def get_lst():
        print('Парсим 4vsar...')
        url = 'https://www.4vsar.ru/news'
        lst = []
        count = 0
        while count < 2:
            try:
                head = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                'Host': 'www.4vsar.ru',
                'sec-ch-ua-platform': "Windows",
                "Connection": 'keep-alive'}

                data = requests.get(url, headers=head).text
                with open('4vsar.html', 'w', encoding='windows-1251', errors='ignore') as f:
                    f.write(data)
                with open('4vsar.html', encoding='windows-1251') as f:
                    data = f.read()

                soup = BeautifulSoup(data, 'lxml')
                all_tr = soup.find('table', class_='lenta').find_all('tr')


                date_ = soup.find('div', class_='wide').find('h1').text[14:]
                print(f'date_{date_}')
                month = {"января": '.01.', "февраля": '.02.', "марта": '.03.',
                         "апреля": '.04.', "майя": '.05.', "июня": '.06.',
                         "июля": '.07.', "августа": '.08.', "сентября": '.09.',
                         "октября": '.10.', "ноября": '.11.', "декабря": '.12.'}
                # print(date_)
                for key in month:
                    if key in date_:
                        date_ = datetime.datetime.strptime(f'{date_[:2].strip()}{month[key]}{date_[-4:]}', '%d.%m.%Y').date().strftime('%d.%m.%Y')
                print(f'дата после обработки {date_}')

                for tr in all_tr:
                    date_time = f"{date_} {tr.find('div', class_='date').text}"
                    # print(date_time)
                    title = tr.find('a').find('h2').text
                    # print(title)
                    url = f"https://www.4vsar.ru{tr.find('a').get('href')}"
                    # print(url)
                    lst.append([date_time, '4vsar', title, url])
                print(lst)

                url = 'https://www.4vsar.ru/archive/' + str((datetime.datetime.strptime(date_, '%d.%m.%Y') - datetime.timedelta(1)).date().strftime('%Y.%m.%d')).replace('.', '/')
                print(f'next page {url}')
                count += 1
            except ConnectionError:
                print(f'4vsar: Соединение разорвано')
            time.sleep(randint(5, 10))
        return lst


class Ria56:
    @staticmethod
    def get_lst():
        print('Парсим ria56...')
        lst_url = ['https://ria56.ru/novosti',
                   'https://ria56.ru/novosti/page/2',
                   'https://ria56.ru/novosti/page/3']
        # lst_url = ['https://ria56.ru/novosti']
        lst = []
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_article = soup .find_all('article')
                for article in all_article:
                    dt = article.find('span', class_='entry-date').find('a').find('time').get('datetime')
                    date_time = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')
                    # print(date_time)
                    title = article.find('h2', class_='entry-title').find('a').text
                    # print(title)
                    url = article.find('h2', class_='entry-title').find('a').get('href')
                    # print(url)
                    lst.append([date_time, 'ria56', title, url])

            except ConnectionError:
                print(f'ria56: Соединение разорвано')
            # print(lst)
            time.sleep(randint(5, 10))
        return lst


class Ch74:
    @staticmethod
    def get_lst():
        print('Парсим 74.ru...')
        lst_url = ['https://74.ru/text/',
                   'https://74.ru/text/?page=2']
        lst = []
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_article = soup.find_all('article', class_='G1ahf')
                for article in all_article:
                    dt = article.find('time').get('datetime')
                    date_time = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')
                    # print(date_time)
                    title = article.find('h2', class_='G1ez').find('a').text
                    url = 'https://74.ru' + article.find('h2', class_='G1ez').find('a').get('href')
                    # print(title)
                    # print(url)
                    lst.append([date_time, '74.ru', title, url])

            except ConnectionError:
                print(f'74.ru: Соединение разорвано')
            # print(lst)
            time.sleep(randint(5, 10))
        return lst


class Kurgan45:
    @staticmethod
    def get_lst():
        print('Парсим 45.ru...')
        lst_url = ['https://45.ru/text/',
                   'https://45.ru/text/?page=2']
        lst = []
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        for url in lst_url:
            try:
                data = requests.get(url, headers=head).text

                soup = BeautifulSoup(data, 'lxml')
                all_article = soup.find_all('article', class_='G1ahf')
                for article in all_article:
                    dt = article.find('time').get('datetime')
                    date_time = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')
                    # print(date_time)
                    title = article.find('h2', class_='G1ez').find('a').text
                    url = 'https://45.ru' + article.find('h2', class_='G1ez').find('a').get('href')
                    # print(title)
                    # print(url)
                    lst.append([date_time, '45.ru', title, url])

            except ConnectionError:
                print(f'45.ru: Соединение разорвано')
            # print(lst)
            time.sleep(randint(5, 10))
        return lst



# if __name__ == '__main__':

    # head = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    # url = 'https://ria56.ru/novosti'
    # data = requests.get(url).text
    # # print(data)
    # with open('ria56.html', 'w', encoding='windows-1251', errors='ignore') as f:
    #     f.write(data)
    # with open('ria56.html', encoding='windows-1251') as f:
    #     data = f.read()
    # print(data)

    # g = Kurgan45()
    # g.get_lst()


    # print(lst)
    # r = Ria()
    # print(r.__class__.__name__ == 'Ria')

    # print(lst)
    # print(Fourvsar.get_lst())

    # t1 = '08:55, 2 декабря'
    # t2 = '15:28, 30 ноября'
    # month = {"января": '.01.', "февраля": '.02.', "марта": '.03.',
    #          "апреля": '.04.', "майя": '.05.', "июня": '.06.',
    #          "июля": '.07.', "августа": '.08.', "сентября": '.09.',
    #          "октября": '.10.', "ноября": '.11.', "декабря": '.12.'}
    # for key in month:
    #     if key in t1[6:]:
    #         dt = datetime.datetime.strptime(f'{t1[6:9].strip()}{month[key]}{datetime.date.today().year}', '%d.%m.%Y').date().strftime('%d.%m.%Y')
    # t = '2021-12-03T14:20:28+05:00'
    # print(f"{datetime.datetime.strptime(t[:10], '%Y-%m-%d').date().strftime('%d.%m.%Y')} {t[11:]}")
    # print(datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M'))
    # t = '2021-12-01T15:42:00'
    # print(datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M'))