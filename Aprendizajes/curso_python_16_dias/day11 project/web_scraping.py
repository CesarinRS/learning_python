from bs4 import BeautifulSoup
import requests

result = requests.get('https://fede-garay.vercel.app/')
sopa = BeautifulSoup(result.text, 'lxml')

for label in sopa.select('videos a'):
    print(label['href'])

image = sopa.select('img')[0]

image_url = 'https://fede-garay.vercel.app/' + image['src']

image_answer = requests.get(image_url).content

download_pic = open('test.png', 'wb')
download_pic.write(image_answer)
download_pic.close()