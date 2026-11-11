# Matriz de rastreabilidade

Cada pergunta do [questionário](questionario.md) existe para responder a uma questão de pesquisa (ou é controle
ou filtro). Nenhuma pergunta "solta". Cadeia: **Objetivo (G) → Questão (QP) → Métrica (M) → Pergunta → Escala → Análise.**

## 1. Objetivo (G)

Analisar o uso de assistentes de IA, com o propósito de entender sua **associação** com a síndrome do impostor
percebida, do ponto de vista de desenvolvedores de software.

> Sugestão ao grupo: usar "associação" no lugar de "impacto". Um survey transversal não sustenta causalidade.

## 2. Métricas (M)

| ID | Métrica | Definição operacional | Tipo / escala | Perguntas |
|---|---|---|---|---|
| M1 | Síndrome do impostor percebida | Média dos 7 itens da Leary Impostorism Scale, versão PT-BR (Silva et al., 2026); faixa 1–5, maior = mais impostor | Ordinal (Likert 5 pontos agregado); tratada como ordinal | C1…C7 |
| M2 | Frequência de uso de IA | Frequência nos últimos 3 meses | Ordinal, 5 níveis (0–4) | B1 |
| M3 | Experiência profissional | Tempo total com desenvolvimento | Ordinal, 5 faixas | D1 |
| M4 | Tipo de tarefa predominante | Categoria (core/auxiliar) da tarefa que mais realiza com IA | Nominal, 2 categorias (derivada de B4) | B4 (+ B3) |

## 3. Matriz QP → pergunta → análise

| QP | Pergunta de pesquisa (resumo) | Variáveis | Perguntas do questionário | Escala | Análise proposta |
|---|---|---|---|---|---|
| **QP1** | Mais frequência de uso de IA ↔ menor impostor? | M1 (resposta) × M2 | B1, C1…C7 | ordinal × ordinal | Correlação de **Spearman** (ρ, IC 95%, p). Análise complementar controlando D1 (correlação parcial ou regressão ordinal). Hipótese H1: ρ < 0. |
| **QP2** | A relação varia com a experiência? | M1 × M2, estratificado por M3 | B1, C1…C7, D1 | ordinal | Spearman **por faixa de experiência** (sugestão: < 3 anos vs. ≥ 3 anos, por causa do n pequeno) + comparação das correlações (transformação z de Fisher) ou termo de interação M2×M3 em regressão ordinal. |
| **QP3** | Impostor difere entre uso para tarefas core vs. auxiliares? | M1 por grupo de M4 | B3, B4, C1…C7 | nominal × ordinal | **Mann-Whitney U** (core vs. auxiliar) + tamanho de efeito (r de postos bisserial / Cliff's δ). Sensibilidade: 3 grupos pela composição de B3 (só core, só auxiliar, ambos) com **Kruskal-Wallis**. Apenas quem respondeu B1 ≠ Nunca. |

## 4. Rastreabilidade pergunta → motivo

| Código | Pergunta (resumo) | Escala | Finalidade | Serve a |
|---|---|---|---|---|
| Z1 | Consentimento | nominal (sim/não) | Ética / LGPD | todas |
| A1 | Maior de 18 anos | nominal | Filtro de elegibilidade | todas |
| A2 | Atua com desenvolvimento | nominal | Filtro de elegibilidade (população-alvo) | todas |
| B1 | Frequência de uso de IA | ordinal 0–4 | **Variável independente** (M2) | QP1, QP2 |
| B2 | Tempo de uso de IA | ordinal 4 níveis | Controle (usuários antigos vs. recentes) | QP1 (sensibilidade) |
| B3 | Tarefas em que usa IA | nominal, múltipla | Caracterizar uso; composição dos grupos de sensibilidade | QP3 |
| B4 | Tarefa mais frequente | nominal | **Variável independente** (M4) | QP3 |
| C1…C7 | Itens da escala de impostor | Likert 1–5 | **Variável dependente** (M1) | QP1, QP2, QP3 |
| AT1 | Item de atenção (marcar a opção 4) | nominal (acerto/erro) | Qualidade dos dados: identifica respostas automáticas ou descuidadas (exigência do enunciado) | todas (filtro de exclusão) |
| D1 | Tempo de experiência | ordinal 5 faixas | **Variável moderadora** (M3) / controle | QP2, QP1 |
| D2 | Faixa etária (opcional) | ordinal | Controle / descrição da amostra | todas (descritiva) |
| D3 | Gênero (opcional) | nominal | Controle / descrição da amostra | todas (descritiva) |
| D4 | Canal de origem | nominal | Avaliar viés de seleção; evidência de divulgação | ameaças à validade |

## 5. Regras de derivação de variáveis (para o dashboard)

1. `M1` = média de C1…C7 (a LIS não tem itens invertidos). AT1 **não** entra na média.
2. `M4`: B4 ∈ {gerar código, completar/refatorar, depurar, testes} → **core**; demais (inclui "Criar protótipos de telas ou interfaces" e "Outra tarefa") → **auxiliar**.
3. Grupo de sensibilidade (QP3): marcou só opções core em B3 → "só core"; só auxiliares → "só auxiliar"; ambos → "misto".
4. Não usuários (B1 = 0) entram em QP1 e QP2 (B1 = 0), mas **ficam fora** de QP3.
5. Quem responde "Não concordo" (Z1) ou "Não" em A1/A2 chega a uma tela final e precisa clicar em **Enviar**:
   isso gera uma linha na planilha só com essas colunas preenchidas. Contar essas linhas como recusas/inelegíveis
   (reportar o número) e **excluí-las** da análise.
   Descartes: Z1 ≠ sim, A1 ≠ sim, A2 ≠ sim, **AT1 ≠ 4 (falhou no item de atenção)**; respostas duplicadas evidentes (mesmos valores em todos os campos
   e timestamps colados). Todo descarte entra no log de desvios/tratamento de dados.

## 6. Pontos a combinar com o grupo

- Confirmar a escolha da **LIS PT-BR (7 itens)** como escala do impostor (decisão provisória, feita por Carlos;
  alternativas: Clance, com validação brasileira em Psico-USF 2021, 20 itens). Verificar no artigo as âncoras
  (Nunca–Quase sempre).
- Se não usuários de IA (B1 = 0) ficam na amostra. A proposta aqui mantém, para dar variabilidade em QP1,
  mas o GQM original fala em "times que utilizam IA no dia a dia". Se mantiver, ajustar a redação do GQM.
- Corte da experiência em QP2 (3 anos é sugestão; confirmar com a distribuição esperada).
- Poder estatístico: com n ≈ 50, só se detectam correlações moderadas (|ρ| ≳ 0,4) com 80% de poder. Declarar
  isso em Ameaças à Validade.
