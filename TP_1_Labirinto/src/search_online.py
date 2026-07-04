"""
Módulo de busca online.

Atenção:
"Online" aqui NÃO significa internet.

No contexto de IA, busca online significa que o agente não conhece o mapa
completo antes de agir. Ele precisa descobrir o ambiente enquanto se move.

Estratégia implementada:
    Replanning com A*

Ciclo do agente:
    perceber -> atualizar mapa interno -> planejar -> agir

No simulador:
- o mapa real existe;
- mas o agente só acessa a vizinhança local por percepção.
"""

from dataclasses import dataclass
from typing import List, Optional

from maze import Maze, Position
from search_classic import a_star, manhattan


@dataclass
class OnlineResult:
    """
    Resultado final da busca online.

    Campos principais:
    - success: se chegou ao objetivo;
    - path: trajetória real percorrida;
    - movements: quantidade de movimentos;
    - revealed_cells: células descobertas;
    - replans: quantas vezes o agente replanejou;
    - offline_cost: custo ótimo com mapa completo;
    - ratio_online_offline: comparação entre online e offline.
    """

    success: bool
    path: List[Position]
    movements: int
    real_cost: int
    revealed_cells: int
    revisited_cells: int
    replans: int
    offline_cost: int
    ratio_online_offline: float


class OnlineKnownMaze:
    """
    Representa o mapa interno do agente.

    O agente online não começa conhecendo o mapa completo.
    Portanto, o mapa interno começa preenchido com '?'.

    Símbolos:
    - #: parede conhecida;
    - espaço/A/B/C: célula conhecida e caminhável;
    - ?: célula desconhecida.

    Decisão de projeto:
    Durante o planejamento, células desconhecidas são tratadas como transitáveis.
    Se o agente tentar ir para uma célula e descobrir que é parede, ele marca
    como parede e replaneja.
    """

    def __init__(self, real_maze: Maze, internal_grid: List[List[str]]):
        self.real_maze = real_maze
        self.grid = internal_grid

        # Mantemos os mesmos pontos principais do mapa real.
        # Isso facilita reaproveitar a função A*.
        self.start = real_maze.start
        self.goal = real_maze.goal
        self.collections = real_maze.collections

    @property
    def rows(self):
        return self.real_maze.rows

    @property
    def cols(self):
        return self.real_maze.cols

    def in_bounds(self, pos: Position) -> bool:
        """
        Verifica se a posição está dentro do mapa.
        """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, pos: Position) -> bool:
        """
        Verifica se o agente pode planejar passar por uma célula.

        No mapa interno:
        - parede conhecida (#) não é caminhável;
        - desconhecido (?) é tratado como possível caminho;
        - células livres conhecidas também são caminháveis.
        """
        if not self.in_bounds(pos):
            return False

        r, c = pos
        return self.grid[r][c] != "#"

    def neighbors(self, pos: Position) -> List[Position]:
        """
        Retorna vizinhos válidos no mapa interno conhecido pelo agente.
        """
        r, c = pos
        candidates = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]

        return [p for p in candidates if self.is_walkable(p)]

    def movement_cost(self, current: Position, next_pos: Position) -> int:
        """
        Custo unitário por movimento.
        """
        return 1


def perceive(real_maze: Maze, internal_grid: List[List[str]], position: Position, radius: int = 1) -> int:
    """
    Simula a percepção local do agente.

    O agente está em uma posição e percebe:
    - a própria célula;
    - cima;
    - baixo;
    - esquerda;
    - direita.

    Com radius=1, isso representa exatamente uma vizinhança ortogonal simples.

    A função retorna quantas novas células foram reveladas.
    """

    # Conta quantas células já eram conhecidas antes da percepção.
    revealed_before = sum(1 for row in internal_grid for cell in row if cell != "?")

    r, c = position

    # A própria posição sempre é percebida.
    cells = [(r, c)]

    # Adiciona vizinhos dentro do raio definido.
    for dist in range(1, radius + 1):
        cells.extend([
            (r - dist, c),
            (r + dist, c),
            (r, c - dist),
            (r, c + dist),
        ])

    # Copia do mapa real para o mapa interno apenas as células percebidas.
    for cell in cells:
        if real_maze.in_bounds(cell):
            rr, cc = cell
            internal_grid[rr][cc] = real_maze.grid[rr][cc]

    # Conta depois da percepção para medir quantas foram reveladas agora.
    revealed_after = sum(1 for row in internal_grid for cell in row if cell != "?")

    return revealed_after - revealed_before


