# -------------------------------------------------------ESTRUTURA-------------------------------------------------------
# Código de barras
#       Trinca 1: Região de origem 
#       Trinca 2: Região de destino
#       Trinca 3: Código da Loggi
#       Trinca 4: Código do vendedor do produto
#       Trinca 5: Tipo do produto
#
# Código de região [ordenados pela ordem de entrega na rota]
#       Centro-oeste: 201 a 299
#       Nordeste:     300 a 399
#       Norte:        400 a 499
#       Sudeste:      001 a 099
#       Sul:          100 a 199
#
# Códigos de produto
#       Jóias:        001
#       Livros:       111
#       Eletrônicos:  333
#       Bebidas:      555
#       Brinquedos:   888
#
# Restrições
#       Não enviar produtos de tipos diferentes dos mencionados acima
#       Pacotes contendo jóias não podem vir da região centro-oeste
#       Pacotes com código de vendedor 367 (trinca 4 = 367) serão considerados inválidos
#
# -------------------------------------------------------SAÍDAS-------------------------------------------------------
# 1) Identificar a região de destino de cada pacote, com soma por região
# 2) Saber quais pacotes possuem código de barra válido e/ou inválido
# 3) Identificar pacotes que têm como origem a região Sul e Brinquedos em seu conteúdo
# 4) Listar pacotes agrupados por região de destino (apenas pacotes válidos)
# 5) Listar o número de pacotes enviados por cada vendedor (apenas pacotes válidos)
# 6) Gerar relatório/lista de pacotes por destino e por tipo (apenas pacotes válidos)
# 7) Se o transporte dos pacotes para o Norte passa pela Região Centro-Oeste, quais são os pacotes que devem ser despachados no mesmo caminhão?
# 8) Se todos os pacotes fossem uma fila qual seria a ordem de carga para o Norte no caminhão para descarregar os pacotes da Região Centro Oeste primeiro?
# 9) No item acima considerar que as jóias fossem sempre as primeiras a serem descarregadas
# 10) Listar os pacotes inválidos

import json

"""
Escrevendo no arquivo json
"""
def escreverJSON(lista):
    # Escrevendo a lista de dicionários no arquivo json
    jsonFile = open("Pacotes.json", "w")
    data = json.dumps(lista, indent=2)
    jsonFile.write(data)
    jsonFile.close()

"""
Lendo o arquivo json
"""
def lerJSON():
    # Abrindo o arquivo json
    arquivo = open('Pacotes.json', 'r')
    dados = arquivo.read()
    pacotes = json.loads(dados)

    return pacotes

"""
Removendo todos os registros do arquivo json
"""
def limpaJSON():
    jsonFile = open("Pacotes.json", "r+")
    jsonFile.seek(0)
    jsonFile.truncate()


"""
Separando as trincas do código de barra, adicionando os valores aos campos correspondentes no dicionário 
e escrevendo os dados no arquivo json
"""
def inicializarPacotes(pacotes):
    n = 3
    # Dicionário que irá conter os dados dos pacotes, o campo status é iniciado como 'empty' 
    # e posteriormente poderá ser 'válido' ou 'inválido', dependendo dos critérios estipulados na estrutura
    pacoteDict = {
        'ID': 0,
        'Origem': 0,
        'Destino': 0,
        'Transportadora': 0,
        'Vendedor': 0,
        'Produto': 0,
        'Status': 'Empty',
    }
    pacotesDict = [] # Lista que irá conter os dicionários com os dados dos pacotes

    # Percorrendo a lista original com os códigos dos pacotes
    for pacote in pacotes:

        pacoteDict['ID'] = pacotes.index(pacote) + 1

        # Percorrendo cada um dos códigos e setando cada trinca no respectivo campo do dicionário
        for index in range(0, len(pacote), n):
            if index == 0*n:
                pacoteDict['Origem'] = pacote[index:index+ n]
            if index == 1*n:
                pacoteDict['Destino'] = pacote[index:index+ n]
            if index == 2*n:
                pacoteDict['Transportadora'] = pacote[index:index+ n]
            if index == 3*n:
                pacoteDict['Vendedor'] = pacote[index:index+ n]
            if index == 4*n:
                pacoteDict['Produto'] = pacote[index:index+ n]

        pacotesDict.append(pacoteDict.copy()) # Adicionando oo dicionário à lista de pacotes

    escreverJSON(pacotesDict)

    

