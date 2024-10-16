
import json
import os
import subprocess
import sys

from django.conf import settings


def obtem_size(filename:str, param:str) -> dict:
    '''
    Retorna o usuario com maior ou menor size no arquivo definido em filename
    '''
    try:
        uploaded_file = os.path.join(settings.UPLOADED_FILES_DIR, filename)    
        result = subprocess.check_output(
            [settings.SCRIPTS_DIR + '/' + 'max-min-size.sh', uploaded_file, '-'+param]
        ).decode('utf-8')
        
        _result = result.split(' ')
            
        return {
            'user': _result[0],
            'folder': _result[1],
            'numberMessages': int(_result[2]),
            'size': int(_result[4].replace('\n', ''))
        }
    except Exception as _error:
        # TODO: adding log error
        pass
    return {}

def obtem_arquivos_submetidos() -> list:
    result = os.listdir(settings.UPLOADED_FILES_DIR)
    return result

def obtem_users_ordered(filename:str, ordering:str = 'asc'):
    '''
    Retorna lista de usuarios ordenados por username
    - ordering: define crescente ou decrescente
    - filename: arquivo onde realizar a busca
    '''
    try:
        uploaded_file = os.path.join(settings.UPLOADED_FILES_DIR, filename)
        result = subprocess.check_output(
            [settings.SCRIPTS_DIR + '/' + 'order-by-username.sh', uploaded_file, '-'+ordering]
        ).decode('utf-8')
        
        _result = result.split('\n')        
        collection = []
        for r in _result:            
            if r:
                item = r.split(' ')
                collection.append({
                    'user': item[0],
                    'folder': item[1],
                    'numberMessages': int(item[2]),
                    'size':int(item[4].replace('\n', ''))
                })
        return collection
    except Exception as _error:
        # TODO: adding log error
        print(_error)
        pass
    return {}

def obtem_users_inbox(filename:str, _min:int, _max:int):
    '''
    Retorna lista de usuarios com quantidade de mensagens de INBOX entre min e max
    - min: quantidade minima de mensagens
    - max: quantidade maxima de mensagens
    - filename: arquivo onde realizar a busca
    '''
    try:
        uploaded_file = os.path.join(settings.UPLOADED_FILES_DIR, filename)
        result = subprocess.check_output(
            [settings.SCRIPTS_DIR + '/' + 'between-msgs.sh', uploaded_file, str(_min), str(_max)]
        ).decode('utf-8')
        
        _result = result.split('\n')        
        collection = []
        for r in _result:            
            if r:
                item = r.split(' ')
                collection.append({
                    'user': item[0],
                    'folder': item[1],
                    'numberMessages': int(item[2]),
                    'size':int(item[4].replace('\n', ''))
                })
        return collection
    except Exception as _error:
        # TODO: adding log error
        print(_error)
        pass
    return {}    