def nearest_known_frontier(internal_grid: List[List[str]], start: Position) -> Optional[Position]:
    """
    Encontra uma fronteira conhecida próxima.

    Fronteira:
    uma célula conhecida e caminhável que possui pelo menos um vizinho desconhecido.

    Isso é usado como plano alternativo quando o agente ainda não consegue
    planejar diretamente até o objetivo.
    """

    rows = len(internal_grid)
    cols = len(internal_grid[0])
    frontier = []

    for r in range(rows):
        for c in range(cols):
            # Ignora células desconhecidas.
            if internal_grid[r][c] == "?":
                continue

            # Ignora paredes.
            if internal_grid[r][c] == "#":
                continue

            neighbors = [
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1),
            ]

            has_unknown_neighbor = any(
                0 <= nr < rows and 0 <= nc < cols and internal_grid[nr][nc] == "?"
                for nr, nc in neighbors
            )

            if has_unknown_neighbor:
                frontier.append((r, c))

    if not frontier:
        return None

    # Escolhe a fronteira mais próxima pela distância de Manhattan.
    frontier.sort(key=lambda p: manhattan(start, p))
    return frontier[0]


def online_replanning_a_star(real_maze: Maze, max_steps: int = 1000, perception_radius: int = 1) -> OnlineResult:
    """
    Executa busca online usando replanning com A*.

    Fluxo:
    1. cria um mapa interno totalmente desconhecido;
    2. agente começa em A;
    3. percebe vizinhança;
    4. atualiza mapa interno;
    5. roda A* no mapa interno;
    6. executa apenas o próximo passo;
    7. repete até chegar em B ou atingir limite de passos.

    Ponto para apresentação:
    O mapa real é usado pelo simulador, mas o agente só atualiza seu modelo
    por percepção local.
    """

    # Mapa interno começa totalmente desconhecido.
    internal_grid = [["?" for _ in range(real_maze.cols)] for _ in range(real_maze.rows)]

    position = real_maze.start
    path_taken = [position]

    # Guarda quantas vezes cada célula foi visitada.
    # Isso permite calcular células revisitadas.
    visited_count = {position: 1}

    replans = 0
    revealed = 0

    # Calcula o custo ótimo offline com A* no mapa completo.
    # Isso é usado para comparar online/offline.
    offline = a_star(real_maze)
    offline_cost = int(offline.cost) if offline.success else 0

    for _ in range(max_steps):
        # O agente percebe a vizinhança atual.
        revealed += perceive(real_maze, internal_grid, position, perception_radius)

        # Se chegou no objetivo, encerra com sucesso.
        if position == real_maze.goal:
            revisited = sum(1 for count in visited_count.values() if count > 1)

            ratio = len(path_taken) - 1
            ratio = ratio / offline_cost if offline_cost > 0 else float("inf")

            return OnlineResult(
                True,
                path_taken,
                len(path_taken) - 1,
                len(path_taken) - 1,
                revealed,
                revisited,
                replans,
                offline_cost,
                ratio,
            )

        # Cria uma visão do labirinto baseada no mapa interno do agente.
        known_maze = OnlineKnownMaze(real_maze, internal_grid)

        # Planeja um caminho até o objetivo usando o conhecimento atual.
        plan = a_star(known_maze, position, real_maze.goal)
        replans += 1

        # Se ainda não for possível chegar ao objetivo,
        # tenta ir até uma fronteira conhecida para explorar mais.
        if not plan.success or len(plan.path) < 2:
            frontier = nearest_known_frontier(internal_grid, position)

            if frontier is None:
                break

            plan = a_star(known_maze, position, frontier)
            replans += 1

            if not plan.success or len(plan.path) < 2:
                break

        # O agente executa apenas o próximo passo do plano.
        # Esse é o ponto central do replanning.
        next_position = plan.path[1]

        # Antes de mover, o simulador verifica no mapa real se a célula é parede.
        # Se for parede, o agente marca no mapa interno e replaneja.
        if not real_maze.is_walkable(next_position):
            rr, cc = next_position
            internal_grid[rr][cc] = "#"
            continue

        # Movimento efetivo do agente.
        position = next_position
        path_taken.append(position)
        visited_count[position] = visited_count.get(position, 0) + 1

    # Se saiu do loop sem chegar ao objetivo, retorna falha.
    revisited = sum(1 for count in visited_count.values() if count > 1)
    ratio = (len(path_taken) - 1) / offline_cost if offline_cost > 0 else float("inf")

    return OnlineResult(
        False,
        path_taken,
        len(path_taken) - 1,
        len(path_taken) - 1,
        revealed,
        revisited,
        replans,
        offline_cost,
        ratio,
    )