"""
Listando os pacotes por destino
"""
def listarPacotesDestino(destinos):
    
    pacotes = lerJSON()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Identificado região de destino de cada pacote...')
    print('----------------------------------------------------------------------------------------------------------------------')
    
    # Percorrendo a lista dos pacotes para ler o código de destino,
    # conforme os ranges estipulados na estrutura é atualizada a contagem de pacotes por região
    for pacote in pacotes:
        print('Pacote => '+ str(pacote))
        if int(pacote['Destino']) <= 0 or int(pacote['Destino'])> 500:
            pacote['Status'] = 'Invalido'
            print('Destino => Invalido')
        elif int(pacote['Destino']) < 100:
            destinos['Sudeste'] += 1
            print('Destino => Sudeste')
        elif int(pacote['Destino']) < 200:
            destinos['Sul'] += 1
            print('Destino => Sul')
        elif int(pacote['Destino']) < 300:
            destinos['Centro-oeste'] += 1
            print('Destino => Centro-oeste')
        elif int(pacote['Destino']) < 400:
            destinos['Nordeste'] += 1
            print('Destino => Nordeste')
        elif int(pacote['Destino']) < 500:
            destinos['Norte'] += 1
            print('Destino => Norte')

        escreverJSON(pacotes)

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Total de pacotes por região de destino:')
    print('----------------------------------------------------------------------------------------------------------------------')
    print(destinos)
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Checando quais pacotes têm código de barras inválido
    Foram observados as seguintes condições:
        - Código do produto deve ser um dos explicitados na estrutura
        - Código da região deve estar dentro dos ranges válidos
        - Se o código do produto for '001' [jóia], origem não pode ser centro-oeste [201 a 299]
        - Código do vendedor não pode ser 367
"""
def validaPacote():
    pacotes = lerJSON()

    produtosValidos = ['001', '111', '333', '555', '888'] # Lista que contém os códigos válidos para os produtos

    for pacote in pacotes:
        # Verifica se o pacote contém produtos válidos
        if pacote['Produto'] not in produtosValidos:
            pacote['Status'] = 'Invalido'
        # Verifica se o código de destino é válido
        elif int(pacote['Destino']) <= 0 or int(pacote['Destino'])> 500:
            pacote['Status'] = 'Invalido'
        # Verifica se o código de origem é válido
        elif int(pacote['Origem']) <= 0 or int(pacote['Destino'])> 500:
            pacote['Status'] = 'Invalido'
        # Verifica se há pacotes de origem no centro-oeste contendo jóias
        elif pacote['Produto'] == '001' and 201 <= int(pacote['Origem']) <= 299:
            pacote['Status'] = 'Invalido'
        # Verifica se há pacotes do vendedor bloqueado
        elif pacote['Vendedor'] == '367':
            pacote['Status'] = 'Invalido'
        # Se nenhuma dessas condições foi encontrada, o pacote é válido
        else:
            pacote['Status'] = 'Valido'

    #Atualiza status dos pacotes no arquivo json
    escreverJSON(pacotes)

"""
Verificando quais pacotes possuem código válido e inválido
"""
def retornaPacotesValidos(listaPacotes):
    validaPacote()

    pacotes = lerJSON()

    pacotesValidos = []
    pacotesInvalidos = []

    # Percorre todos os pacotes
    for pacote in pacotes:
        # Adiciona à lista de pacotes válidos, se for o caso
        if pacote['Status'] == 'Valido':
            pacotesValidos.append(pacote['ID'])
        # Adiciona à lista de pacotes inválidos, se for o caso
        else:
            pacotesInvalidos.append(pacote['ID'])

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                                   Pacotes Validos')
    print('----------------------------------------------------------------------------------------------------------------------')
    for i in pacotesValidos:
        print(str(i) + ':' + listaPacotes[(i-1)])
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                                   Pacotes Invalidos')
    print('----------------------------------------------------------------------------------------------------------------------')
    for i in pacotesInvalidos:
        print(str(i) + ':' + listaPacotes[(i-1)])
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Identificando pacotes com origem na região Sul que têm Brinquedos como produto
"""
def sulBrinquedos():
    pacotes = lerJSON()
    pacotesEncontrados = []

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                             Buscando pacotes com origem na região Sul contendo brinquedos...')
    print('----------------------------------------------------------------------------------------------------------------------')

    for pacote in pacotes:
        if 100 <= int(pacote['Origem']) <= 199 and pacote['Produto'] == '888':
            pacotesEncontrados.append(pacote)
    
    print(f'Encontramos {len(pacotesEncontrados)} pacote(s) correspondente(s), detalhes abaixo:')
    if(len(pacotesEncontrados) > 0):
        print(pacotesEncontrados)
    else:
        print('     Nenhum pacote correspondente aos critérios de busca')
    print('----------------------------------------------------------------------------------------------------------------------')
    
