# Registro de Uso de IA Generativa

## 1. Ferramentas Utilizadas

Foi utilizada a ferramenta ChatGPT como apoio para organização do projeto, revisão conceitual, geração inicial de estrutura de código, explicação dos algoritmos e apoio na escrita do relatório.

## 2. Principais Prompts Utilizados

- "Analise a dificuldade do trabalho prático de agente inteligente em labirinto."
- "Monte uma estrutura simples em Python para BFS, DFS, UCS, Gulosa e A*."
- "Explique uma forma simples de implementar busca local com pontos de coleta."
- "Monte uma estratégia simples de busca online com replanning A*."
- "Crie uma estrutura inicial de relatório em LaTeX."

## 3. Trechos De Código Sugeridos Por IA

A IA auxiliou na proposta inicial dos módulos:

- `maze.py`
- `search_classic.py`
- `search_local.py`
- `search_online.py`
- `metrics.py`
- `visualization.py`

## 4. Sugestões Rejeitadas

Foram rejeitadas sugestões de criar interface gráfica complexa e animação em tempo real, pois aumentariam a complexidade sem necessidade para os objetivos do trabalho.

Também foi rejeitado o uso de bibliotecas prontas de busca, para manter implementação própria dos algoritmos.

## 5. Erros Cometidos Pela IA

A IA inicialmente sugeriu uma estrutura mais ampla do que o necessário. O grupo reduziu o escopo para manter a solução simples, executável e explicável.

## 6. Como A Solução Foi Validada

A validação foi realizada executando o programa em mapa de teste, verificando:

- se os algoritmos encontravam caminho;
- se os custos eram coerentes;
- se os arquivos CSV eram gerados;
- se os gráficos eram exportados;
- se o agente online conseguia alcançar o objetivo.

## 7. Modificações Feitas Pelo Grupo

O grupo ajustou nomes, mapas, parâmetros de execução, quantidade de iterações e análise textual do relatório conforme necessidade da entrega.
