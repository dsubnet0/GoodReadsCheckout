import requests

RAKUTEN_APPLICATION_ID = 1093196333123354205

def query_rakuten_by_isbn13(isbn13: str, verbose=False):
    url = f'https://app.rakuten.co.jp/services/api/Kobo/EbookSearch/20170404?applicationId={RAKUTEN_APPLICATION_ID}&itemNumber={isbn13}'
    if verbose: print(url)
    try:
        result = requests.get(url)
    except Exception as e:
        print(e)
    if not result:
        print('Some problem with Rakuten API request')
        return None
    return result

if __name__ == '__main__':
    print(query_rakuten_by_isbn13('9780593321218', True))