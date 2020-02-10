import requests
import os
from . import configs

config = {
    'dataurl': 'https://osu.ppy.sh/api/get_user',
    'avatarurl': 'https://a.ppy.sh/'
}

modemap = {
    '0': 'osu',
    '1': 'taiko',
    '2': 'ctb',
    '3': 'mania'
}

def data(attr):
    try:
        attr['mode']
    except KeyError:
        mode = '0'
    else:
        mode = attr['mode']

    d = {'k':configs.token('osu'), 'u':attr['id'], 'm':mode}
    data = requests.post(config['dataurl'], data=d).json()
    data = data[0]
    
    ret = {}; ret['attr'] = {}; ret['logos'] = []

    ret['name'] = data['username']
    ret['attr']['Rank'] = '#'+data['pp_rank']
    ret['attr']['PP'] = data['pp_raw']
    ret['attr']['Acc'] = str(round(float(data['accuracy']), 1))+'%'
    ret['logos'].append(os.path.dirname(os.path.abspath(__file__))+'/osu/logo.png')
    ret['logos'].append(os.path.dirname(os.path.abspath(__file__))+'/osu/'+modemap[mode]+'_black.png')
    ret['region'] = data['country']
    ret['avatar'] = requests.get(config['avatarurl']+data['user_id']).content

    return ret