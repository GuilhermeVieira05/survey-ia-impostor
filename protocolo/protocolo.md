# Protocolo do Survey: assistentes de IA e síndrome do impostor entre desenvolvedores

**Disciplina:** Medição em Engenharia de Software · **Grupo:** Guilherme, Carlos, Mateus e Rafael · **Versão 1.0** · 11/11/2026 · **Entrega da Parte 1:** 13/11/2026
**Repositório:** https://github.com/GuilhermeVieira05/survey-ia-impostor

**Registro prévio.** Este protocolo foi fechado antes de qualquer coleta da amostra. O formulário oficial está com "Aceitando respostas" desligado e só será aberto depois da entrega. A única coleta anterior é o pré-teste (seção 4), feito em uma cópia separada do formulário, cujas respostas não entram na amostra. A data é comprovada pelo commit deste arquivo no repositório e pelo envio na plataforma da disciplina.

## 1. Objetivo e questões de pesquisa

**Objetivo (GQM).** Analisar o **uso de assistentes de IA**, com o propósito de **entender sua associação** com a **síndrome do impostor percebida**, do ponto de vista de **desenvolvedores de software**, no contexto de pessoas que atuam com desenvolvimento, usem ou não assistentes de IA.

- **QP1.** Desenvolvedores que usam IA com mais frequência relatam menor nível de síndrome do impostor? *(H1: correlação negativa.)*
- **QP2.** Essa relação varia com o tempo de experiência do desenvolvedor? *(H2: a correlação difere entre menos e mais experientes.)*
- **QP3.** O nível de síndrome do impostor difere entre quem usa IA principalmente em tarefas **core** (gerar, completar, depurar código; testes) e em tarefas **auxiliares** (documentação, busca, explicação, protótipos)? *(H3: diferença, sem direção prevista.)*

Por ser um survey transversal, as questões tratam de **associação**, não de causa e efeito.

| Métrica | Definição operacional | Escala | Itens |
|---|---|---|---|
| **M1** Síndrome do impostor percebida | média dos 7 itens da Leary Impostorism Scale (LIS), 1 a 5; maior = mais sentimentos de impostor | Likert 5 pontos; escore tratado como **ordinal** | C1–C7 |
| **M2** Frequência de uso de IA | frequência nos últimos 3 meses (nunca = 0 … diariamente = 4) | ordinal, 5 níveis | B1 |
| **M3** Experiência profissional | tempo total com desenvolvimento (5 faixas; corte de QP2: menos de 3 anos × 3 anos ou mais) | ordinal | D1 |
| **M4** Tipo de tarefa predominante | tarefa mais frequente com IA, classificada em core ou auxiliar | nominal, 2 categorias | B4 (e B3) |

## 2. População e amostragem

- **População-alvo.** Pessoas com 18 anos ou mais que atuam, ou atuaram nos últimos 12 meses, com desenvolvimento de software (emprego, estágio, freelance ou projetos próprios remunerados), abordadas em português e majoritariamente brasileiras. Quem **nunca usou IA** permanece na amostra: dá variabilidade a QP1 e QP2, e fica fora de QP3.
- **Origem dos contatos.** Redes dos quatro integrantes: grupos de WhatsApp e Telegram de tecnologia, LinkedIn, Discord e Slack de comunidades de desenvolvedores, colegas e professores. Os respondentes são convidados a repassar o link.
- **Estratégia.** **Não probabilística, por conveniência com bola de neve**, porque não existe cadastro da população-alvo. Os resultados valem para a amostra e não se generalizam à população.
- **Tamanho.** Mínimo de **50 respostas válidas** (depois das exclusões da seção 5). Meta de 70, para ter folga contra exclusões.
- **Margem de erro** (95%, pior caso p = 0,5): e = 1,96 × √(p(1 − p)/n). Com n = 50, **e ≈ ±13,9 p.p. (cerca de ±14)**; com n = 70, e ≈ ±11,7 p.p. A margem é indicativa, pois a amostra não é probabilística.
- **Poder.** Com n = 50, só se detectam correlações moderadas (|ρ| ≳ 0,4) com 80% de poder. Em QP2 cada grupo terá cerca de 25 pessoas, então a análise é exploratória.

