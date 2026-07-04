"""
Módulo responsável pela representação do labirinto.

Este arquivo não implementa busca.
Ele apenas define como o labirinto é carregado, armazenado e consultado.

Conceito importante:
O labirinto é tratado como uma matriz bidimensional.

Exemplo:
########
#A   B #
########

Cada caractere vira uma célula:
- A: posição inicial do agente;
- B: objetivo final;
- C: ponto de coleta obrigatório;
- #: parede;
- espaço: caminho livre.

Na apresentação:
Diga que este módulo representa o "ambiente" do agente.
"""

from dataclasses import dataclass
from typing import List, Tuple

# Position é apenas um apelido de tipo.
# Uma posição do labirinto é representada por uma tupla:
# (linha, coluna)
#
# Exemplo:
# (2, 5) significa linha 2, coluna 5.
Position = Tuple[int, int]


@dataclass
class Maze:
    """
    Classe que representa o labirinto.

    Atributos:
    - grid: matriz de caracteres do mapa;
    - start: posição inicial A;
    - goal: posição objetivo B;
    - collections: lista com todos os pontos C.

    O uso de dataclass reduz código repetitivo,
    como construtor __init__ manual.
    """

    grid: List[List[str]]
    start: Position
    goal: Position
    collections: List[Position]

    @classmethod
    def from_file(cls, path: str) -> "Maze":
        """
        Carrega um labirinto a partir de um arquivo texto.

        Exemplo de uso:
            maze = Maze.from_file("maps/mapa1.txt")

        Fluxo:
        1. lê as linhas do arquivo;
        2. transforma cada linha em uma lista de caracteres;
        3. procura A, B e C;
        4. valida se existe início e objetivo;
        5. retorna uma instância de Maze.
        """

        # Lê todas as linhas do arquivo.
        # rstrip("\\n") remove apenas a quebra de linha no final.
        # Não removemos espaços internos porque espaços representam caminhos livres.
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file if line.rstrip("\n") != ""]

        # Calcula a maior largura do mapa.
        # Isso evita erro se alguma linha vier menor que outra.
        width = max(len(line) for line in lines)

        # Converte cada linha em uma lista de caracteres.
        # ljust(width) completa linhas menores com espaços.
        # Isso mantém a matriz retangular.
        grid = [list(line.ljust(width)) for line in lines]

        # Variáveis que serão preenchidas ao percorrer o mapa.
        start = None
        goal = None
        collections = []

        # Percorre todas as células da matriz.
        # r = índice da linha
        # c = índice da coluna
        # value = caractere naquela posição
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                if value == "A":
                    start = (r, c)
                elif value == "B":
                    goal = (r, c)
                elif value == "C":
                    collections.append((r, c))

        # Validação básica.
        # Sem A ou sem B, o problema de busca não tem definição correta.
        if start is None:
            raise ValueError("Mapa inválido: posição inicial A não encontrada.")
        if goal is None:
            raise ValueError("Mapa inválido: objetivo B não encontrado.")

        return cls(grid=grid, start=start, goal=goal, collections=collections)

    @property
    def rows(self) -> int:
        """
        Retorna a quantidade de linhas do labirinto.
        """
        return len(self.grid)

    @property
    def cols(self) -> int:
        """
        Retorna a quantidade de colunas do labirinto.
        """
        return len(self.grid[0]) if self.grid else 0

    def in_bounds(self, pos: Position) -> bool:
        """
        Verifica se uma posição está dentro dos limites do mapa.

        Isso evita tentar acessar uma linha ou coluna inexistente.
        """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_wall(self, pos: Position) -> bool:
        """
        Verifica se uma posição é parede.

        Parede é representada pelo caractere '#'.
        """
        r, c = pos
        return self.grid[r][c] == "#"

    def is_walkable(self, pos: Position) -> bool:
        """
        Verifica se o agente pode andar para uma posição.

        Uma posição é caminhável quando:
        1. está dentro do mapa;
        2. não é parede.

        A, B, C e espaços são considerados caminháveis.
        """
        return self.in_bounds(pos) and not self.is_wall(pos)

    def neighbors(self, pos: Position) -> List[Position]:
        """
        Retorna os vizinhos válidos de uma posição.

        Como o trabalho define movimentos ortogonais, o agente pode ir para:
        - cima;
        - baixo;
        - esquerda;
        - direita.

        Movimentos diagonais não são permitidos.
        """
        r, c = pos

        # Candidatos antes de validar parede/limite.
        candidates = [
            (r - 1, c),  # cima
            (r + 1, c),  # baixo
            (r, c - 1),  # esquerda
            (r, c + 1),  # direita
        ]

        # Filtra apenas posições caminháveis.
        return [p for p in candidates if self.is_walkable(p)]

    def movement_cost(self, current: Position, next_pos: Position) -> int:
        """
        Custo de movimento entre duas células vizinhas.

        Neste trabalho, foi usado custo unitário:
        cada passo custa 1.

        Isso simplifica a comparação entre BFS, UCS e A*.
        """
        return 1

    def copy_grid(self) -> List[List[str]]:
        """
        Retorna uma cópia da matriz do mapa.

        Isso é usado nas visualizações para desenhar caminhos sem alterar
        o mapa original.
        """
        return [row[:] for row in self.grid]
