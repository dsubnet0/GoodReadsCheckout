from typing import Dict, List
from urllib.parse import quote

import requests


class RakutenQuerier():

    def __init__(self, base_url: str, application_id: int, verbose: bool = False):
        self.base_url = base_url
        self.application_id = application_id
        self.verbose = verbose

    def get_book(self, title: str, isbn13: str) -> str:
        isbn_result = self.query_by_isbn13(isbn13)
        result_string = ''
        if len(isbn_result) > 0:
            result_string += f'\n\n{isbn13}:'
            for r in isbn_result:
                result_string += '\n'+'|'.join(r.values())
        else:
            title_result = self.query_by_title(title)
            if len(title_result) > 0:
                result_string += f'\n\n{title} ({format}):'
                for r in title_result:
                    result_string += '\n'+'|'.join(r.values())
        return result_string

    def query_by_isbn13(self, isbn13: str) -> Dict:
        '''
        returns a dicts something like {title: '', url: ''}
        '''
        if self.verbose:
            print(f'Querying for {isbn13}')
        url = f'{self.base_url}?applicationId={self.application_id}&itemNumber={isbn13}'
        return self._query_rakuten_api(url)

    def query_by_title(self, title: str) -> Dict:
        if self.verbose:
            print(f'Querying for {title}')
        url = f'{self.base_url}?applicationId={self.application_id}&title={quote(title)}'
        return self._query_rakuten_api(url)

    def _query_rakuten_api(self, url: str) -> Dict:
        if self.verbose: print(url)
        result = None
        try:
            result = requests.get(url)
        except Exception as e:
            print(e)
        if not result:
            print('Some problem with Rakuten API request')
            return None
        return result.json()


    def format_results(self, results: Dict, limit: int = 1) -> List:
        '''
        Returns a list of neat result strings, ready to be printed
        '''
        result_string_list = []
        result_count = 0
        if len(results) > 0 and len(results['Items']) > 0:
            for r in results['Items']:
                if result_count >= limit: break
                result_string_list.append(f'{r["Item"]["title"]} - {r["Item"]["itemUrl"]}')
                result_count += 1
        return result_string_list


if __name__ == '__main__':
    rakuten_application_id = 1093196333123354205
    rakuten_base_url = f'https://app.rakuten.co.jp/services/api/Kobo/EbookSearch/20170426'
    rq = RakutenQuerier(rakuten_base_url, rakuten_application_id)
    print(rq.query_by_isbn13('9780593320532', True))