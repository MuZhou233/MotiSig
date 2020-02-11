import requests
import os
from . import configs

config = {
    'dataurl': 'https://api.github.com/users/'
}
header = {
    'Authorization': 'token' + configs.token('github')
}

def data(attr):
    data = requests.get(config['dataurl']+attr['id'], headers=header).json()
    print(data)
    ret = {}; ret['attr'] = {}; ret['logos'] = []

    ret['name'] = data['name'] if data['name'] != None else data['login']
    ret['attr']['Repo'] = data['public_repos']
    ret['attr']['Follower'] = data['followers']
    ret['logos'].append(os.path.dirname(os.path.abspath(__file__))+'/github/logo.png')
    ret['avatar'] = requests.get(data['avatar_url'], headers=header).content

    return ret