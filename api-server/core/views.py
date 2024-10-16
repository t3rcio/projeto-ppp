
import os
import re
import sys

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings

from ninja import NinjaAPI

from core.scripts import obtem_size, obtem_arquivos_submetidos, obtem_users_ordered, obtem_users_inbox
from core.paging import paginate_items

STATUS_ARQUIVO_ERR = 0
STATUS_ARQUIVO_SALVO = 1
STATUS_ARQUIVO_SUBSTITUIDO = 2
LIMIT_ITEMS = 10
USER_MAX_SIZE_PARAM = 'max'
USER_MIN_SIZE_PARAM = 'min'
FILENAME_REGEX = '^[a-zA-Z0-9\_\-]+$'

api = NinjaAPI(
    openapi_extra = {
        'info': {
            'termsOfService': 'https://github.com/t3rcio/projeto-ppp'
        }
    },
    title = 'API-Server - Projeto PPP',
    description = 'API Demo - Projeto PPP'
)

def valida_file_name(filename):
    '''
    Valida o nome do arquvo de acordo com o padrao FILENAME_REGEX
    '''
    result = False
    try:
        arquivo = filename.split('.')[0] if '.' in filename else filename
        pattern = re.compile(FILENAME_REGEX)
        return re.match(pattern, arquivo).group()
    except:
        pass
    return result


def salva_arquivo(request, filename):
    '''
    Salva arquivo submetido
    Retorna o status do arquivo: 
    - STATUS_ARQUIVO_ERR - em caso de erros no arquivo
    - STATUS_ARQUIVO_SALVO - caso o arquivo n exista
    - STATUS_ARQUIVO_SUBSTITUIDO - o arquivo existia e foi substituido
    '''
    response = STATUS_ARQUIVO_ERR
    try:
        files = os.listdir(settings.UPLOADED_FILES_DIR)
        response = STATUS_ARQUIVO_SUBSTITUIDO if filename in files else STATUS_ARQUIVO_SALVO        
        uploaded_file_path = os.path.join(settings.UPLOADED_FILES_DIR, filename)
        with open(uploaded_file_path, "wb+") as uploaded_file:
            uploaded_file.write(request.body)
        
        return response
    except:
        response = STATUS_ARQUIVO_ERR
    return response

def _404(text):
    '''
    Retorna um 404
    '''
    response = HttpResponse()
    response.status = 404
    response.content = text
    return response

@api.put('upload')
def upload_file(request, filename:str):
    '''
    Endpoint para upload de arquivos via PUT
    '''

    response = HttpResponse()
    response.status_code = 400
    response.content = 'Bad request: generic error'
    
    if request.method == 'PUT':
        if not request.body:
            response.status_code = 400
            response.content = 'Bad Request: no file'
            return response
        
        if not filename:            
            response.status_code = 400
            response.content = 'nome do arquivo não permitido'
            return response            

        filename_valido = valida_file_name(filename)        
        if not filename_valido:
            response.status_code = 400
            response.content = 'nome de arquivo não permitido'
            return response
        
        status = salva_arquivo(request, filename)
        if status == STATUS_ARQUIVO_SALVO:
            response.status_code = 201
            response.content = 'OK'
        if status == STATUS_ARQUIVO_SUBSTITUIDO:
            response.status_code = 204
            response.content = 'OK'
        if status == STATUS_ARQUIVO_ERR:
            response.status_code = 500
            response.content = 'erro ao salvar o arquivo'
    return response

@api.get('upload/{filename}')
def get_uploaded_file(request, filename:str):
    '''
    Retorna o arquivo submetido
    '''
    files = obtem_arquivos_submetidos()
    if filename not in files:
        response = HttpResponse(status=404, content='Arquivo não encontrado')
        return response
    
    file_path = os.path.join(settings.UPLOADED_FILES_DIR, filename)
    return FileResponse(open(file_path, 'rb'))
    

