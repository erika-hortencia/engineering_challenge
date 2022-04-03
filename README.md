# engineering_challenge
Solução para o desafio de engenharia desenvolvida em __Python 3.10.2__

Para executar o arquivo utilize o seguinte comando no terminal:
```python erika_desafio_engenharia.py ```

Com base na estrutura, restrições e nos dados fornecidos foram resolvidos os seguintes itens:

- [x] Identificar a região de destino de cada pacote, com totalização de pacotes (soma região)
- [x] Saber quais pacotes possuem códigos de barras válidos e/ou inválidos
- [x] Identificar os pacotes que têm como origem a região Sul e Brinquedos em seu conteúdo
- [x] Listar os pacotes agrupados por região de destino (Considere apenas pacotes válidos)
- [x] Listar o número de pacotes enviados por cada vendedor (Considere apenas pacotes válidos)
- [x] Gerar o relatório/lista de pacotes por destino e por tipo (Considere apenas pacotes válidos)
- [x] Se o transporte dos pacotes para o Norte passa pela Região Centro-Oeste, quais são os pacotes que devem ser despachados no mesmo caminhão?
- [x] Se todos os pacotes fossem uma fila qual seria a ordem de carga para o Norte no caminhão para descarregar os pacotes da Região Centro Oeste primeiro
- [x] No item acima considerar que as jóias fossem sempre as primeiras a serem descarregadas;
- [x] Listar os pacotes inválidos

Na tabela abaixo estão as funções utilizadas para responder a cada item:

| Item | Função                     |
|------|----------------------------|
| 1    | listarPacotesDestino()     |
| 2    | retornaPacotesValidos()    |
| 3    | sulBrinquedos()            |
| 4    | exibePacotesAgrupados()    |
| 5    | listaPacotesVendedor()     |
| 6    | listaPacotesDestinoTipo()  |
| 7    | despacharMesmoCaminhao()   |
| 8    | listarOrdemDeCarga()       |
| 9    | listarOrdemPriorizaJoias() |
| 10   | listaInvalidos()           |
