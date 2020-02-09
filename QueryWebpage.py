import requests
from lxml import html
from bs4 import BeautifulSoup
import pprint

PP = pprint.PrettyPrinter(indent=4)


def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')


def query_southbury_library(title):
    url = 'https://southbury.biblio.org/eg/opac/results?query={}&qtype=title&fi%3Asearch_format=book&locg=89&detail_record_view=0&sort=popularity'.format(title)
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    if not page:
        print('Some problem with the library request')
        return -1

    soup = BeautifulSoup(page.content, 'html.parser')
    for table in soup.find_all('table', id='result_table_table'):
        for subtable in table.find_all(attrs={'class':'result_holdings_table'}):
            for row in subtable.find_all('tr'):
                record = []
                for subrow in row.find_all('td'):
                    record.append(subrow.string)
                print(' '.join(record))


if __name__ == '__main__':
    print(query_southbury_library('fear and loathing'))