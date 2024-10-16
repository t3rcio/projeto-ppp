
from django.conf import settings

PAGE_SIZE_DEFAULT = 5
PAGE_SIZE = getattr(settings, 'PAGE_SIZE', PAGE_SIZE_DEFAULT)

def paginate_items(items:list, page_size:int = None) -> dict:
    '''
    Retorna um dicionario com items paginados 
    - page_size define o tamanho da pagina. 
    Se não usado usa a variavel settings.PAGE_SIZE ou o PAGE_SIZE_DEFAULT(5)
    '''
    pg_size = page_size if page_size else PAGE_SIZE    
    paginated_result = {}
    quantas_paginas = int(len(items) / pg_size if not len(items) % pg_size else (len(items) / pg_size) + 1)
    
    if quantas_paginas < 1:
        quantas_paginas = 1
    
    for i in list(range(0, quantas_paginas)):        
        start = (i*pg_size)
        end = (pg_size * (i+1))
        if end > len(items):
            end = len(items) - 1
        
        __items = items[start:end]
        paginated_result[i+1] = __items
    
    return paginated_result