## 3. Questionário com rastreabilidade

Formulário anônimo (Google Forms), versão **1.0**, 7 seções, cerca de 4 a 6 minutos. O texto completo está em `questionario/questionario.md` e a matriz completa em `questionario/rastreabilidade.md`.

| Código | Item (resumo) | Métrica / uso | QP | Escala |
|---|---|---|---|---|
| Z1 | Consentimento (Sim / Não concordo) | ética; "Não" encerra | todas | nominal |
| A1, A2 | Tem 18 anos ou mais; atua com desenvolvimento | elegibilidade; "Não" encerra | todas | nominal |
| B1 | Frequência de uso de IA nos últimos 3 meses | **M2**; "Nunca usei" pula B2–B4 | QP1, QP2 | ordinal (0–4) |
| B2 | Há quanto tempo usa IA | controle (sensibilidade) | QP1 | ordinal (4 faixas) |
| B3 | Tarefas em que usa IA (8 opções + "Outro", múltipla) | **M4** (composição) | QP3 | nominal |
| B4 | Tarefa que mais realiza com IA | **M4** | QP3 | nominal |
| C1–C7 | Itens da LIS (C1 a C7) | **M1** | QP1, QP2, QP3 | Likert 1–5 (ordinal) |
| AT1 | Item de atenção, dentro da grade (marcar a opção 4) | qualidade dos dados; filtro | todas | nominal (acerto/erro) |
| D1 | Tempo de experiência (5 faixas) | **M3** | QP2, QP1 | ordinal |
| D2, D3 | Faixa etária; gênero (opcionais) | descrição e controle | todas | ordinal; nominal |
| D4 | Como soube da pesquisa | viés de seleção por canal | validade | nominal |

- **Escala do impostor.** LIS (Leary et al., 2000), na adaptação brasileira de Silva et al. (2026, *Avaliação Psicológica*, 25, e25570; licença CC BY-NC 4.0, uso acadêmico sem fins lucrativos). Âncoras: **1 = Nunca … 5 = Quase sempre**. Todos os itens são diretos (sem item invertido).
- **Construtos com mais de um item.** O impostor é medido por **7 itens** (M1). O uso de IA tem B1 como indicador principal; B2 (duração) e o número de tarefas marcadas em B3 (amplitude) entram como indicadores complementares em análises de sensibilidade. Declaramos que M2 depende principalmente de **um** item.
- **Pergunta de atenção.** AT1: "Para mostrar que está lendo com atenção, marque a opção 4 nesta linha." Quem não marcar 4 é **excluído**, e o número de excluídos é reportado. AT1 não entra em M1.
- **Classificação de tarefas (M4).** *Core:* gerar código novo; completar ou refatorar código; depurar; escrever testes. *Auxiliar:* documentação; buscar informação; entender código; criar protótipos de telas; outra tarefa. Como o Forms não filtra B4 por B3, a consistência B4 ⊆ B3 é verificada na limpeza.

## 4. Pré-teste

**Aplicação.** 3 desenvolvedores de fora do grupo responderam a versão 0.2, em uma cópia do formulário, em **11/11/2026** (respostas às 19h31, 19h32 e 19h42), em computador e celular. Tempo relatado: **4 a 6 minutos** (sem cronômetro). Perfil: os 3 usam IA diariamente, têm 1 a menos de 3 anos de experiência, 18 a 24 anos e são homens. Nenhuma resposta incompleta ou duplicada. As 5 respostas de teste feitas pela equipe em 07/11 foram apagadas antes.

| # | Pergunta | Problema observado | Mudança | Antes → depois |
|---|---|---|---|---|
| 1 | B3 e B4 | Um participante escreveu "Fazer o protótipo de telas" em "Outro": tarefa não prevista | Nova opção "Criar protótipos de telas ou interfaces" (auxiliar) | 7 → 8 opções (+ Outro) |
| 2 | Seção C | Faltava pergunta de atenção (exigência do enunciado, **não** veio dos participantes) | Linha AT1 na grade, fora do escore | 7 → 8 linhas |

