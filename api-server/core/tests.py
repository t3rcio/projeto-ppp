from django.test import TestCase
from django.conf import settings

import os

from core.scripts import obtem_size, obtem_arquivos_submetidos, obtem_users_ordered
from core.paging import paginate_items, PAGE_SIZE

class TestCenarios(TestCase):

    def setUp(self):
        self.input_file = settings.UPLOADED_FILES_DIR + '/input'
    
    def test_obtem_maior_size(self):
        param = 'max'
        result = obtem_size(self.input_file, param)
        correct = {
            'user': 'juvati_be@uol.com.br',
            'folder': 'inbox',
            'numberMessages': 232478,
            'size': 12345671
        }
        self.assertEqual(result, correct)
    
    def test_obtem_menor_size(self):
        param = 'min'
        result = obtem_size(self.input_file, param)
        correct = {
            'user':'wjogilabe@uol.com.br',
            'folder': 'inbox',
            'numberMessages': 12344022,
            'size': 8
        }
        self.assertEqual(result, correct)
    
    def test_obtem_size_error_file(self):
        param = 'max'
        result = obtem_size('input2', param)
        correct = {}
        self.assertEqual(result, correct)
    
    def test_obtem_arquivos_submetidos(self):
        correct = os.listdir(settings.UPLOADED_FILES_DIR)
        result = obtem_arquivos_submetidos()
        self.assertEqual(result, correct)
    
    def test_obtem_arquivos_submetidos_paginados(self):
        correct = os.listdir(settings.UPLOADED_FILES_DIR)
        result = obtem_arquivos_submetidos()
        paginated_result = paginate_items(result)
        self.assertEqual(paginated_result.get(1, []), correct)    

    def test_paginacao_lista_items(self):
        PAGE_SIZE = 30
        items = list(range(0,100))
        paginated_result = paginate_items(items, PAGE_SIZE)        
        correct = list(range(0,30))
        pages_correct = 4
        pages_result = len(paginated_result.keys())
        self.assertEqual(paginated_result.get(1, []), correct)
        self.assertEqual(pages_result, pages_correct)
    
    def test_lista_arquivos_paginada(self):
        # Usa a PAGE_SIZE definida no settings: 50 items por pagina
        arquivos = ['input' + str(i) for i in list(range(0,500))]
        correct = ['input' + str(i) for i in list(range(0,50))]
        qtd_paginas = len(arquivos) / PAGE_SIZE

        paginated_result = paginate_items(arquivos)        
        self.assertEqual(
            correct,
            paginated_result.get(1, [])
        )
        self.assertEqual(
            qtd_paginas,
            len(paginated_result)
        )
