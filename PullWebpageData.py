import requests
import xmltodict

API_KEY = 'gslnNIUU1HVFZN4kQig'
API_SECRET = 'c2Q3V74CjGsaqcKzJ86ueTCf7Zzj1OIJ0kKGw4jf0'
def get_toread_titles():
    pass


USER_ID = '3696598'
#url = 'https://www.goodreads.com/review/list/3696598-doug?shelf=to-read'
url = 'https://www.goodreads.com/review/list.xml?v=2&key={key}&id={id}&shelf=to-read'.format(key=api_key,id=user_id)
try:
    r = requests.get(url)
except e:
    print(e)

if r:
    print('Successful request')
else:
    print('Some problem with the request')

#print(r.text)

shelf_contents = xmltodict.parse(r.text)

for book in shelf_contents['GoodreadsResponse']['reviews']['review']:
    for key,value in book['book'].items():
        if key == 'title':
            print('Title:',value)

