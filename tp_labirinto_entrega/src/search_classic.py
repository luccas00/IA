"""
Módulo de busca clássica.

Aqui estão os algoritmos obrigatórios da Parte II do trabalho:

1. BFS - Busca em Largura;
2. DFS - Busca em Profundidade;
3. UCS - Busca de Custo Uniforme;
4. Busca Gulosa;
5. A*.

Todos recebem um Maze e retornam um SearchResult com:
- sucesso ou falha;
- caminho encontrado;
- custo;
- passos;
- nós explorados/expandidos;
- tempo;
- tamanho máximo da fronteira.

Na apresentação:
Diga que este módulo resolve o cenário em que o agente conhece o mapa inteiro.
"""

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from time import perf_counter
from typing import Dict, List, Optional

from maze import Maze, Position


@dataclass
class SearchResult:
    """
    Estrutura padrão de retorno para todos os algoritmos de busca clássica.

    Isso facilita comparar algoritmos, porque todos retornam os mesmos campos.
    """

    algorithm: str
    success: bool
    path: List[Position]
    cost: float
    steps: int
    explored: int
    expanded: int
    elapsed: float
    max_frontier: int
    visited_order: List[Position]


def manhattan(a: Position, b: Position) -> int:
    """
    Calcula a distância de Manhattan entre duas posições.

    Fórmula:
        |x1 - x2| + |y1 - y2|

    Por que Manhattan?
    Porque o agente só anda em quatro direções:
    cima, baixo, esquerda e direita.

    Essa heurística é admissível no nosso cenário, pois não superestima
    a distância real mínima até o objetivo.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(parent: Dict[Position, Optional[Position]], goal: Position) -> List[Position]:
    """
    Reconstrói o caminho final a partir do dicionário de pais.

    Durante a busca, quando visitamos um vizinho, salvamos de onde ele veio.
    Exemplo:
        parent[(2, 3)] = (2, 2)

    Quando encontramos o objetivo, voltamos do objetivo até o início,
    seguindo esses pais.

    Depois invertemos o caminho para ficar:
        início -> objetivo
    """

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def path_cost(maze: Maze, path: List[Position]) -> int:
    """
    Calcula o custo de um caminho.

    Como cada movimento custa 1, o custo é:
        quantidade de posições no caminho - 1

    Exemplo:
        [A, x, y, B] tem 4 posições e 3 movimentos.
    """
    if not path:
        return 0
    return max(0, len(path) - 1)


def bfs(maze: Maze, start: Position = None, goal: Position = None) -> SearchResult:
    """
    Busca em Largura (BFS).

    Ideia:
    Explora primeiro todos os estados mais próximos do início.
    Usa uma fila FIFO:
    - primeiro que entra;
    - primeiro que sai.

    Vantagem:
    Com custo unitário, garante o menor caminho em número de passos.

    Limitação:
    Pode expandir muitos nós.
    """

    start = start or maze.start
    goal = goal or maze.goal

    begin = perf_counter()

    # Fila da fronteira.
    # A fronteira guarda os nós descobertos, mas ainda não expandidos.
    frontier = deque([start])

    # parent guarda o caminho:
    # para cada posição, quem foi seu antecessor.
    parent = {start: None}

    explored_set = set()
    visited_order = []

    expanded = 0
    max_frontier = 1

    while frontier:
        # BFS remove da esquerda da fila.
        current = frontier.popleft()
        visited_order.append(current)

        # Teste de objetivo.
        if current == goal:
            elapsed = perf_counter() - begin
            path = reconstruct_path(parent, goal)

            return SearchResult(
                "BFS",
                True,
                path,
                path_cost(maze, path),
                len(path) - 1,
                len(explored_set),
                expanded,
                elapsed,
                max_frontier,
                visited_order,
            )

        explored_set.add(current)
        expanded += 1

        # Expande os vizinhos válidos.
        for neighbor in maze.neighbors(current):
            # Se o vizinho ainda não tem pai, ele ainda não foi descoberto.
            if neighbor not in parent:
                parent[neighbor] = current
                frontier.append(neighbor)

        max_frontier = max(max_frontier, len(frontier))

    elapsed = perf_counter() - begin

    return SearchResult(
        "BFS",
        False,
        [],
        float("inf"),
        0,
        len(explored_set),
        expanded,
        elapsed,
        max_frontier,
        visited_order,
    )


def dfs(maze: Maze, start: Position = None, goal: Position = None) -> SearchResult:
    """
    Busca em Profundidade (DFS).

    Ideia:
    Explora um caminho até o fundo antes de tentar alternativas.

    Usa pilha LIFO:
    - último que entra;
    - primeiro que sai.

    Vantagem:
    Pode encontrar uma solução rapidamente.

    Limitação:
    Não garante o menor caminho.
    """

    start = start or maze.start
    goal = goal or maze.goal

    begin = perf_counter()

    # Pilha da DFS.
    frontier = [start]

    parent = {start: None}
    explored_set = set()
    visited_order = []

    expanded = 0
    max_frontier = 1

    while frontier:
        # DFS remove do final da lista.
        current = frontier.pop()
        visited_order.append(current)

        if current == goal:
            elapsed = perf_counter() - begin
            path = reconstruct_path(parent, goal)

            return SearchResult(
                "DFS",
                True,
                path,
                path_cost(maze, path),
                len(path) - 1,
                len(explored_set),
                expanded,
                elapsed,
                max_frontier,
                visited_order,
            )

        if current in explored_set:
            continue

        explored_set.add(current)
        expanded += 1

        # reversed é usado para manter uma ordem de exploração mais estável
        # em relação aos vizinhos retornados pelo Maze.
        for neighbor in reversed(maze.neighbors(current)):
            if neighbor not in explored_set and neighbor not in parent:
                parent[neighbor] = current
                frontier.append(neighbor)

        max_frontier = max(max_frontier, len(frontier))

    elapsed = perf_counter() - begin

    return SearchResult(
        "DFS",
        False,
        [],
        float("inf"),
        0,
        len(explored_set),
        expanded,
        elapsed,
        max_frontier,
        visited_order,
    )


def uniform_cost_search(maze: Maze, start: Position = None, goal: Position = None) -> SearchResult:
    """
    Busca de Custo Uniforme (UCS).

    Ideia:
    Sempre expande o caminho com menor custo acumulado.

    Usa fila de prioridade:
    - prioridade = custo acumulado até o nó.

    Quando todos os movimentos custam 1, UCS se comporta de forma parecida
    com BFS. Porém, se os custos variassem, UCS seria mais adequada.
    """

    start = start or maze.start
    goal = goal or maze.goal

    begin = perf_counter()

    frontier = []

    # heapq implementa uma fila de prioridade.
    # Cada item é uma tupla: (prioridade, posição)
    heappush(frontier, (0, start))

    parent = {start: None}
    best_cost = {start: 0}
    explored_set = set()
    visited_order = []

    expanded = 0
    max_frontier = 1

    while frontier:
        current_cost, current = heappop(frontier)

        if current in explored_set:
            continue

        visited_order.append(current)

        if current == goal:
            elapsed = perf_counter() - begin
            path = reconstruct_path(parent, goal)

            return SearchResult(
                "UCS",
                True,
                path,
                current_cost,
                len(path) - 1,
                len(explored_set),
                expanded,
                elapsed,
                max_frontier,
                visited_order,
            )

        explored_set.add(current)
        expanded += 1

        for neighbor in maze.neighbors(current):
            new_cost = current_cost + maze.movement_cost(current, neighbor)

            # Atualiza o melhor custo conhecido até o vizinho.
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                parent[neighbor] = current
                heappush(frontier, (new_cost, neighbor))

        max_frontier = max(max_frontier, len(frontier))

    elapsed = perf_counter() - begin

    return SearchResult(
        "UCS",
        False,
        [],
        float("inf"),
        0,
        len(explored_set),
        expanded,
        elapsed,
        max_frontier,
        visited_order,
    )


def greedy_best_first_search(maze: Maze, start: Position = None, goal: Position = None) -> SearchResult:
    """
    Busca Gulosa.

    Ideia:
    Escolhe o próximo nó que parece mais perto do objetivo.

    Prioridade:
        h(n)

    Ou seja:
    Usa somente a heurística, ignorando o custo já percorrido.

    Vantagem:
    Normalmente expande poucos nós.

    Limitação:
    Não garante caminho ótimo, porque pode escolher uma rota aparentemente
    boa, mas que depois fica bloqueada ou alonga o caminho.
    """

    start = start or maze.start
    goal = goal or maze.goal

    begin = perf_counter()

    frontier = []
    heappush(frontier, (manhattan(start, goal), start))

    parent = {start: None}
    explored_set = set()
    visited_order = []

    expanded = 0
    max_frontier = 1

    while frontier:
        _, current = heappop(frontier)

        if current in explored_set:
            continue

        visited_order.append(current)

        if current == goal:
            elapsed = perf_counter() - begin
            path = reconstruct_path(parent, goal)

            return SearchResult(
                "Gulosa",
                True,
                path,
                path_cost(maze, path),
                len(path) - 1,
                len(explored_set),
                expanded,
                elapsed,
                max_frontier,
                visited_order,
            )

        explored_set.add(current)
        expanded += 1

        for neighbor in maze.neighbors(current):
            if neighbor not in explored_set and neighbor not in parent:
                parent[neighbor] = current

                # Prioridade gulosa:
                # quanto menor a distância de Manhattan até o objetivo,
                # maior a prioridade.
                heappush(frontier, (manhattan(neighbor, goal), neighbor))

        max_frontier = max(max_frontier, len(frontier))

    elapsed = perf_counter() - begin

    return SearchResult(
        "Gulosa",
        False,
        [],
        float("inf"),
        0,
        len(explored_set),
        expanded,
        elapsed,
        max_frontier,
        visited_order,
    )


def a_star(maze: Maze, start: Position = None, goal: Position = None) -> SearchResult:
    """
    Algoritmo A*.

    Ideia:
    Combina custo real já percorrido com uma estimativa do custo restante.

    Fórmula:
        f(n) = g(n) + h(n)

    Onde:
    - g(n): custo acumulado do início até n;
    - h(n): heurística estimada de n até o objetivo.

    Neste projeto:
    - g(n) = quantidade de passos até o nó;
    - h(n) = distância de Manhattan.

    Vantagem:
    Com heurística admissível, encontra solução ótima e tende a expandir
    menos nós que BFS/UCS.
    """

    start = start or maze.start
    goal = goal or maze.goal

    begin = perf_counter()

    frontier = []

    # Tupla usada na fila de prioridade:
    # (prioridade f, custo acumulado g, posição)
    heappush(frontier, (manhattan(start, goal), 0, start))

    parent = {start: None}
    best_cost = {start: 0}
    explored_set = set()
    visited_order = []

    expanded = 0
    max_frontier = 1

    while frontier:
        _, current_cost, current = heappop(frontier)

        if current in explored_set:
            continue

        visited_order.append(current)

        if current == goal:
            elapsed = perf_counter() - begin
            path = reconstruct_path(parent, goal)

            return SearchResult(
                "A*",
                True,
                path,
                current_cost,
                len(path) - 1,
                len(explored_set),
                expanded,
                elapsed,
                max_frontier,
                visited_order,
            )

        explored_set.add(current)
        expanded += 1

        for neighbor in maze.neighbors(current):
            new_cost = current_cost + maze.movement_cost(current, neighbor)

            # Se encontramos um caminho melhor até o vizinho,
            # atualizamos o custo e o pai dele.
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                parent[neighbor] = current

                # Prioridade do A*:
                # custo real já percorrido + estimativa até o objetivo.
                priority = new_cost + manhattan(neighbor, goal)

                heappush(frontier, (priority, new_cost, neighbor))

        max_frontier = max(max_frontier, len(frontier))

    elapsed = perf_counter() - begin

    return SearchResult(
        "A*",
        False,
        [],
        float("inf"),
        0,
        len(explored_set),
        expanded,
        elapsed,
        max_frontier,
        visited_order,
    )


def run_all_classic(maze: Maze) -> List[SearchResult]:
    """
    Executa todos os algoritmos clássicos obrigatórios.

    Isso centraliza a chamada dos algoritmos e mantém o main.py mais limpo.
    """
    return [
        bfs(maze),
        dfs(maze),
        uniform_cost_search(maze),
        greedy_best_first_search(maze),
        a_star(maze),
    ]
