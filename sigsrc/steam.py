import requests
import time
import os
import re
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://motisig.mosarin.tech/',
    'Content-Type': 'application/json; charset=UTF-8'
}

config = {
    'summurl': 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
    'ownedurl': 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/',
    'appdetailsurl': 'https://store.steampowered.com/api/appdetails/',
    'idurl': 'https://steamidfinder.com/lookup/',
    'token': ''
}

def data(attr):
    #Get steam 64bit-id
    if not re.match('[0-9]{17}', attr['id']):
        soup = BeautifulSoup(requests.get(config['idurl']+attr['id']).text, 'html.parser')
        for v in soup.find('div', attrs={"class":"panel-body"}).find_all('code'):
            if re.match('[0-9]{17}', v.string.strip()):
                attr['id'] = v.string.strip()

    d = {'key':config['token'], 'steamids':attr['id'], 'format':'json'}
    data = requests.get(config['summurl'], params=d).json()
    data = data['response']['players'][0]

    d = {'key':config['token'], 'steamid':attr['id'], 'format':'json'}
    tmp = requests.get(config['ownedurl'], params=d).json()
    data['game_count'] = tmp['response']['game_count']

    cappids = ""
    for x in tmp['response']['games']:
        cappids += str(x['appid']) + ','
    cappids = cappids[0:-1]
    d = { 'appids' : cappids, 'cc' : 'cn' , 'l' : 'cn' , 'filters' : 'price_overview' }
    tmp = requests.get(config['appdetailsurl'], params=d).json()
    tot_value, err_count = 0, 0
    for x in tmp.values():
        if(x['success']):
            try:
                tot_value += x['data']['price_overview']['initial']
            except TypeError:
                err_count += 1
                continue
        else:
            err_count += 1
            continue
    tot_value /= 100

    ret = {}; ret['attr'] = {}; ret['logos'] = []

    ret['name'] = data['personaname']
    ret['attr']['Last Log'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(data['lastlogoff']))
    ret['attr']['Game Count'] = data['game_count']
    ret['attr']['Total Value(Initial)'] = str(tot_value) + "CNY"
    ret['logos'].append(os.path.dirname(os.path.abspath(__file__))+'/steam/logo.png')

    try:
        data['loccountrycode']
    except KeyError:
        pass
    else:
        if len(data['loccountrycode']) == 2:
            ret['region'] = data['loccountrycode']

    ret['avatar'] = requests.get(data['avatarfull']).content
    return ret