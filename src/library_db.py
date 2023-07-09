from typing import List

import requests
from bs4 import BeautifulSoup

BASE_URL =  url = f'https://southbury.biblio.org/eg/opac/results?query='


class LibraryDB():

    def __init__(self, base_url=None, verbose=False):
        if base_url:
            self._base_url = base_url
        else:
            self._base_url = BASE_URL
        self.verbose = verbose

    @property
    def base_url(self):
        return self._base_url


    def get_book(self, title: str, isbn: str, format: str) -> str:
        isbn_result = self._query_library_by_isbn(isbn, format)
        result_string = ''
        if len(isbn_result) > 0:
            result_string += f'\n\n{isbn} ({format}):'
            for r in isbn_result:
                result_string += '\n'+'|'.join(r.values())
        else:
            title_result = self._query_library_by_title(title, format)
            if len(title_result) > 0:
                result_string += f'\n\n{title} ({format}):'
                for r in title_result:
                    result_string += '\n'+'|'.join(r.values())
        return result_string


    def _query_library_by_isbn(self, isbn: str, format: str):
        url = self._get_search_url_isbn(isbn=isbn, format=format)
        return self._query_library(url)


    def _query_library_by_title(self, title: str, format: str):
        url = self._get_search_url_title(title=title, format=format)
        return self._query_library(url)

    def _query_library(self, url):
        if self.verbose: print(url)
        try:
            page = requests.get(url)
        except Exception as e:
            print(e)
        if not page:
            print('Some problem with library request')
            return None
        return self._parse_library_results(page)


    def _get_search_url_isbn(self, isbn: str, format: str) -> str:
        return f'{self.base_url}identifier%7Cisbn%3A{isbn}&qtype=keyword&fi%3Asearch_format={format}&locg=89&detail_record_view=0&_adv=1&page=0&_special=1'

    def _get_search_url_title(self, title: str, format: str) -> str:
        return f'{self.base_url}"{title}"&qtype=title&fi%3Asearch_format={format}&locg=89&detail_record_view=0&_adv=1&page=0&_special=1'


    def _parse_library_results(self, page) -> List:
        '''
        Returns list of {title, availability, call_number} objects
        '''
        soup = BeautifulSoup(page.content, 'html.parser')
        records = []
        for table in soup.find_all('div', id='result_table_div'):
            for results in table.find_all('div', id='result_block'):
                for title in results.find_all('a', attrs={'class': 'record_title search_link'}):
                    title_text = title.get_text().strip()
                for row in results.find_all('div', attrs={'class': 'result_count'}):
                    availability = row.get_text().strip()
                    if 'Southbury' in availability:
                        for call_number in results.find_all('div', attrs={'class': 'result_call_number'}):
                            call_number_text = call_number.get_text().strip()
                            records.append({'title': title_text, 'availability': availability, 'call_number': call_number_text})
        return records