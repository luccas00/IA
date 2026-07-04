"""
Módulo de busca local.

Esta parte resolve o problema com pontos de coleta obrigatórios.

No cenário clássico, o agente precisava apenas:
    A -> B

Na busca local, ele precisa:
    A -> C1 -> C2 -> ... -> B

Mas a ordem dos pontos C pode mudar. Por isso, a solução candidata é uma
permutação/lista com a ordem dos pontos de coleta.

Exemplo:
    [C3, C1, C2]

Significa:
    A -> C3 -> C1 -> C2 -> B

Algoritmos implementados:
1. Hill-Climbing;
2. Simulated Annealing.
"""

import math
import random
from dataclasses import dataclass
from time import perf_counter
from typing import List, Tuple

from maze import Maze, Position
from search_classic import a_star


@dataclass
class LocalSearchResult:
    """
    Resultado consolidado de um algoritmo de busca local.

    Como busca local usa aleatoriedade, executamos várias vezes e guardamos:
    - melhor custo;
    - pior custo;
    - custo médio;
    - tempo médio;
    - média de iterações;
    - taxa de sucesso;
    - curva de convergência.
    """

    algorithm: str
    order: List[Position]
    best_cost: float
    worst_cost: float
    average_cost: float
    average_time: float
    average_iterations: float
    success_rate: float
    convergence: List[float]


def route_cost(maze: Maze, order: List[Position]) -> float:
    """
    Calcula o custo total de uma ordem de visitação.

    Exemplo:
        order = [C2, C1, C3]

    Rota avaliada:
        A -> C2 -> C1 -> C3 -> B

    Para cada trecho, usamos A* para calcular o menor caminho entre os pontos.

    Isso atende à especificação do trabalho, que pede que d(X, Y), ou seja,
    a distância entre dois pontos, seja calculada com A* ou UCS.
    """

    # Monta a sequência completa da rota:
    # início + coletas + objetivo.
    points = [maze.start] + list(order) + [maze.goal]

    total = 0

    # Soma o menor caminho entre cada par consecutivo.
    for i in range(len(points) - 1):
        result = a_star(maze, points[i], points[i + 1])

        # Se algum trecho for impossível, a rota inteira é inválida.
        if not result.success:
            return float("inf")

        total += result.cost

    return total