Os 3 participantes não apontaram nada confuso, faltando ou incômodo nas demais perguntas, no consentimento, no tempo ou no uso em celular. Resultado: **2 mudanças** (1 opção e 1 item adicionados; nenhuma pergunta reescrita; fluxo mantido). Versão **0.2 → 1.0**.

**Limites.** Os 3 têm perfil homogêneo e não exercitaram o ramo "Nunca usei" com respondentes reais (testado só tecnicamente em 07/11). AT1 foi criado depois e não foi respondido por eles. O tempo é autorrelato.

## 5. Plano de análise

**Limpeza.** Excluir: Z1 ≠ Sim, A1 ≠ Sim, A2 ≠ Sim, **AT1 ≠ 4** e respostas duplicadas evidentes. A quantidade excluída por motivo é reportada. Quem recusa o consentimento ou é inelegível gera uma linha parcial, contada como recusa e não analisada. Campos obrigatórios não geram dados faltantes. D2 e D3 em branco ou "Prefiro não informar" são tratados como categoria própria.

**Descritiva.** Frequências e percentuais (nominais e ordinais); mediana e intervalo interquartil (ordinais); média e desvio-padrão de M1 apenas para descrição. **Confiabilidade:** alfa de Cronbach dos itens C1–C7, com meta ≥ 0,7 (no estudo de validação, α = 0,95 em estudantes); se ficar abaixo, reportamos e interpretamos com cautela.

| QP | Teste (bilateral, α = 0,05) | Variáveis e escala | Tamanho de efeito |
|---|---|---|---|
| QP1 | **Spearman** | M1 × M2 (ordinal × ordinal) | ρ com IC 95% (transformação z de Fisher). Complemento: correlação parcial de Spearman controlando M3 |
| QP2 | **Spearman por faixa** (< 3 anos × ≥ 3 anos) e **teste z de Fisher** para a diferença entre os ρ | M1 × M2, estratificado por M3 | Δρ com IC 95% |
| QP3 | **Mann-Whitney U**, core × auxiliar, só quem usa IA (B1 ≠ Nunca) | M1 por M4 (ordinal × nominal) | r = Z/√N e diferença de medianas. Sensibilidade: **Kruskal-Wallis** com 3 grupos (só core, só auxiliar, misto, a partir de B3), com pós-teste de Dunn |
| Exploratório | **χ²** de independência (Fisher exato se esperado < 5) | tarefa predominante × experiência; canal (D4) × grupo de uso (nominal × nominal) | V de Cramér |

**Múltiplas comparações.** Os 3 testes confirmatórios (QP1, QP2, QP3) formam uma família e usam a **correção de Holm-Bonferroni** (α familiar = 0,05). Pós-testes de Dunn usam Holm. Testes de sensibilidade e χ² são **exploratórios**: reportados e rotulados como tal. Sem inferência causal.

**Respostas abertas.** O único campo livre é "Outro" em B3. Duas pessoas do grupo codificam **de forma independente** (core ou auxiliar e categoria temática), com lista inicial de categorias; divergências são resolvidas por consenso com uma terceira pessoa, e a concordância é reportada (κ de Cohen). Tarefas novas e recorrentes viram categoria própria e o fato vai para a página de desvios.

## 6. Ética e LGPD

