"""
Módulo responsável por salvar métricas em arquivos CSV.

O trabalho exige coleta experimental.
Por isso, os resultados dos algoritmos são salvos em arquivos na pasta results/.

Os CSVs ajudam a:
- comparar algoritmos;
- montar tabela no relatório;
- comprovar execução;
- reproduzir os resultados.
"""

import csv
from pathlib import Path
from typing import List

from search_classic import SearchResult
from search_local import LocalSearchResult
from search_online import OnlineResult


def save_classic_metrics(results: List[SearchResult], path: str) -> None:
    """
    Salva as métricas dos algoritmos clássicos.

    Cada linha representa um algoritmo:
    BFS, DFS, UCS, Gulosa ou A*.
    """

    # Garante que a pasta de destino exista.
    # Exemplo: results/
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        # Cabeçalho do CSV.
        writer.writerow([
            "Algoritmo",
            "Sucesso",
            "Custo",
            "Passos",
            "Explorados",
            "Expandidos",
            "Tempo",
            "Fronteira",
        ])

        # Escreve uma linha para cada resultado.
        for result in results:
            writer.writerow([
                result.algorithm,
                result.success,
                result.cost,
                result.steps,
                result.explored,
                result.expanded,
                f"{result.elapsed:.8f}",
                result.max_frontier,
            ])


def save_local_metrics(results: List[LocalSearchResult], path: str) -> None:
    """
    Salva métricas consolidadas da busca local.

    Como busca local roda várias vezes, salvamos:
    - melhor custo;
    - pior custo;
    - custo médio;
    - tempo médio;
    - iterações médias;
    - taxa de sucesso.
    """

    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow([
            "Algoritmo",
            "Melhor Custo",
            "Pior Custo",
            "Custo Medio",
            "Tempo Medio",
            "Iteracoes Medias",
            "Taxa Sucesso",
        ])

        for result in results:
            writer.writerow([
                result.algorithm,
                result.best_cost,
                result.worst_cost,
                f"{result.average_cost:.4f}",
                f"{result.average_time:.8f}",
                result.average_iterations,
                f"{result.success_rate:.2f}",
            ])


def save_online_metrics(result: OnlineResult, path: str) -> None:
    """
    Salva métricas da busca online.

    Métrica central:
        razão online/offline

    Essa razão compara:
        custo percorrido pelo agente online / custo ótimo offline

    Se for 1:
        online encontrou caminho tão bom quanto o agente com mapa completo.

    Se for maior que 1:
        houve custo adicional por falta de conhecimento do ambiente.
    """

    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow([
            "Sucesso",
            "Movimentos",
            "Custo Real",
            "Celulas Reveladas",
            "Celulas Revisitadas",
            "Replanejamentos",
            "Custo Otimo Offline",
            "Razao Online Offline",
        ])

        writer.writerow([
            result.success,
            result.movements,
            result.real_cost,
            result.revealed_cells,
            result.revisited_cells,
            result.replans,
            result.offline_cost,
            f"{result.ratio_online_offline:.4f}",
        ])
