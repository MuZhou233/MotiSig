import requests
import time
import os
import re
from bs4 import BeautifulSoup
from . import configs

config = {
    'summurl': 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
    'ownedurl': 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/',
    'idurl': 'https://steamidfinder.com/lookup/'
}

def data(attr):
    #Get steam 64bit-id
    if not re.match('[0-9]{17}', attr['id']):
        soup = BeautifulSoup(requests.get(config['idurl']+attr['id']).text, 'html.parser')
        for v in soup.find('div', attrs={"class":"panel-body"}).find_all('code'):
            if re.match('[0-9]{17}', v.string.strip()):
                attr['id'] = v.string.strip()

    d = {'key':configs.token('steam'), 'steamids':attr['id'], 'format':'json'}
    data = requests.get(config['summurl'], params=d).json()
    data = data['response']['players'][0]

    d = {'key':configs.token('steam'), 'steamid':attr['id'], 'format':'json'}
    tmp = requests.get(config['ownedurl'].split('\n')[0], params=d).json()
    data['game_count'] = tmp['response']['game_count']

    ret = {}; ret['attr'] = {}; ret['logos'] = []

    ret['name'] = data['personaname']
    ret['attr']['Last Log'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(data['lastlogoff']))
    ret['attr']['Game Count'] = data['game_count']
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