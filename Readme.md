
# Projeto PPP

## Executando o projeto
Opções para executar o projeto:
1. Baixe o projeto num diretório, crie um virtualenv, instale as libs especificadas no requirements.txt. Feito isso, execute no Terminal `python manage.py runserver` depois acesse no seu browser http://localhost:8000/api/docs ou execute os exemplos a seguir numa outra aba do seu Terminal
2. Veja a seção "Docker"
## Bash scripts

1 - Identificar o usuário que tem o maior “size” (Bônus: ser capaz de informar o usuário de menor “size” dado um parâmetro).:

    $ ./max-min-size.sh input ↵
    juvati_be@uol.com.br inbox 000232478 size 012345671

    #Bônus: capaz de informar o usuário de menor "size" dado um parâmetro: "-min"
    $ ./max-min-size.sh input -min ↵
    wjogilabe@uol.com.br inbox 012344022 size 000000008

2 - Ordenar os “users” em ordem alfabética (Bônus: capaz de ordenar de forma decrescente dado um parâmetro). Abaixo um exemplo:

    $ ./order-by-username.sh input| head -n 3 ↵
    aadmoq@uol.com.br inbox 010030343 size 012115112
    aasurari@uol.com.br inbox 000014415 size 002331211
    abefadibi@uol.com.br inbox 000141552 size 012042478

    #Bônus: capaz de ordenar de forma descrescente dado um parâmetro: "-desc"
    $ ./order-by-username.sh input -desc | head -n 3 ↵
    zzvenaju@uol.com.br inbox 001004028 size 000105267
    zzbarica@uol.com.br inbox 001120321 size 000023348
    zyzjuf@uol.com.br inbox 002004113 size 000312436

3 - Identificar os usuários que estão na seguinte faixa de quantidade de mensagens na INBOX:

    $ ./between-msgs.sh input 50 200 ↵
    hgioep@uol.com.br inbox 000000050 size 001003108
    vinecitoma@uol.com.br inbox 000000165 size 001214178
    rovejusita@uol.com.br inbox 000000153 size 002122412
    qivigeva@uol.com.br inbox 000000124 size 001134104

Todos os scripts implementam o argumento "help" para exibir um texto de ajuda ;-)
Exemplo: 

    $ ./max-min-size.sh help ↵
    Use: max-min-size [input] [options]: Retorna o usuario com maior size
    Options:
        no options: Retorna o usuario com maior size
        -max: Retorna o usuario com maior size
        -min: Retorna o usuario com menor size

## Python API

    ** As urls da API usadas no exemplo abaixo devem ser alteradas para o seu ambiente ;-)
    ** Os endpoints podem ser testados diretamente na documentação acessando no seu browser:
    http://localhost:8000/api/docs

1 – Desenvolver um recurso para upload de arquivo, o mesmo só permitirá arquivos de nome com caracteres A-Z, a-z, 0-9, - (hífen) e _ (underline). O arquivo deverá ser salvo em uma pasta que aplicação criará (exemplo: /tmp/teste-api):

**Endpoint:** /api/upload/filename

**Method:** PUT

**Responses:**
|Status|Resultado| 
|--|--|
|201| caso o arquivo exista  
|204| caso já exista arquivo com o mesmo nome e foi substituído |
|400| nome de arquivo inválido

Exemplo:

    $ curl http://localhost:8000/api/upload/input --upload-file input ↵
    $ OK%
    $ curl http://localhost:8000/api/upload/NomeInválidoDe&arquivo --upload-file input ↵
    $ nome de arquivo invalido%

2 - Desenvolver um recurso para listagem de arquivos armazenados (Bônus: implementar um mecanismo de paginação):

**Endpoint:** /api/arquivos

**Method:** GET

**Response:**
|Status|Resultado| 
|--|--|
|200| devolve a lista de arquivos submetidos com o total de paginas

Exemplo 1 -  sem paginação:

    $ curl http://localhost:8000/api/arquivos ↵
    $ {"arquivos": ["arquivo1", "arquivo2",...,"arquivoN"], "total_paginas": 0}%  

Exemplo 2 - resultados paginados:

    $ curl http://localhost:8000/api/arquivos/1 ↵
    $ {"arquivos": ["arquivo1", "arquivo2",...,"arquivoN"], "total_paginas": 12}%  

Exemplo 3 - página não existe:

    $ curl http://localhost:8000/api/arquivos/158 ↵
    $ {"arquivos": [], "total_paginas": 12}%  

3 – Desenvolver um recurso para obter usuário com tamanho maior size (Bônus: desenvolver também um recurso para menor size), deverá receber o nome de um arquivo que foi armazenado para ser processado utilizando script desenvolvido anteriormente:

