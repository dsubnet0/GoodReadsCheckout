import requests
import xmltodict

API_KEY = 'gslnNIUU1HVFZN4kQig'
API_SECRET = 'c2Q3V74CjGsaqcKzJ86ueTCf7Zzj1OIJ0kKGw4jf0'


def get_toread_titles(user_id, page=1):
    url = 'https://www.goodreads.com/review/list.xml?v=2&key={key}&id={id}' \
          '&shelf=to-read&sort=avg_rating&order=d&page={page}'.\
            format(key=API_KEY, id=user_id, page=page)
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
        title_list.append(entry_items['title'])
    return title_list


USER_ID = '3696598'

if __name__ == '__main__':
    for t in get_toread_titles(USER_ID):
        print(t)


