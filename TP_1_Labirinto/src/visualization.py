"""
Módulo de visualização.

Este arquivo gera:
- imagem do caminho encontrado;
- imagem da trajetória online;
- gráfico de convergência da busca local;
- impressão do caminho no terminal.

A visualização foi mantida simples para facilitar explicação e reduzir risco.
"""

from pathlib import Path
from typing import List

import matplotlib.pyplot as plt

from maze import Maze, Position


def draw_path(maze: Maze, path: List[Position], visited: List[Position], title: str, output_path: str) -> None:
    """
    Desenha o labirinto com nós visitados e caminho final.

    Convenção visual:
    - "." representa células visitadas/expandidas;
    - "*" representa o caminho final;
    - "#" continua sendo parede;
    - A e B são preservados.
    """

    # Copia o mapa para não alterar o original.
    grid = maze.copy_grid()

    # Marca as células visitadas.
    for r, c in visited:
        if grid[r][c] == " ":
            grid[r][c] = "."

    # Marca o caminho final.
    # O caminho sobrescreve "." porque ele é mais importante visualmente.
    for r, c in path:
        if grid[r][c] == " " or grid[r][c] == ".":
            grid[r][c] = "*"

    # Converte a matriz novamente para linhas de texto.
    lines = ["".join(row) for row in grid]

    # Garante que a pasta do arquivo exista.
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Gera uma figura simples com texto monoespaçado.
    # Isso preserva o formato ASCII do labirinto.
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.title(title)
    plt.text(0, 1, "\n".join(lines), family="monospace", fontsize=11, va="top")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def draw_online_path(maze: Maze, path: List[Position], title: str, output_path: str) -> None:
    """
    Desenha a trajetória real percorrida pelo agente online.

    Aqui não marcamos todos os nós expandidos, apenas o caminho efetivamente
    percorrido pelo agente.
    """

    grid = maze.copy_grid()

    for r, c in path:
        if grid[r][c] == " ":
            grid[r][c] = "*"

    lines = ["".join(row) for row in grid]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.title(title)
    plt.text(0, 1, "\n".join(lines), family="monospace", fontsize=11, va="top")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def draw_convergence(convergence: List[float], title: str, output_path: str) -> None:
    """
    Gera o gráfico de convergência da busca local.

    Eixo X:
        iteração

    Eixo Y:
        melhor custo encontrado até aquele momento

    Esse gráfico mostra se o algoritmo melhorou rapidamente,
    ficou preso ou continuou encontrando soluções melhores.
    """

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(range(len(convergence)), convergence)
    plt.xlabel("Iteração")
    plt.ylabel("Melhor custo")
    plt.title(title)
    plt.grid(True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def print_path_on_terminal(maze: Maze, path: List[Position]) -> None:
    """
    Imprime o mapa no terminal com o caminho final.

    Isso é útil para demonstrar o resultado mesmo sem abrir as imagens.
    """

    grid = maze.copy_grid()

    for r, c in path:
        if grid[r][c] == " ":
            grid[r][c] = "*"

    for row in grid:
        print("".join(row))
