# CSI457 – Inteligência Artificial
# Trabalho Prático 2 – Agentes Inteligentes para Jogos

## Integrantes

- Ana Flávia
- Eduarda Gomes
- Thiago Augusto
- Luccas Carneiro – 20.1.8015

---

# Descrição

Este projeto consiste na evolução da Inteligência Artificial dos bots do jogo **Mega Arena Royale**, desenvolvido originalmente pelo professor Tiago Linhares Medeiros.

O objetivo foi aplicar conceitos estudados na disciplina de Inteligência Artificial para tornar o comportamento dos bots progressivamente mais inteligente conforme o aumento do nível de dificuldade.

As melhorias implementadas utilizam técnicas clássicas de busca heurística, busca online e cooperação entre agentes.

---

# Objetivos

O projeto possui cinco níveis de inteligência artificial.

Cada nível adiciona novas capacidades aos bots, permitindo uma evolução gradual do comportamento durante o jogo.

| Nível | Inteligência aplicada |
|-------|------------------------|
| 1 | Busca Gulosa para localizar o item mais próximo |
| 2 | Busca Gulosa com desvio de obstáculos |
| 3 | Busca A* para navegação até caixas, armas e inimigos |
| 4 | Busca Online (A*) com construção gradual do mapa e replanejamento |
| 5 | Cooperação entre bots, comunicação e estratégia em grupo |

---

# Técnicas de IA Utilizadas

## Busca Gulosa

Utilizada nos primeiros níveis.

O bot seleciona o objetivo aparentemente mais próximo utilizando apenas uma heurística de distância.

Vantagens:

- baixo custo computacional;
- decisões rápidas;
- comportamento simples.

---

## Busca A*

Utilizada nos níveis intermediários.

O algoritmo considera simultaneamente:

- custo já percorrido;
- estimativa até o objetivo.

Produz caminhos significativamente melhores que a Busca Gulosa.

Foi utilizada para:

- localizar caixas;
- perseguir jogadores;
- alcançar armas;
- movimentação pela arena.

---

## Busca Online

Nos níveis avançados os bots deixam de conhecer completamente o mapa.

Cada agente:

- explora a arena;
- constrói seu próprio mapa interno;
- recalcula rotas sempre que novas informações são descobertas.

Essa estratégia torna o comportamento adaptativo.

---

## Cooperação entre Agentes

No nível máximo os bots passam a compartilhar informações.

São implementadas estratégias como:

- comunicação entre bots;
- compartilhamento de posições dos jogadores;
- compartilhamento de regiões exploradas;
- coordenação dos ataques;
- utilização de cobertura durante os confrontos.

---

# Organização do Projeto

Todo o projeto permanece concentrado em um único arquivo.

```
jogodetiro.html
```

Esse arquivo contém:

- HTML da interface;
- CSS;
- JavaScript;
- lógica do jogo;
- IA dos bots;
- renderização;
- gerenciamento de estados.

---

# Como Executar

Basta abrir o arquivo

```
jogodetiro.html
```

em qualquer navegador moderno.

Não são necessárias instalações adicionais, servidor web ou bibliotecas externas.

---

# Funcionalidades Implementadas

- Arena 2D
- Múltiplos modos de jogo
- Sistema de loja
- Passe de batalha
- Zona segura
- IA baseada em níveis
- Busca Gulosa
- Busca A*
- Busca Online
- Cooperação entre agentes
- Persistência utilizando LocalStorage

---

# Principais Alterações em Relação ao Projeto Original

As seguintes melhorias foram implementadas na IA dos bots:

- comportamento progressivo conforme o nível;
- navegação utilizando algoritmos de busca;
- busca por caixas e itens;
- desvio inteligente de obstáculos;
- replanejamento de caminhos;
- compartilhamento de informações entre agentes;
- movimentação cooperativa;
- utilização estratégica da cobertura.