@api.get('arquivos')
def get_saved_files(request):
    '''
    Endpoint para retorno dos arquivos salvos
    Default: retorna pagina 1 de resultados
    '''
    response = obtem_arquivos_submetidos()
    paginated_result = paginate_items(response)
    _response = {
        'arquivos': paginated_result.get(1, []),
        'total_paginas': len(paginated_result)
    }
    return JsonResponse(_response)

@api.get('arquivos/{page}')
def get_saved_files_paginated(request, page:int):
    '''
    Endpoint para retorno dos arquivos numa pagina especificada em page (int)
    - page: pagina de resultados
    '''
    response = obtem_arquivos_submetidos()
    paginated_result = paginate_items(response)
    _response = {
        'arquivos': paginated_result.get(page, []),
        'total_paginas': len(paginated_result)
    }
    return JsonResponse(_response)    


@api.get('/users/{filename}/{size}')
def get_user_size(request, filename:str, size:str):
    '''
    Endpoint para retorno do usuario com size maximo ou minimo contido no arquivo definido em filename
    - filename: arquivo para busca
    - size: [max | min]
    '''
    response = HttpResponse()
    if not filename:
        response.status_code = 400
        response.content = 'Bad Request'
        return response
    
    param = size if size else USER_MAX_SIZE_PARAM
    result = obtem_size(filename, param)
    if not result:
        return _404('Arquivo informado não armazenado')
    
    return JsonResponse(result)

@api.get('/users/ordered/{filename}/{ordering}')
def get_users_ordered(request, filename:str, ordering:str, limit:int = 0, page:int = 1, search:str = ''):
    '''
    Endpoint para retorno de usuarios ordenados por username
    - ordering: [asc|desc]
    - filename: arquivo onde realizar a busca
    Filtros:
    - limit: quantidade de registros
    - search: buscar por um termo presente no username
    - page: indica a pagina de resultados    
    '''
    if filename not in os.listdir(settings.UPLOADED_FILES_DIR):
        return _404('Arquivo informado não armazenado')
    
    result = obtem_users_ordered(filename, ordering)
    paginated_result = paginate_items(result)    
    _response = {
        'users': paginated_result.get(page, []),
        'total_paginas': len(paginated_result)
    }
    if limit:
        __result = paginated_result.get(page, [])
        limited_result = __result[0: limit]  if __result else []
        _response = {
            'users': limited_result,
            'total_paginas': len(paginated_result)
        }

    if search:
        user = [r for r in result if search in r['user']]
        _response = {
            'user': user[0] if user else []
        }
    
    return JsonResponse(_response, safe=False)

@api.get('/users/inbox/{filename}/{min}/{max}')
def get_users_by_inbox_size(request, filename:str, min:int, max:int, limit:int = 0, page:int = 1, search:str=''):
    '''
    Endpoint para retorno de usuarios por quantidade de mensagens na INBOX
    - min: quantidade minima de mensagens na inbox
    - max: quantidade maxima de mensagens na inbox
    - filename: arquivo onde realizar a busca
    Filtros:
    - limit: quantidade de registros
    - search: buscar por um termo presente no username
    - page: indica a pagina de resultados
    '''
    if filename not in os.listdir(settings.UPLOADED_FILES_DIR):
        return _404('Arquivo informado não armazenado')
    
    result = obtem_users_inbox(filename, _min=min, _max=max)    
    paginated_result = paginate_items(result)
    _response = {
        'users': paginated_result.get(page, []),
        'total_paginas': len(paginated_result)
    }
    if limit:
        __result = paginated_result.get(page, [])
        limited_result = __result[0: limit]  if __result else []
        _response = {
            'users': limited_result,
            'total_paginas': len(paginated_result)
        }

    if search:
        user = [r for r in result if search in r['user']]
        _response = {
            'user': user[0] if user else []
        }
    
    return JsonResponse(_response, safe=False)
    