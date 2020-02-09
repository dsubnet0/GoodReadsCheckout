import requests
from lxml import html
from bs4 import BeautifulSoup
import dumper


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
        for subtable in table.find_all('table'):
            print('ITEM>'+str(subtable)+'\n')

#    tb = soup.find('table', id='result_table_table')
#    for t2 in tb.find_all('tr'):
#        print('ITEM>'+str(t2.find('td')))


    #tree = html.fromstring(page.content)
    #for table in tree.xpath('//table[@id="result_table_table"]'):
    #    header = [text(th) for th in table.xpath('//th')]
    #    data = []
    #    for tr in table.xpath('//tr'):
    #        for td in tr.xpath('td'):
    #            #print('BEGIN>'+text(td).strip()+'<END')
    #            data.append(text(td).strip())
    #    data = [row for row in data if len(row)==len(header)]
    #    data = pd.DataFrame(data,columns=header)
    #    print(data)

if __name__ == '__main__':
    print(query_southbury_library('wuthering heights'))