def random_neighbor(order: List[Position]) -> List[Position]:
    """
    Gera um vizinho da solução atual.

    A vizinhança escolhida foi troca de dois pontos.
    Exemplo:
        [C1, C2, C3] -> [C3, C2, C1]

    Essa escolha é simples, fácil de explicar e suficiente para alterar
    a ordem de visitação dos pontos de coleta.
    """

    neighbor = list(order)

    # Se houver menos de dois pontos, não há troca possível.
    if len(neighbor) < 2:
        return neighbor

    # Escolhe duas posições aleatórias da lista e troca.
    i, j = random.sample(range(len(neighbor)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

    return neighbor


def hill_climbing_once(maze: Maze, max_iterations: int = 200) -> Tuple[List[Position], float, int, List[float]]:
    """
    Executa uma rodada de Hill-Climbing.

    Ideia do Hill-Climbing:
    1. começa com uma solução inicial aleatória;
    2. gera uma solução vizinha;
    3. se o vizinho for melhor, aceita;
    4. se for pior, rejeita;
    5. repete.

    Ponto importante para apresentação:
    Hill-Climbing pode ficar preso em mínimo local porque ele só aceita melhoria.
    """

    # Solução inicial: uma ordem aleatória dos pontos C.
    current = list(maze.collections)
    random.shuffle(current)

    # Custo da solução atual.
    current_cost = route_cost(maze, current)

    # Guarda a evolução do melhor custo para gerar gráfico.
    convergence = [current_cost]

    for iteration in range(max_iterations):
        # Gera uma pequena alteração na ordem atual.
        candidate = random_neighbor(current)
        candidate_cost = route_cost(maze, candidate)

        # Só aceita se melhorar.
        if candidate_cost < current_cost:
            current = candidate
            current_cost = candidate_cost

        convergence.append(current_cost)

    return current, current_cost, max_iterations, convergence


def simulated_annealing_once(
    maze: Maze,
    max_iterations: int = 400,
    initial_temperature: float = 100.0,
    cooling_rate: float = 0.97
) -> Tuple[List[Position], float, int, List[float]]:
    """
    Executa uma rodada de Simulated Annealing.

    Ideia:
    Parecido com Hill-Climbing, mas com uma diferença importante:
    ele pode aceitar uma solução pior em alguns momentos.

    Por quê?
    Para escapar de mínimos locais.

    A chance de aceitar piora depende da temperatura:
    - temperatura alta: mais exploração;
    - temperatura baixa: comportamento mais conservador.

    cooling_rate reduz a temperatura a cada iteração.
    """

    current = list(maze.collections)
    random.shuffle(current)

    current_cost = route_cost(maze, current)

    # best guarda a melhor solução global encontrada até agora.
    best = list(current)
    best_cost = current_cost

    temperature = initial_temperature

    convergence = [best_cost]

    for iteration in range(max_iterations):
        candidate = random_neighbor(current)
        candidate_cost = route_cost(maze, candidate)

        # delta < 0 significa que o candidato é melhor.
        # delta > 0 significa que o candidato é pior.
        delta = candidate_cost - current_cost

        # Critério de aceitação:
        # - se for melhor, aceita;
        # - se for pior, pode aceitar com probabilidade controlada pela temperatura.
        if delta < 0 or random.random() < math.exp(-delta / max(temperature, 0.0001)):
            current = candidate
            current_cost = candidate_cost

        # Atualiza a melhor solução global.
        if current_cost < best_cost:
            best = list(current)
            best_cost = current_cost

        # Resfriamento: reduz a temperatura.
        temperature *= cooling_rate

        convergence.append(best_cost)

    return best, best_cost, max_iterations, convergence


def evaluate_local_search(maze: Maze, algorithm: str, runs: int = 10) -> LocalSearchResult:
    """
    Executa um algoritmo de busca local várias vezes e consolida métricas.

    Por que várias execuções?
    Porque busca local é influenciada por aleatoriedade.
    Uma execução isolada pode não representar bem o comportamento do algoritmo.
    """

    costs = []
    times = []
    iterations = []

    best_order = []
    best_cost = float("inf")
    worst_cost = 0
    best_convergence = []

    # Define um limite aceitável para calcular taxa de sucesso.
    # Aqui consideramos aceitável uma solução até 20% pior que a rota original.
    acceptable_limit = route_cost(maze, maze.collections) * 1.20

    for _ in range(runs):
        begin = perf_counter()

        if algorithm == "Hill-Climbing":
            order, cost, iters, convergence = hill_climbing_once(maze)
        elif algorithm == "Simulated Annealing":
            order, cost, iters, convergence = simulated_annealing_once(maze)
        else:
            raise ValueError("Algoritmo de busca local inválido.")

        elapsed = perf_counter() - begin

        costs.append(cost)
        times.append(elapsed)
        iterations.append(iters)

        # Guarda a melhor execução.
        if cost < best_cost:
            best_cost = cost
            best_order = order
            best_convergence = convergence

        worst_cost = max(worst_cost, cost)

    success_count = sum(1 for c in costs if c <= acceptable_limit)

    return LocalSearchResult(
        algorithm=algorithm,
        order=best_order,
        best_cost=best_cost,
        worst_cost=worst_cost,
        average_cost=sum(costs) / len(costs),
        average_time=sum(times) / len(times),
        average_iterations=sum(iterations) / len(iterations),
        success_rate=success_count / len(costs),
        convergence=best_convergence,
    )
