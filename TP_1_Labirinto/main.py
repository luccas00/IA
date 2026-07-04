"""
Arquivo principal do projeto.

Responsabilidade deste arquivo:
1. carregar o labirinto;
2. executar os algoritmos de busca clássica;
3. executar os algoritmos de busca local;
4. executar a busca online;
5. salvar métricas em CSV;
6. gerar gráficos;
7. imprimir resultados no terminal.

Observação para apresentação:
Este arquivo funciona como o "orquestrador" do projeto. A lógica pesada dos
algoritmos fica separada nos arquivos da pasta src/.
"""

# Permite que o Python encontre os módulos dentro da pasta src.
# Mantido para facilitar execução direta pelo terminal com: python3 main.py
import sys
sys.path.append("src")

# random é usado na busca local para gerar soluções/vizinhos aleatórios.
import random

# Classe que representa o labirinto carregado do arquivo .txt.
from src.maze import Maze

# Funções responsáveis por salvar as métricas dos experimentos em arquivos CSV.
from src.metrics import save_classic_metrics, save_local_metrics, save_online_metrics

# Executa BFS, DFS, UCS, Gulosa e A* de uma vez.
from src.search_classic import run_all_classic

# Executa Hill-Climbing ou Simulated Annealing várias vezes e consolida métricas.
from src.search_local import evaluate_local_search

# Executa a estratégia online escolhida: replanning com A*.
from src.search_online import online_replanning_a_star

# Funções de visualização: imagens, gráficos e impressão no terminal.
from src.visualization import draw_path, draw_convergence, draw_online_path, print_path_on_terminal


def main():
    """
    Função principal do programa.

    A execução foi organizada em três blocos, seguindo a divisão do trabalho:

    1. Busca clássica:
       O agente conhece o mapa completo e precisa ir de A até B.

    2. Busca local:
       O agente precisa visitar os pontos C em alguma ordem antes de chegar em B.

    3. Busca online:
       O agente não conhece o mapa completo. Ele percebe, atualiza o mapa interno,
       replaneja e anda passo a passo.
    """

    # Define uma semente fixa para os algoritmos aleatórios.
    # Isso torna os resultados mais reproduzíveis:
    # se executar novamente, tende a gerar os mesmos valores.
    random.seed(42)

    # Carrega o mapa a partir do arquivo texto.
    #
    # Para trocar o mapa, basta alterar o caminho abaixo.
    # Exemplo:
    # maze = Maze.from_file("maps/outro_mapa.txt")
    maze = Maze.from_file("maps/mapa2.txt")

    # ==========================================================
    # PARTE 1: BUSCA CLÁSSICA
    # ==========================================================

    print("=== BUSCA CLASSICA ===")

    # Executa todos os algoritmos clássicos obrigatórios:
    # BFS, DFS, UCS, Gulosa e A*.
    classic_results = run_all_classic(maze)

    # Salva as métricas em CSV para atender ao requisito experimental do trabalho.
    save_classic_metrics(classic_results, "results/metricas_classicas.csv")

    # Imprime no terminal um resumo dos resultados.
    # Esses valores ajudam a comparar custo, passos, expansões e tempo.
    for result in classic_results:
        print(
            f"{result.algorithm}: sucesso={result.success}, "
            f"custo={result.cost}, passos={result.steps}, "
            f"expandidos={result.expanded}, tempo={result.elapsed:.8f}s"
        )

    # Seleciona o resultado do A* para visualização.
    # O A* foi escolhido porque combina custo acumulado e heurística,
    # sendo uma boa referência para mostrar o caminho encontrado.
    best_classic = next(result for result in classic_results if result.algorithm == "A*")

    # Gera uma imagem do labirinto com:
    # "." representando nós visitados/expandidos;
    # "*" representando o caminho final encontrado.
    draw_path(
        maze,
        best_classic.path,
        best_classic.visited_order,
        "Caminho encontrado pelo A*",
        "results/graficos/caminho_astar.png"
    )

    # Também imprime o caminho no terminal para visualização simples.
    print("\nMapa com caminho A*:")
    print_path_on_terminal(maze, best_classic.path)

    # ==========================================================
    # PARTE 2: BUSCA LOCAL COM PONTOS DE COLETA
    # ==========================================================

    print("\n=== BUSCA LOCAL ===")

    # Executa os dois métodos obrigatórios de busca local.
    #
    # Cada algoritmo roda 10 vezes porque busca local envolve aleatoriedade.
    # Rodar múltiplas vezes permite calcular melhor custo, pior custo,
    # custo médio, tempo médio e taxa de sucesso.
    local_results = [
        evaluate_local_search(maze, "Hill-Climbing", runs=10),
        evaluate_local_search(maze, "Simulated Annealing", runs=10)
    ]

    # Salva as métricas da busca local em CSV.
    save_local_metrics(local_results, "results/metricas_busca_local.csv")

    # Imprime resumo dos resultados de busca local.
    for result in local_results:
        print(
            f"{result.algorithm}: melhor_custo={result.best_cost}, "
            f"custo_medio={result.average_cost:.2f}, "
            f"taxa_sucesso={result.success_rate:.2f}"
        )

        # Cria um nome de arquivo simples baseado no nome do algoritmo.
        # Exemplo:
        # "Hill-Climbing" vira "hill_climbing".
        filename = result.algorithm.lower().replace(" ", "_").replace("-", "_")

        # Gera o gráfico de convergência: iteração x melhor custo.
        # Esse gráfico é exigido na especificação do trabalho.
        draw_convergence(
            result.convergence,
            f"Convergência - {result.algorithm}",
            f"results/graficos/convergencia_{filename}.png"
        )

    # ==========================================================
    # PARTE 3: BUSCA ONLINE
    # ==========================================================

    print("\n=== BUSCA ONLINE ===")

    # Executa a busca online com replanning A*.
    #
    # Ideia:
    # - o simulador tem o mapa real;
    # - o agente começa com mapa interno desconhecido;
    # - a cada passo, percebe a vizinhança, atualiza o mapa e replaneja.
    online_result = online_replanning_a_star(maze)

    # Salva as métricas da busca online em CSV.
    save_online_metrics(online_result, "results/metricas_online.csv")

    # Imprime métricas principais da busca online.
    print(
        f"Online A*: sucesso={online_result.success}, "
        f"movimentos={online_result.movements}, "
        f"replanejamentos={online_result.replans}, "
        f"razao={online_result.ratio_online_offline:.4f}"
    )

    # Gera imagem da trajetória percorrida pelo agente online.
    draw_online_path(
        maze,
        online_result.path,
        "Trajetória online com replanning A*",
        "results/graficos/trajetoria_online.png"
    )

    print("\nArquivos gerados na pasta results/.")


# Este bloco garante que main() será chamado apenas quando o arquivo
# for executado diretamente.
#
# Se este arquivo for importado por outro módulo, main() não roda automaticamente.
if __name__ == "__main__":
    main()
