import requests

from bs4 import BeautifulSoup
word = input()

pars = BeautifulSoup(requests.get(input()).content, 'html.parser').find_all('p')
for i in pars:
    if word in i.text:
        print(i.text)
        break
