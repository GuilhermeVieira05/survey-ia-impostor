Diferenças entre o protocolo entregue em 13/11/2026 e o que foi executado.

| # | Seção do protocolo | Previsto | Executado | Motivo | Impacto na validade |
|---|---|---|---|---|---|
| D1 | 8 · Divulgação | Abrir a coleta em 13/11/2026 | Formulário aberto em 17/11/2026; primeira resposta às 19h35 | Abertura do formulário só nessa data | Janela de coleta menor (8 dias em vez de 12), o que contribuiu para não atingir 50 válidas; nenhuma resposta antes do pré-registro |
| D2 | 8 · Divulgação | Encerrar em 20/11, prorrogar até 24/11 se < 50 válidas | Prorrogado até 24/11 | Em 20/11 havia menos de 50 respostas válidas (regra já prevista) | Nenhum: regra do protocolo |
| D3 | 2 · Amostragem | Mínimo de 50 respostas válidas | Coleta encerrada em 24/11 com 45 válidas (55 recebidas) | Fim da prorrogação prevista no protocolo; janela curta (D1) e só dois canais de divulgação (D4) | Com n = 45, a margem de erro sobe de ±13,9 para ±14,6 p.p. e o poder cai |
| D4 | 8 · Divulgação | WhatsApp/Telegram, LinkedIn, Discord/Slack, colegas | Divulgação só por grupos de WhatsApp/Telegram e colegas/professores; LinkedIn e Discord/Slack não foram usados. No D4: WhatsApp/Telegram (26), colegas/professores (18), outro (1) | Decisão do grupo de não usar LinkedIn e Discord/Slack | Amostra concentrada nas redes pessoais do grupo: maior autosseleção e perfil mais homogêneo (jovens, homens, uso diário de IA); conclusões restritas à amostra |
| D5 | 5 · Análise (QP2) | Spearman M1 × B1 em cada faixa de experiência e z de Fisher | Não calculável: todas as 13 pessoas com ≥ 3 anos usam IA diariamente (B1 constante) | Falta de variação nos dados, não prevista | QP2 fica sem teste confirmatório; mostramos como exploratória a alternativa com B2 (tempo de uso) no lugar de B1, fora da família de Holm |
| D6 | 5 · Análise (QP3, sensibilidade) | Kruskal-Wallis com 3 grupos (só core, só auxiliar, misto) | Feito com 3 grupos, mas muito desbalanceados: misto = 42, só core = 1, só auxiliar = 1 | Composição dos dados: quase todos usam IA em tarefas dos dois tipos | Teste pouco informativo; grupos de 1 pessoa não permitem conclusão |
| D7 | 5 · Análise (χ²) | Fisher exato quando esperado < 5 | Fisher exato em tabelas 2×2; nas maiores, p exato por Monte Carlo (20.000 permutações, semente fixa) | O Fisher exato do scipy só cobre 2×2 | Nenhum relevante: o objetivo (p sem depender da aproximação χ²) é o mesmo |
| D8 | 5 · Limpeza | Verificar B4 ⊆ B3 | 1 inconsistência (linha 50: B3 = só "pentest", B4 = "Escrever testes"); mantida na análise principal | O protocolo não dizia se a inconsistência excluía a resposta | Análise de sensibilidade sem essa linha disponível no dashboard |
| D9 | 5 · Limpeza | Excluir só por Z1, A1, A2, AT1 e duplicatas | Mantido. Respostas com C1–C7 todos iguais (inclui a única pessoa que nunca usou IA, linha 12, com tudo 5) **não** foram excluídas | Critério não estava pré-registrado; essas pessoas acertaram AT1 | Análise de sensibilidade sem elas disponível no dashboard; a linha 12 pesa muito em QP1 |
| D10 | 5 · Análise (QP1) | Só B1 como preditor principal | Acrescentadas como sensibilidade: QP1 só com quem usa IA | B1 com quase nenhuma variação (89% "Diariamente") | Exploratório, fora da família de Holm |
| D11 | 6 · Ética e LGPD | Repositório privado enquanto houver dados | CSV versionado em repositório público | Permitir que o dashboard leia os dados brutos e que qualquer avaliador reproduza a análise | Sem identificadores diretos (nome, e-mail, login); faixas de idade e experiência e gênero opcional reduzem o risco de reidentificação, que não é nulo em amostra pequena |
| D12 | 5 · Respostas abertas | Dois codificadores independentes, consenso com um terceiro e κ de Cohen | Codificação feita por um integrante | Só 2 respostas abertas; com n = 2 o κ não é informativo | Classificação depende de um julgamento; afeta só 2 respostas (linha 50 passa a "só core" no grupo de B3) |

#### Tratamento dos dados

- Recusas e inelegíveis: 5 linhas com A2 = Não (geradas pela tela final do formulário), contadas e não analisadas.
- Falha no item de atenção: 5 linhas (AT1 ≠ 4), excluídas pela regra pré-registrada.
- Duplicatas: nenhuma encontrada (critério: todas as respostas iguais, enviadas com menos de 5 minutos de diferença).
- Respostas abertas ("Outro" em B3): 2, codificadas em `dados/codificacao_outro.csv`. Linha 2 (ofertas e produtos digitais, criativos, anúncios, pesquisa de público, vendas) = auxiliar; linha 50 ("pentest") = core.