**Endpoint:** /api/users/filename/[min|max]

**Method:** GET

**Response:**
|Status|Content| 
|--|--|
|200| devolve o registro encontrado no arquivo [filename]
|404| arquivo informado não armazenado

Exemplo 1: buscando usuário com maior size num arquivo "input"

    $ curl http://localhost:8000/api/users/input/max ↵
    $ {"user": "juvati_be@uol.com.br", "folder": "inbox", "numberMessages": 232478, "size": 12345671}%
Exemplo 2: buscando usuário com menor size num arquivo "input"

    $ curl http://localhost:8000/api/users/input/min ↵
    $ {"user": "wjogilabe@uol.com.br", "folder": "inbox", "numberMessages": 12344022, "size": 8}%
Exemplo 3: buscando num arquivo que não existe

    $ curl http://localhost:8000/api/users?filename=arquivonaoexiste ↵
    $ Arquivo informado não armazenado%

4 - Desenvolver um recurso para obter a lista de usuários ordenados pelo nome de usuário (Bônus: 
1 - permitir também ordenar de forma decrescente; 2 - implementar um mecânimos de paginação, 3 –
parâmetro para filtro pelo username), deverá receber o nome de um arquivo que foi armazenado
para ser processado utilizando script desenvolvido anteriormente:

**Endpoint:** /api/users/ordered/filename/[page|search|limit]=value

**Method:** GET

**Response:**

Obrigatórios
|Status|Parametro|Resultado| 
|--|--|--|
|200| [asc\|desc] |retorna os registros ordenados: asc(endente) desc(endente)
|200| filename|indica o arquivo em que a busca deve ser feita

Erros
|Status|Parametro|Resultado| 
|--|--|--|
|404| filename|se o arquivo indicado por filename não existir no diretorio da aplicação

Filtros

|Status|Parametros opcionais|Resultado| 
|--|--|--|
|200| search=termo |devolve o registro contendo o termo em username
|200| limit=limite |devolve a quantidade de registros definido em limit
|200| page=numero_pagina |retorna os registros contidos na pagina especificada em numero_pagina

Exemplo 1: ordenando ascendente

    $ curl http://localhost:8000/api/users/ordered/input/asc ↵
    {"users": [{"user": "aadmoq@uol.com.br", "folder": "inbox", "numberMessages": 10030343, "size": 12115112}, {"user": "aasurari@uol.com.br", "folder": "inbox", "numberMessages": 14415, "size": 2331211}, {"user": "abefadibi@uol.com.br", "folder": "inbox", "numberMessages": 141552, "size": 12042478}, {"user": "abeteberi@uol.com.br", "folder": "inbox", "numberMessages": 12200652, "size": 2203617}, {"user": "abijejow@uol.com.br", "folder": "inbox", "numberMessages": 1225664, "size": 12313524}, {"user": "abijuduro@uol.com.br", "folder": "inbox", "numberMessages": 10335332, "size": 11100427}, {"user": "abi_lsu@uol.com.br", "folder": "inbox", "numberMessages": 2134370, "size": 24072}, {"user": "abitluh@uol.com.br", "folder": "inbox", "numberMessages": 2235050, "size": 1130616}, {"user": "ablazmo@uol.com.br", "folder": "inbox", "numberMessages": 2121230, "size": 213536}, {"user": "abpepmo@uol.com.br", "folder": "inbox", "numberMessages": 2244570, "size": 10324107}, {(...)}], "total_paginas": 6}% 

Exemplo 2: ordenando descendente

    $ curl http://localhost:8000/api/users/ordered/input/desc ↵
    {"users": [{"user": "zzvenaju@uol.com.br", "folder": "inbox", "numberMessages": 1004028, "size": 105267}, {"user": "zzbarica@uol.com.br", "folder": "inbox", "numberMessages": 1120321, "size": 23348}, {"user": "zyzjuf@uol.com.br", "folder": "inbox", "numberMessages": 2004113, "size": 312436}, {(...)}], "total_paginas": 6}% 

Exemplo 3: buscando por nome, ou parte do username

    $ curl http://localhost:8000/api/users/ordered/asc?search=aad ↵
    {"user": {"user": "aadmoq@uol.com.br", "folder": "inbox", "numberMessages": 10030343, "size": 12115112}}%

