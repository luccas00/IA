# CSI701 – Inteligência Artificial
# Trabalho Prático 2 – Agentes Inteligentes para Jogos

## Integrantes

- Ana Flávia
- Eduarda Gomes
- Thiago Augusto
- Luccas Carneiro

---

# Descrição

Este projeto consiste na evolução da Inteligência Artificial dos bots do jogo **Mega Arena Royale**, desenvolvido originalmente pelo professor Tiago Linhares Medeiros.

O objetivo foi aplicar conceitos estudados na disciplina de Inteligência Artificial para tornar o comportamento dos bots progressivamente mais inteligente conforme o aumento do nível de dificuldade.

Diferentemente do projeto original, onde a dificuldade alterava principalmente atributos como velocidade e tempo entre disparos, esta versão implementa diferentes estratégias de tomada de decisão para cada nível de IA.

Além disso, todos os bots passam a possuir percepção parcial do ambiente, descobrindo o mapa gradualmente durante a partida.

---

# Objetivos

Implementar uma evolução progressiva da inteligência dos agentes, permitindo que cada nível apresente um comportamento mais sofisticado que o anterior.

| Nível | Inteligência aplicada |
|-------|------------------------|
| 1 | Busca Gulosa e percepção limitada do ambiente |
| 2 | Busca Gulosa com desvio simples de obstáculos |
| 3 | Busca A* para navegação inteligente |
| 4 | Busca Online (A*) com exploração do mapa e compartilhamento parcial |
| 5 | Cooperação entre bots, cobertura e estratégia em grupo |

---

# Técnicas de IA Utilizadas

## Busca Gulosa

Nos primeiros níveis, os bots utilizam Busca Gulosa para selecionar rapidamente o objetivo mais promissor.

As decisões são tomadas considerando apenas uma heurística de distância, produzindo comportamento simples e baixo custo computacional.

Foi utilizada para:

- localizar caixas próximas;
- localizar melhorias;
- perseguir jogadores.

---

## Busca A*

A partir do nível 3 os bots passam a utilizar o algoritmo A*.

O algoritmo considera simultaneamente:

- custo já percorrido;
- estimativa até o objetivo.

Isso produz caminhos significativamente melhores do que a Busca Gulosa.

O A* foi utilizado para:

- navegar entre obstáculos;
- localizar caixas;
- perseguir jogadores;
- movimentação inteligente pela arena.

---

## Busca Online

A partir do nível 4 os bots deixam de utilizar conhecimento completo do mapa.

Cada agente passa a:

- explorar a arena;
- descobrir novas regiões;
- construir seu próprio mapa interno;
- recalcular rotas conforme novas informações são obtidas.

Quanto maior o nível, maior também é o raio de percepção do ambiente, permitindo que bots mais avançados reconheçam o cenário com maior rapidez.

---

## Cooperação entre Agentes

No nível máximo os bots passam a atuar de forma cooperativa.

São implementadas estratégias como:

- compartilhamento das regiões exploradas;
- compartilhamento de obstáculos descobertos;
- compartilhamento da última posição conhecida do jogador;
- coordenação durante perseguições;
- utilização de cobertura durante confrontos;
- movimentação em flanco para cercar o jogador.

---

# Evolução da Inteligência

Cada nível adiciona novas capacidades aos bots.

| Nível | Comportamento |
|--------|---------------|
| 1 | Busca Gulosa e exploração inicial do mapa |
| 2 | Busca Gulosa com desvio simples de obstáculos |
| 3 | Navegação utilizando A* |
| 4 | Busca Online com construção do mapa e compartilhamento parcial |
| 5 | Cooperação entre bots, flanqueamento e utilização de cobertura |

Além da evolução da IA, os níveis continuam aumentando a velocidade dos bots e reduzindo o intervalo entre disparos, preservando a mecânica original do jogo.

---

# Organização do Projeto

O projeto foi reorganizado em três arquivos.

```
index.html
styles.css
game.js
```

### index.html

Contém:

- estrutura da interface;
- HUD;
- menus;
- canvas do jogo.

### styles.css

Contém:

- toda a identidade visual;
- HUD;
- animações;
- menus;
- responsividade.

### game.js

Contém toda a lógica do jogo:

- renderização;
- física;
- movimentação;
- sistema de combate;
- gerenciamento da arena;
- IA dos bots;
- algoritmos de busca;
- persistência utilizando LocalStorage.

---

# Como Executar

Basta abrir

```
index.html
```

em qualquer navegador moderno.

Não é necessário instalar bibliotecas, frameworks ou executar servidor local.

---

# Funcionalidades Implementadas

- Arena 2D
- Sistema de batalha
- Loja
- Passe de batalha
- Zona segura
- Boss Fight
- Persistência utilizando LocalStorage
- Busca Gulosa
- Busca A*
- Busca Online
- Cooperação entre agentes
- Compartilhamento de informações
- Utilização de cobertura
- Flanqueamento
- Percepção parcial do ambiente
- Evolução progressiva da IA

---

# Principais Alterações em Relação ao Projeto Original

As seguintes melhorias foram implementadas:

- separação do projeto em HTML, CSS e JavaScript;
- implementação de diferentes algoritmos de IA por nível;
- utilização de Busca Gulosa;
- implementação do algoritmo A*;
- implementação de Busca Online;
- exploração gradual da arena;
- percepção parcial do ambiente;
- construção de mapa interno pelos agentes;
- compartilhamento de informações entre bots;
- compartilhamento de obstáculos descobertos;
- compartilhamento da última posição conhecida do jogador;
- movimentação cooperativa;
- utilização de cobertura;
- flanqueamento durante confrontos;
- melhoria da navegação entre obstáculos;
- prevenção de travamentos entre bots;
- replanejamento automático de rotas.

---

# Tecnologias Utilizadas

- HTML5
- CSS3
- JavaScript (ES6)
- Canvas 2D
- LocalStorage

---

# Conceitos de Inteligência Artificial Aplicados

- Agentes Inteligentes
- Busca Gulosa
- Busca Heurística
- Algoritmo A*
- Busca Online
- Planejamento de Caminhos
- Replanejamento
- Cooperação entre Agentes
- Compartilhamento de Conhecimento
- Percepção Parcial do Ambiente
