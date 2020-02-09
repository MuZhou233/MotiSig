import requests

def data(attr):
    ret = {}; ret['attr'] = {}

    ret['name'] = 'MotiSig'
    ret['attr']['Service'] = 'Online'
    ret['attr']['Version'] = 'Alpha v0.1'

    return ret