"""
Agrupando pacotes pela região de destino [função auxiliar utilizada por exibePacotesAgrupados() e listaPacotesDestinoTipo()]
OBS.:   pensei em alterar origem e destino de números para o nome da região na função listarPacotesDestino(), 
        o que tornaria a função abaixo menos verbosa, porém julguei necessário manter o código no json já que provavelmente
        o código está ligado não apenas à região, mas também à cidade de destino
"""
def agrupaDestino():
    destinoCentroOeste = []
    destinoNordeste = []
    destinoNorte = []
    destinoSudeste = []
    destinoSul = []

    pacotesAgrupados = {}

    pacotes = lerJSON()

    # Percorrendo a lista dos pacotes para ler o código de destino,
    # conforme os ranges estipulados na estrutura é atualizada a contagem de pacotes por região
    for pacote in pacotes:
        if pacote['Status'] == 'Valido':
            if int(pacote['Destino']) < 100:
                destinoSudeste.append(pacote)
            elif int(pacote['Destino']) < 200:
                destinoSul.append(pacote)
            elif int(pacote['Destino']) < 300:
                destinoCentroOeste.append(pacote)
            elif int(pacote['Destino']) < 400:
                destinoNordeste.append(pacote)
            elif int(pacote['Destino']) < 500:
                destinoNorte.append(pacote)
    
    pacotesAgrupados['Sudeste'] = destinoSudeste
    pacotesAgrupados['Sul'] = destinoSul
    pacotesAgrupados['Centro-oeste'] = destinoCentroOeste
    pacotesAgrupados['Nordeste'] = destinoNordeste
    pacotesAgrupados['Norte'] = destinoNorte

    return pacotesAgrupados

"""
Listando pacotes agrupados por região de destino
"""
def exibePacotesAgrupados():
    base = agrupaDestino()
    
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Agrupando pacotes por região de destino...')
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Centro-oeste:')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Centro-oeste']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Nordeste:')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Nordeste']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Norte:')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Norte']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Sudeste:')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Sudeste']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Sul:')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Sul']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')
    
