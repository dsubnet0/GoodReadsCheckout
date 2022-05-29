from tkinter import W
import requests
from bs4 import BeautifulSoup
import pprint
import logging

PP = pprint.PrettyPrinter(indent=4)


def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

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

def query_southbury_library(query, format='book'):
    query = query.replace(' ', '+')
    url = f'https://southbury.biblio.org/eg/opac/results?query={query}&qtype=title&fi%3Asearch_format={format}'
    print(url)
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
#    for table in soup.find_all('table', id='result_table_table'):
#        for t in table.find_all(attrs={'class':'record_title search_link'}):
#            titles.append(t.get('title').replace('Display record details for ',''))
#        for subtable in table.find_all(attrs={'class':'result_holdings_table'}):
#            for row in subtable.find_all('tr'):
#                record = []
#                for subrow in row.find_all('td'):
#                    record.append(subrow.string)
#                if len(record)>0:
#                    records.append(record)
    for table in soup.find_all('div', id='result_table_div'):
        for results in table.find_all('div', id='result_block'):
            print(results)
            for row in results.find_all('div', attrs={'class': 'row'}):
                print(row)
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
    #print(get_goodreads_list(user_string='3696598-doug', verbose=True))
    print(query_southbury_library_by_isbn(isbn='0345480619', format='book'))