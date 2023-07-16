import requests
from typing import Dict, List
from urllib.parse import quote


class RakutenQuerier():

    def __init__(self, base_url: str, application_id: int):
        self.base_url = base_url
        self.application_id = application_id

    def query_by_isbn13(self, isbn13: str, verbose=False) -> Dict:
        url = f'{self.base_url}?applicationId={self.application_id}&itemNumber={isbn13}'
        return self._query_rakuten_api(url, verbose)

    def query_by_title(self, title: str, verbose=False) -> Dict:
        url = f'{self.base_url}?applicationId={self.application_id}&title={quote(title)}'
        return self._query_rakuten_api(url, verbose)

    def _query_rakuten_api(self, url: str, verbose=False) -> Dict:
        if verbose: print(url)
        result = None
        try:
            result = requests.get(url)
        except Exception as e:
            print(e)
        if not result:
            print('Some problem with Rakuten API request')
            return None
        return result.json()


    def format_results(self, results: Dict) -> List:
        '''
        Returns a list of neat result strings, ready to be printed
        '''
        titles_hit = 0
        if len(results) > 0 and len(results['Items']) > 0:
            titles_hit += 1
            for r in results['Items']:
                print(f'{r["Item"]["title"]} - {r["Item"]["itemUrl"]}')
        return titles_hit


if __name__ == '__main__':
    rakuten_application_id = 1093196333123354205
    rakuten_base_url = f'https://app.rakuten.co.jp/services/api/Kobo/EbookSearch/20170426'
    rq = RakutenQuerier(rakuten_base_url, rakuten_application_id)
    print(rq.query_by_isbn13('9780593320532', True))