"""
Listando o número de pacotes por vendedor
"""
def listaPacotesVendedor():
    vendedores = {}

    pacotes = lerJSON()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Contando pacotes por vendedor...')
    print('----------------------------------------------------------------------------------------------------------------------')

    for pacote in pacotes:
        if pacote['Status'] == 'Valido':
            if pacote['Vendedor'] in vendedores:
                vendedores[pacote['Vendedor']] += 1
            else:
                vendedores[pacote['Vendedor']] = 1
    
    print(vendedores)
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Printando pacotes por destino e por tipo [função auxiliar utilizada por listaPacotesDestinoTipo()]
"""
def exibePacotesDestinoTipo(joias, livros, eletronicos, bebidas, brinquedos):
    print('Jóias:')
    for item in joias:
        print(item)
    print('Livros:')
    for item in livros:
        print(item)
    print('Eletrônicos:')
    for item in eletronicos:
        print(item)
    print('Bebidas:')
    for item in bebidas:
        print(item)
    print('Brinquedos:')
    for item in brinquedos:
        print(item)

"""
Limpando as listas com tipo de produto por região [função auxiliar utilizada por listaPacotesDestinoTipo()]
"""
def limpaLista():
    joias = []
    livros = []
    eletronicos = []
    bebidas = []
    brinquedos = []

    return(joias, livros, eletronicos, bebidas, brinquedos)


"""
Listando pacotes por destino e por tipo
"""
def listaPacotesDestinoTipo():
    base = agrupaDestino()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                           Agrupando pacotes por região de destino e tipo de produto...')
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Centro-oeste:')
    print('----------------------------------------------------------------------------------------------------------------------')
    joias, livros, eletronicos, bebidas, brinquedos = limpaLista()
    for pacote in base['Centro-oeste']:
        if pacote['Produto'] == '001':
            joias.append(pacote)
        elif pacote['Produto'] == '111':
            livros.append(pacote)
        elif pacote['Produto'] == '333':
            eletronicos.append(pacote)
        elif pacote['Produto'] == '555':
            bebidas.append(pacote)
        elif pacote['Produto'] == '888':
            brinquedos.append(pacote)
    exibePacotesDestinoTipo(joias, livros, eletronicos, bebidas, brinquedos)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Nordeste:')
    print('----------------------------------------------------------------------------------------------------------------------')
    joias, livros, eletronicos, bebidas, brinquedos = limpaLista()
    for pacote in base['Nordeste']:
        if pacote['Produto'] == '001':
            joias.append(pacote)
        elif pacote['Produto'] == '111':
            livros.append(pacote)
        elif pacote['Produto'] == '333':
            eletronicos.append(pacote)
        elif pacote['Produto'] == '555':
            bebidas.append(pacote)
        elif pacote['Produto'] == '888':
            brinquedos.append(pacote)
    exibePacotesDestinoTipo(joias, livros, eletronicos, bebidas, brinquedos)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Norte:')
    print('----------------------------------------------------------------------------------------------------------------------')
    joias, livros, eletronicos, bebidas, brinquedos = limpaLista()
    for pacote in base['Norte']:
        if pacote['Produto'] == '001':
            joias.append(pacote)
        elif pacote['Produto'] == '111':
            livros.append(pacote)
        elif pacote['Produto'] == '333':
            eletronicos.append(pacote)
        elif pacote['Produto'] == '555':
            bebidas.append(pacote)
        elif pacote['Produto'] == '888':
            brinquedos.append(pacote)
    exibePacotesDestinoTipo(joias, livros, eletronicos, bebidas, brinquedos)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Sudeste:')
    print('----------------------------------------------------------------------------------------------------------------------')
    joias, livros, eletronicos, bebidas, brinquedos = limpaLista()
    for pacote in base['Sudeste']:
        if pacote['Produto'] == '001':
            joias.append(pacote)
        elif pacote['Produto'] == '111':
            livros.append(pacote)
        elif pacote['Produto'] == '333':
            eletronicos.append(pacote)
        elif pacote['Produto'] == '555':
            bebidas.append(pacote)
        elif pacote['Produto'] == '888':
            brinquedos.append(pacote)
    exibePacotesDestinoTipo(joias, livros, eletronicos, bebidas, brinquedos)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                     Pacotes Sul:')
    print('----------------------------------------------------------------------------------------------------------------------')
    joias, livros, eletronicos, bebidas, brinquedos = limpaLista()
    for pacote in base['Sul']:
        if pacote['Produto'] == '001':
            joias.append(pacote)
        elif pacote['Produto'] == '111':
            livros.append(pacote)
        elif pacote['Produto'] == '333':
            eletronicos.append(pacote)
        elif pacote['Produto'] == '555':
            bebidas.append(pacote)
        elif pacote['Produto'] == '888':
            brinquedos.append(pacote)
    exibePacotesDestinoTipo(joias, livros, eletronicos, bebidas, brinquedos)
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Listando pacotes que devem ser despachados no mesmo caminhão [destino norte e centro-oeste]
"""
def despacharMesmoCaminhao():
    base = agrupaDestino()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                 Os pacotes abaixo devem ser despachados no mesmo caminhão')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Centro-oeste']:
        print(pacote)
    for pacote in base['Norte']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Listando a ordem de carga do caminhão para o norte, de forma que os pacotes do centro-oeste sejam descarregados primeiro
    Pra essa função foi adotada a noção de fila "física", onde os pacotes carregados primeiros seriam os últimos a serem descarregados.
    Assim, os pacotes destinados à região Norte devem ser carregado antes dos pacotes destinados ao Centro-oeste
