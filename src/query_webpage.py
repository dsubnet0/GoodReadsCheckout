import requests
from bs4 import BeautifulSoup


def _parse_library_results(page):
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


def query_southbury_library_by_isbn(isbn, format='book', verbose=False):
    url = f'https://southbury.biblio.org/eg/opac/results?query=identifier%7Cisbn%3A{isbn}&qtype=keyword&fi%3Asearch_format={format}&locg=89&detail_record_view=0&_adv=1&page=0&_special=1'
    if verbose: print(url)
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    if not page:
        print('Some problem with library request')
        return None
    return _parse_library_results(page)


def get_goodreads_list(user_string: str, verbose: bool = False): 
    """"  
    Returns an array of (title,isbn) dicts
    """
    print('Compiling titles and ISBNs from Goodreads...')
    page_number = 1
    records = []
    records_in_page = 99
    while records_in_page > 0:
        records_in_page = 0
        if verbose: print(f'Fetching page {page_number}')
        url = f'https://www.goodreads.com/review/list/{user_string}?page={page_number}&ref=nav_mybooks&shelf=to-read&per_page=50'
        if verbose: print(url)
        try:
            page = requests.get(url)
        except Exception as e:
            print(e)
        if not page:
            print('Some problem with the Goodreads request')
            return records
        
        soup = BeautifulSoup(page.content, 'html.parser')
        for table in soup.find_all('table', id='books'):
            for row in table.find_all('tr'):
                title = ''
                isbn = ''
                for data in row.find_all('td'):
                    td_class = ' '.join(data.get('class'))
                    if td_class == 'field title' or td_class == 'field isbn':
                        for value in data.find_all('div', attrs={'class':'value'}):
                            if td_class == 'field title':
                                title = value.get_text().strip()
                                break
                            if td_class == 'field isbn':
                                isbn = value.get_text().strip()
                                break
                            if td_class == 'field isbn13':
                                isbn13 = value.get_text().strip()
                if title and isbn and isbn13:
                    records.append({'title': title, 'isbn': isbn, 'isbn13': isbn13})
                    records_in_page += 1
        if verbose: print(f'{len(records)} found so far')
        page_number += 1
    print(f'{len(records)} titles found')
    return records


if __name__ == '__main__':
    #for r in query_southbury_library('fear and loathing'):
    #    print('|'.join(r))
    #print(get_goodreads_list(user_string='3696598-doug', verbose=True))
    print(query_southbury_library_by_isbn(isbn='0345480619', format='book'))