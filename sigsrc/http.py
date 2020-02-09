import requests
from bs4 import BeautifulSoup
import re
import socket

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.google.com/'
}

def data(attr):
    try:
        attr['params']
    except KeyError:
        params = {}
    else:
        params = attr['params']

    if attr['id'].strip().find('http') == 0 :
        id = attr['id'].strip()
    else:
        id = 'https://'+attr['id'].strip()
    if id[-1] != '/' :
        id = id + '/'
    if id.find('locahost') != -1 or id.find('127.0') != -1 :
        return

    response = requests.get(id, params=params, headers=headers,stream = True)
    ip = response.raw._connection.sock.getpeername()[0]
    region = requests.get('http://ip-api.com/json/'+ip).json()
    region = region['countryCode']

    soup = BeautifulSoup(response.text, 'html.parser')
    icon_link = soup.find('link', rel='icon')

    ret = {}
    ret['attr'] = {}
    ret['name'] = soup.find('title').string.strip() 
    ret['attr']['URL'] = id
    ret['attr']['IP'] = ip
    ret['region'] = region

    if icon_link is not None:
        if icon_link['href'].find('http') >= 0 :
            icon_link = icon_link['href']
        else:
            icon_link = id + icon_link['href']
        ret['avatar'] = requests.get(icon_link).content

    return ret