- **Consentimento.** Na primeira página do formulário, antes de qualquer pergunta: objetivo, participação voluntária, anonimato, duração, uso exclusivamente acadêmico, possível desconforto (com o CVV, telefone 188) e e-mail para dúvidas. Só segue quem marca "Sim, concordo"; "Não concordo" encerra. A escala mede percepção, não faz diagnóstico.
- **Enquadramento.** Pesquisa de opinião com participantes não identificados; em nosso entendimento, dispensada de registro no sistema CEP/CONEP (Resolução CNS 510/2016, art. 1º, parágrafo único).
- **Anonimização.** Não coletamos nome, e-mail, CPF nem qualquer identificador; o formulário não exige login nem coleta e-mail. Idade e gênero são **opcionais e em faixas** (minimização). Sem identificação, os dados são anonimizados (LGPD, art. 12). Por serem sobre autopercepção emocional, tratamos como dados delicados: acesso restrito e só agregados em público.
- **Armazenamento.** Respostas na planilha vinculada ao Forms (Google Planilhas, acesso restrito aos 4 integrantes) e export CSV com data e hora em `dados/` do repositório do grupo, **mantido privado enquanto houver dados** (docente com acesso). Antes de versionar, o campo livre "Outro" é revisado para remover qualquer detalhe identificável. Planilha e CSV serão **excluídos ao fim da disciplina**.

## 7. Ameaças à validade

| Ameaça | Mitigação |
|---|---|
| **Autosseleção e amostra por conveniência.** Quem tem opinião sobre IA ou impostor tende a responder | Canais variados e repasse do link; D4 permite comparar canais; descrever o perfil da amostra; não generalizar |
| **Não resposta.** Quem nunca usou IA pode não se sentir contemplado | Divulgação aberta a quem usa ou não usa IA; opção "Nunca usei"; lembrete em 16/11; reportar recusas e inelegíveis |
| **Desejabilidade social.** Minimizar sentimentos de impostor por vergonha | Anonimato reforçado no consentimento; "não há respostas certas ou erradas"; sem identificadores |
| **Respostas descuidadas ou automáticas** | Item de atenção AT1 e regra de exclusão definida antes da coleta |
| **Validade de construto.** LIS mede sentimentos de impostor, validada em estudantes (não em devs); âncoras do artigo com redação ambígua; uso de IA medido principalmente por 1 item | Recalcular α na amostra; âncoras "Nunca … Quase sempre" por os itens serem de frequência; B2 e B3 como sensibilidade |
| **Validade interna e causalidade.** Não se distingue "IA reduz impostor" de "quem sente menos impostor usa mais IA"; confundidores (experiência, idade, gênero) | Linguagem de associação; controle por M3; D2 e D3 descritivos |
| **Memória e autorrelato** | Janela fixa de 3 meses em B1; perguntas sobre o estado atual |
| **Poder estatístico baixo** (n ≈ 50; QP2 ≈ 25 por grupo) | Reportar IC; tratar QP2 como exploratória; declarar que efeitos pequenos podem passar despercebidos |
| **Pré-teste limitado** (3 pessoas de perfil igual; ramo "Nunca usei" e AT1 não testados com respondentes) | Declarado na seção 4; fluxo testado tecnicamente; desvios registrados |
| **Validade externa** | Amostra não probabilística: conclusões restritas à amostra |

## 8. Plano de divulgação

- **Canais.** Grupos de WhatsApp e Telegram de desenvolvimento e tecnologia, LinkedIn (posts pessoais dos 4 integrantes), Discord e Slack de comunidades de desenvolvedores brasileiros, colegas e professores. Mateus coordena; todos divulgam.
- **Período de coleta.** Abertura em **13/11/2026**, **depois da entrega** (Carlos liga "Aceitando respostas"), e encerramento em **20/11/2026** (7 dias). Se em 20/11 houver menos de 50 respostas válidas, a coleta é **prorrogada até 24/11**, registrando a decisão na página de desvios. De 25 a 27/11: dashboard e apresentação.
- **Estratégia.** Em 13/11 todos divulgam ao mesmo tempo; em 16/11 há um segundo post para quem não viu. A mensagem informa que é anônima, leva cerca de 5 minutos e vale para quem usa ou não usa IA, com o link do formulário oficial.
- **Evidências.** Prints dos posts com data e hora, nº de respostas por canal (D4) e export bruto com carimbo de data e hora. Qualquer mudança em relação a este protocolo vai para `protocolo/desvios.md`.