Exemplo 4: paginando items

    $ curl http://localhost:8000/api/users/ordered/asc?page=1 ↵
    {"users": [{"user": "aadmoq@uol.com.br", "folder": "inbox", "numberMessages": 10030343, "size": 12115112}, {"user": "aasurari@uol.com.br", "folder": "inbox", "numberMessages": 14415, "size": 2331211}, {"user": "abefadibi@uol.com.br", "folder": "inbox", "numberMessages": 141552, "size": 12042478}, {"user": "abeteberi@uol.com.br", "folder": "inbox", "numberMessages": 12200652, "size": 2203617}, {"user": "abijejow@uol.com.br", "folder": "inbox", "numberMessages": 1225664, "size": 12313524}, {(...)}], "total_paginas": 6}% 

Exemplo 5: limitando a quantidade de items retornados

    $ curl http://localhost:8000/api/users/ordered/asc?limit=2 ↵
    {"users": [{"user": "aadmoq@uol.com.br", "folder": "inbox", "numberMessages": 10030343, "size": 12115112}, {"user": "aasurari@uol.com.br", "folder": "inbox", "numberMessages": 14415, "size": 2331211}], "total_paginas": 6}% 

5 - Desenvolver um recurso para obter a lista de usuários entre uma faixa de quantidade de mensagens na INBOX (Bônus: 1 -implementar um mecanismos de paginação; 2 - parâmetro para filtro pelo username), deverá receber o nome de um arquivo que foi armazenado para ser processado utilizando script desenvolvido  anteriormente:

**Endpoint:** /api/users/inbox/[filename]/[min]/[max]

**Method:** GET

**Response:**

Obrigatórios
|Status|Parametro|Resultado| 
|--|--|--|
|200| [min]/[max] |retorna os registros com quantidade de mensagens de INBOX entre min e max
|200| filename|indica o arquivo em que a busca deve ser feita

Erros
|Status|Parametro|Resultado| 
|--|--|--|
|404| filename|se o arquivo indicado por filename não existir no diretorio da aplicação

Filtros

|Status|Parametros opcionais|Resultado| 
|--|--|--|
|200| search=termo |devolve o registro contendo o termo em username
|200| limit=limite |devolve a quantidade de registros definido em limit
|200| page=numero_pagina |retorna os registros contidos na pagina especificada em numero_pagina

Exemplo 1: obtendo usuarios entre com numero de mensagens entre 0 e 200

    curl http://localhost:8000/api/users/inbox/input/8/200
    {"users": [{"user": "hgioep@uol.com.br", "folder": "inbox", "numberMessages": 50, "size": 1003108}, {"user": "vinecitoma@uol.com.br", "folder": "inbox", "numberMessages": 165, "size": 1214178}, {"user": "rovejusita@uol.com.br", "folder": "inbox", "numberMessages": 153, "size": 2122412}, {"user": "qivigeva@uol.com.br", "folder": "inbox", "numberMessages": 124, "size": 1134104}], "total_paginas": 1}%   

Exemplo 2: usando o filtro search

    $ curl http://localhost:8000/api/users/inbox/input/200/500?search=mrapz
    {"user": {"user": "mrapzla@uol.com.br", "folder": "inbox", "numberMessages": 323, "size": 2105523}}% 

Exemplo 3: limitando a quantidade de registros

    $ curl http://localhost:8000/api/users/inbox/input/250/1500?limit=2
    {"users": [{"user": "dibavibt@uol.com.br", "folder": "inbox", "numberMessages": 317, "size": 2012435}, {"user": "jotaztle@uol.com.br", "folder": "inbox", "numberMessages": 1243, "size": 12321611}], "total_paginas": 1}% 

## Extras (não solicitados, mas úteis):

1 – Obtém o arquivo submetido:

**Endpoint:** /api/upload/[filename]

**Method:** GET

**Response:**

Exemplo: Obtendo arquivo "input" submetido

    $ curl http://localhost:8000/api/upload/input
    <conteudo do arquivo/>
    (...)

Exemplo: Tentando obter um arquivo inexistente

    $ curl http://localhost:8000/api/upload/umarquivoqualquer
    Arquivo não encontrado%
2 - Documentação da API:

Acesse: /api/docs

Uma tela do swagger será exibida

## Docker
Para rodar a API num container, execute:

    $ cd <diretorio do projeto/>
    $ docker-compose up --build -d 

Acesse a API no browser:
http://localhost:8000

## Testes
** Submeta um arquivo "input" na pasta api-server/uploaded_files ;-)

Para executar os testes relacionados aos scripts de backend da API:

    $ python manage.py test


Para executar os testes relacionados à API no Postman

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/:19422414-7585b41c-edd2-463d-896c-f461e09e7cd0)


## Melhorias
1) Adicionar logs de erros;
2) Adicionar testes automatizados dos endpoints: atualmente temos apenas testes unitários relacionados aos scripts bash;
3) Uma lib interessante para testes: https://pypi.org/project/responses/
