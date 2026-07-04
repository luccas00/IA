# Trabalho Prático - Agente Inteligente em Labirinto

## Objetivo

Este projeto implementa um agente inteligente para resolver labirintos em três cenários:

1. Labirinto conhecido, usando busca clássica.
2. Labirinto com pontos de coleta obrigatórios, usando busca local.
3. Labirinto desconhecido, usando busca online com replanning A*.

## Como Executar

Requisitos:

```bash
pip install matplotlib
```

Execução:

```bash
python main.py
```

## Estrutura

```text
tp_labirinto/
├── main.py
├── maps/
│   └── mapa1.txt
├── src/
│   ├── maze.py
│   ├── search_classic.py
│   ├── search_local.py
│   ├── search_online.py
│   ├── metrics.py
│   └── visualization.py
├── results/
│   ├── metricas_classicas.csv
│   ├── metricas_busca_local.csv
│   ├── metricas_online.csv
│   └── graficos/
├── docs/
│   └── relatorio.tex
└── uso_ia.md
```

## Algoritmos Implementados

### Busca Clássica

- BFS
- DFS
- UCS
- Busca Gulosa
- A*

### Busca Local

- Hill-Climbing
- Simulated Annealing

A busca local usa a ordem dos pontos de coleta como solução candidata. O custo de uma rota é calculado somando os menores caminhos entre os pontos usando A*.

### Busca Online

Foi implementado replanning com A*. O agente inicia com mapa desconhecido, percebe a vizinhança local, atualiza seu mapa interno e replaneja a cada movimento.

## Mapas

Os mapas ficam na pasta `maps/`.

Símbolos:

- `A`: posição inicial
- `B`: objetivo final
- `C`: ponto de coleta obrigatório
- `#`: parede
- espaço: célula livre

## Resultados

A execução gera:

- CSV com métricas da busca clássica
- CSV com métricas da busca local
- CSV com métricas da busca online
- gráficos em PNG
