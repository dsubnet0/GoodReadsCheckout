import requests
from bs4 import BeautifulSoup
import pprint
import logging

PP = pprint.PrettyPrinter(indent=4)


def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')


def query_southbury_library(query, format='book'):
    url = f'https://southbury.biblio.org/eg/opac/results?query={query}&qtype=keyword&fi%3Asearch_format={format}&locg=89&detail_record_view=0&sort=popularity'
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    if not page:
        print('Some problem with the library request')
        return -1

    soup = BeautifulSoup(page.content, 'html.parser')
    records = []
    titles = []
    for table in soup.find_all('table', id='result_table_table'):
        for t in table.find_all(attrs={'class':'record_title search_link'}):
            titles.append(t.get('title').replace('Display record details for ',''))
        for subtable in table.find_all(attrs={'class':'result_holdings_table'}):
            for row in subtable.find_all('tr'):
                record = []
                for subrow in row.find_all('td'):
                    record.append(subrow.string)
                if len(record)>0:
                    records.append(record)
    for i in range(0, len(titles)):
        if 0<=i<len(records):
            records[i].insert(0, titles[i])
    return records

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
                if title and isbn:
                    records.append({'title': title, 'isbn': isbn})
                    records_in_page += 1
        if verbose: print(f'{len(records)} found so far')
        page_number += 1
    print(f'{len(records)} titles found')
    return records



if __name__ == '__main__':
    #for r in query_southbury_library('fear and loathing'):
    #    print('|'.join(r))
    print(get_goodreads_list(user_string='3696598-doug', verbose=True))