"""
def listarOrdemDeCarga():
    base = agrupaDestino()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                 Ordem de carregamento do caminhão para a região Norte')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Norte']:
        print(pacote)
    for pacote in base['Centro-oeste']:
        print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Essa função repete o que foi feito na listarOrdemDeCarga(), dessa vez priorizando a descarga das jóias
"""
def listarOrdemPriorizaJoias():
    base = agrupaDestino()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                            Ordem de carregamento do caminhão priorizando a descarga das jóias')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in base['Norte']:
        if pacote['Produto'] == '111':
            print(pacote)
        if pacote['Produto'] == '333':
            print(pacote)
        if pacote['Produto'] == '555':
            print(pacote)
        if pacote['Produto'] == '888':
            print(pacote)
        if pacote['Produto'] == '001':
            print(pacote)
    for pacote in base['Centro-oeste']:
        if pacote['Produto'] == '111':
            print(pacote)
        if pacote['Produto'] == '333':
            print(pacote)
        if pacote['Produto'] == '555':
            print(pacote)
        if pacote['Produto'] == '888':
            print(pacote)
        if pacote['Produto'] == '001':
            print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')

"""
Listando pacotes inválidos
"""
def listaInvalidos():
    pacotes = lerJSON()

    print('----------------------------------------------------------------------------------------------------------------------')
    print('                                         Listando pacotes inválidos')
    print('----------------------------------------------------------------------------------------------------------------------')
    for pacote in pacotes:
        if pacote['Status'] == 'Invalido':
            print(pacote)
    print('----------------------------------------------------------------------------------------------------------------------')


    

if __name__ == '__main__':
    pacotes =['288355555123888', '335333555584333','223343555124001', '002111555874555','111188555654777', '111333555123333', 
            '432055555123888', '079333555584333','155333555124001', '333188555584333', '555288555123001', '111388555123555', 
            '288000555367333','066311555874001', '110333555123555', '333488555584333', '455448555123001', '022388555123555', 
            '432044555845333', '034311555874001']
    
    destinos = {
    'Centro-oeste': 0,
    'Nordeste': 0,
    'Norte': 0,
    'Sudeste': 0,
    'Sul': 0
    }

    limpaJSON()
    
    inicializarPacotes(pacotes)

    listarPacotesDestino(destinos)

    retornaPacotesValidos(pacotes)

    sulBrinquedos()

    exibePacotesAgrupados()

    listaPacotesVendedor()

    listaPacotesDestinoTipo()

    despacharMesmoCaminhao()

    listarOrdemDeCarga()

    listarOrdemPriorizaJoias()

    listaInvalidos()

    
