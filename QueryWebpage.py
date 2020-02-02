import requests
from lxml import html
import pandas


def text(elt):
    return elt.text_content().replace(u'\xa0',u' ')


def query_southbury_library(title):
    url = 'https://southbury.biblio.org/eg/opac/results?query={}&qtype=title&fi%3Asearch_format=book&locg=89&detail_record_view=0&sort=popularity'.format(title)
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    if not page:
        print('Some problem with the library request')
        return -1
#    print(page.text)
    #search_results = xmltodict.parse(r.text)
    #print(search_results)
    tree = html.fromstring(page.content)
    #div class="result_table_title_cell"
    for table in tree.xpath('//table[@id="result_table_table"]'):
#        header = [text(th) for th in table.xpath('//th')]  # 1
#        data = [[text(td) for td in tr.xpath('td')]
#                for tr in table.xpath('//tr')]  # 2
#        data = [row for row in data if len(row) == len(header)]  # 3
#        data = pandas.DataFrame(data, columns=header)  # 4
#        print(data)
        for tr in table.xpath('//tr'):
            for td in tr.xpath('td'):
                print(text(td))

if __name__ == '__main__':
    print(query_southbury_library('wuthering heights'))