import requests
import xmltodict

API_KEY = 'gslnNIUU1HVFZN4kQig'
API_SECRET = 'c2Q3V74CjGsaqcKzJ86ueTCf7Zzj1OIJ0kKGw4jf0'


def get_toread_titles(user_id):
    url = 'https://www.goodreads.com/review/list.xml?v=2&key={key}&id={id}&shelf=to-read'.format(key=API_KEY, id=user_id)
    try:
        r = requests.get(url)
    except e:
        print(e)
    if not r:
        print('Some problem with the request')
        return -1

    shelf_contents = xmltodict.parse(r.text)
    title_list = []
    for entry in shelf_contents['GoodreadsResponse']['reviews']['review']:
        entry_items = entry['book']
        print(entry_items['title'])
    return 0


USER_ID = '3696598'

if __name__ == '__main__':
    get_toread_titles(USER_ID)

#print(r.text)


#    for key,value in book['book'].items():
#        if key == 'title':
#            print('Title:',value)

