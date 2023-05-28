import requests
from bs4 import BeautifulSoup

class GoodReads():

    def __init__(self, user_string: str, verbose: bool = None):
        self.user_string = user_string
        self.verbose = verbose
        self._toread_list = None

    @property
    def toread_list(self):
        """
        An array of (title,isbn,isbn13) dicts
        """
        if self._toread_list:
            return self._toread_list
        # else

        page_number = 1
        records = []
        records_in_page = 99
        while records_in_page > 0:
            records_in_page = 0
            if self.verbose: print(f'Fetching page {page_number}')
            url = self._get_url(page_number=page_number)
            if self.verbose: print(url)
            try:
                page = requests.get(url)
            except Exception as e:
                print(e)
            if not page:
                print('Some problem with the GR request')
                return records
            
            parsed_results = self._parse_fields_from_results(page)
            if parsed_results:
                records.extend(parsed_results)
                records_in_page += len(parsed_results)
            if self.verbose: print(f'{len(records)} found so far')
            page_number += 1
        self._toread_list = records
        return self._toread_list


    def _parse_fields_from_results(self, page):
        page_results = []
        soup = BeautifulSoup(page.content, 'html.parser')
        for table in soup.find_all('table', id='books'):
            for row in table.find_all('tr'):
                title = None
                isbn = None
                isbn13 = None
                for data in row.find_all('td'):
                    td_class = ' '.join(data.get('class'))
                    if td_class == 'field title' or td_class == 'field isbn' or td_class == 'field isbn13':
                        for value in data.find_all('div', attrs={'class':'value'}):
                            if td_class == 'field title':
                                title = value.get_text().strip()
                                break
                            if td_class == 'field isbn':
                                isbn = value.get_text().strip()
                                break
                            if td_class == 'field isbn13':
                                isbn13 = value.get_text().strip()
                                break
                if title and (isbn or isbn13):
                    page_results.append({'title': title, 'isbn': isbn, 'isbn13': isbn13})
        return page_results


    def _get_url(self, page_number=None):
        if page_number:
            page_number_clause = f'page={page_number}&'
        else:
            page_number_clause = ''
        return f'https://www.goodreads.com/review/list/{self.user_string}?{page_number_clause}ref=nav_mybooks&shelf=to-read&per_page=50'