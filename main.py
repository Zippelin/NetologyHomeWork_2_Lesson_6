import requests
from bs4 import BeautifulSoup
import re

KEYWORDS = ['embedded', 'Лаборатории Касперского']


class HabrNewsFinder:
    URL = 'https://habr.com/ru/all/'

    TIME_CLASS = 'post__time'
    HEADER_CLASS = 'post__title_link'
    TEXT_CLASS = 'post__text'

    def get_news(self, kwords, deeps_search=False):
        articles = self._get_page_data()
        print('Wait for news loading.')
        all_news = []
        for i, article in enumerate(articles):
            print('', end=f'\rLoading News: {i + 1}/{len(articles)} {"."* (i + 1)}')
            result = self._check_article_contain_kwords(article, kwords, deeps_search)
            if result:
                all_news.append(result)
        print('\nDONE!!!')
        for element in all_news:
            print(f'{element["time"]} - {element["title"]} - {element["url"]}')

    def _get_page_data(self, request_url=None) -> BeautifulSoup:
        url = request_url or self.URL
        result = requests.get(url)
        result.raise_for_status()
        soup = BeautifulSoup(result.text, 'html.parser')
        if request_url:
            page_data = soup.find(class_=self.TEXT_CLASS)
        else:
            page_data = soup.find_all('article')
        return page_data

    def _check_words_in_text(self, text: str, words: list) -> bool:
        for word in words:
            if re.compile(r'\b{0}\b'.format(word), flags=re.IGNORECASE).search(text):
                return True
        return False

    def _check_article_contain_kwords(self, article: BeautifulSoup, kwords: list, deeps_search) -> dict:
        if self._check_words_in_text(article.find(class_=self.TEXT_CLASS).text, kwords):
            return {
                'title': article.find(class_=self.HEADER_CLASS).text.strip(),
                'url': article.find(class_=self.HEADER_CLASS).attrs.get('href'),
                'time': article.find(class_=self.TIME_CLASS).text.strip()
            }
        else:
            if deeps_search:
                full_page_text = self._get_page_data(article.find(class_=self.HEADER_CLASS).attrs.get('href'))
                if self._check_words_in_text(full_page_text.text, kwords):
                    return {
                        'title': article.find(class_=self.HEADER_CLASS).text.strip(),
                        'url': article.find(class_=self.HEADER_CLASS).attrs.get('href'),
                        'time': article.find(class_=self.TIME_CLASS).text.strip()
                    }
            return {}


if __name__ == '__main__':
    aa = HabrNewsFinder()
    aa.get_news(KEYWORDS, deeps_search=True)
