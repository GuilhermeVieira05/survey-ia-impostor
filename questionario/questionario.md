# Questionário — versão 1.0 (congelada após o pré-teste)

> Texto exato a ser colocado no formulário. Cada pergunta tem um **código** (ex.: `B1`) que é usado na
> [matriz de rastreabilidade](rastreabilidade.md) e nos nomes das colunas do export.
> Tempo estimado de resposta: **~4 minutos** (validar no pré-teste).
> O formulário é criado a partir deste texto pelo script [`criar_formulario.gs`](criar_formulario.gs).
> **Se mudar algo aqui, mude também no script (e vice-versa).**

**Convenções**

- **[obrigatória]** = resposta obrigatória no formulário.
- **[condicional]** = só aparece dependendo de uma resposta anterior.
- Escalas estão declaradas em cada pergunta (nominal, ordinal, Likert 1–5).
- O formulário **não coleta e-mail, nome nem qualquer identificador** (anonimato).

**Mudanças da 0.1 para a 0.2:** escala do impostor definida (LIS, 7 itens, PT-BR); B4 ganhou a opção "Outra tarefa".

**Mudanças da 0.2 para a 1.0 (11/Nov):**
1. B3 e B4 ganharam a opção "Criar protótipos de telas ou interfaces" (categoria: auxiliar). Origem: um participante do
   pré-teste escreveu "Fazer o protótipo de telas" em "Outro".
2. Nova linha de **atenção** AT1 dentro da grade da Seção C ("Para mostrar que está lendo com atenção, marque a opção 4
   nesta linha."). Origem: exigência do enunciado (pergunta de atenção), **não** do pré-teste; não foi respondida
   pelos 3 participantes. Fica fora do escore M1.

**Correção após teste do formulário (07/Nov):** as opções de B3 não podem ter vírgula, porque o Google Forms grava
as marcadas numa só célula separadas por vírgula. Reescritas: "Gerar código novo (funções ou trechos de código)" e
"Escrever ou revisar documentação (README e comentários)".

---

## Seção 0 — Apresentação e consentimento (TCLE)

**Texto de abertura:**

> **Pesquisa: uso de assistentes de IA e síndrome do impostor entre desenvolvedores**
>
> Esta pesquisa faz parte de um trabalho da disciplina *Medição em Engenharia de Software*. Queremos entender
> como o uso de assistentes de IA (ChatGPT, GitHub Copilot, Claude, Gemini, Cursor etc.) se relaciona com a
> forma como desenvolvedores percebem a própria competência.
>
> - **Participação voluntária.** Você pode desistir a qualquer momento, simplesmente fechando a página.
> - **Anônima.** Não pedimos nome, e-mail ou qualquer dado que identifique você. Os resultados serão
>   apresentados apenas de forma agregada.
> - **Duração:** cerca de 4 minutos.
> - **Uso dos dados:** exclusivamente acadêmico (análise estatística e apresentação em sala).
> - **Desconforto:** algumas perguntas tratam de sentimentos sobre o próprio desempenho profissional. Se você
>   se sentir incomodado(a), pode parar. Se precisar de apoio emocional, o CVV atende 24h pelo telefone **188**.
> - **Dúvidas:** [e-mail do grupo — preencher].
>
> Não há respostas certas ou erradas.

**Z1.** Li as informações acima e concordo em participar. **[obrigatória]** · nominal
- ( ) Sim, concordo em participar → continua
- ( ) Não concordo → **encerra o formulário** (tela de agradecimento)

---

## Seção A — Elegibilidade

**A1.** Você tem 18 anos ou mais? **[obrigatória]** · nominal
- ( ) Sim → continua
- ( ) Não → **encerra o formulário**

**A2.** Você atua (ou atuou nos últimos 12 meses) com desenvolvimento de software, seja em emprego, estágio,
freelance ou projetos próprios remunerados? **[obrigatória]** · nominal
- ( ) Sim → continua
- ( ) Não → **encerra o formulário**

---

## Seção B — Uso de assistentes de IA

> Texto de apoio: *"Considere assistentes de IA como ChatGPT, GitHub Copilot, Claude, Gemini, Cursor, entre
> outros, usados em atividades de desenvolvimento de software."*

**B1.** Nos **últimos 3 meses**, com que frequência você usou assistentes de IA nas suas atividades de
desenvolvimento? **[obrigatória]** · ordinal (5 níveis, codificação 0–4)
- ( ) Nunca usei → `0` · **pula para a Seção C**
- ( ) Menos de uma vez por mês → `1`
- ( ) Algumas vezes por mês → `2`
- ( ) Algumas vezes por semana → `3`
- ( ) Diariamente → `4`

**B2.** Há quanto tempo você usa assistentes de IA no desenvolvimento? **[obrigatória · condicional: B1 ≠ Nunca]** ·
ordinal (variável de controle)
- ( ) Menos de 6 meses
- ( ) De 6 meses a menos de 1 ano
- ( ) De 1 a 2 anos
- ( ) Mais de 2 anos

**B3.** Para quais tarefas você usa assistentes de IA? *(marque todas que se aplicam)* **[obrigatória ·
condicional: B1 ≠ Nunca]** · nominal, múltipla escolha

| Opção | Categoria (uso interno, **não aparece** para o respondente) |
|---|---|
| Gerar código novo (funções ou trechos de código) | core |
| Completar ou refatorar código existente | core |
| Depurar / corrigir bugs | core |
| Escrever testes automatizados | core |
| Escrever ou revisar documentação (README e comentários) | auxiliar |
| Buscar informação / tirar dúvidas conceituais (substituindo busca na web) | auxiliar |
| Entender ou explicar código existente | auxiliar |
| Criar protótipos de telas ou interfaces (v1.0) | auxiliar |
| Outra: ______ (campo aberto) | auxiliar (revisar caso a caso e registrar em desvios se reclassificar) |

**B4.** Dentre as tarefas marcadas, qual você mais realiza com IA? *(escolha uma)* **[obrigatória · condicional:
B1 ≠ Nunca]** · nominal. O Google Forms não filtra as opções de acordo com B3, então B4 repete a lista
completa de B3 mais **"Outra tarefa (a que informei em B3)"**. Na análise, validar que B4 ⊆ B3 (inconsistências
vão para o log de tratamento de dados).

---

## Seção C — Síndrome do impostor percebida

**Escala:** *Leary Impostorism Scale* (LIS), 7 itens, adaptação brasileira. Fonte do instrumento original:
Leary et al. (2000). Fonte da versão em português: **Silva, P. G. N., Araújo, G. R., Araújo, R. S., Araujo, G. O.,
Dantas, L. M. G. L., Medeiros, E. D., Couto, R. N., & Alvarenga, M. A. S. (2026).** *Leary Impostorism Scale (LIS):
Evidências psicométricas para o contexto brasileiro.* Avaliação Psicológica, 25, e25570.
https://doi.org/10.15689/ap.2026.25.e25570 (licença CC BY-NC 4.0: uso permitido para fins não comerciais com
atribuição; este trabalho é acadêmico e sem fins lucrativos).

**Instrução ao respondente:**
> *"Indique com que frequência cada afirmação descreve você, pensando em como se sente no seu trabalho com
> desenvolvimento de software."*

**C1–C7** · Likert de 5 pontos: **1 = Nunca · 2 · 3 · 4 · 5 = Quase sempre** **[obrigatórias]**

| Código | Item (texto da adaptação brasileira) |
|---|---|
| C1 | Às vezes fico assustado(a)/com medo de que serei descoberto(a) por quem eu realmente sou. |
| C2 | Eu costumo me sentir um(a) falso(a). |
| C3 | Tenho medo das pessoas que são importantes para mim, talvez descubram que não sou tão capaz como eles pensam que sou. |
| C4 | Em algumas situações me sinto como impostor(a). |
| AT1 | **Item de atenção (não é da LIS):** "Para mostrar que está lendo com atenção, marque a opção 4 nesta linha." Fica entre C4 e C5. |
| C5 | Às vezes eu temo que outros descubram o quanto de conhecimento ou habilidade realmente me faltam. |
| C6 | Em algumas situações sinto-me como "um falso/impostor"; isto é, eu não sou tão genuíno(a) quanto as pessoas pensam que realmente eu sou. |
| C7 | Em algumas situações eu ajo como um impostor(a). |

Regras de pontuação:
- Todos os itens são diretos (**nenhum item invertido** na versão publicada).
- **Atenção:** quem não marcar 4 em AT1 é excluído da análise (o número de excluídos é reportado). AT1 não entra em M1.
- **Escore da síndrome do impostor (M1) = média dos 7 itens C1–C7 (faixa 1–5)**; maior = mais sentimentos de impostor.
  Itens obrigatórios, então não há dados faltantes.
- Reportar **alfa de Cronbach** na nossa amostra (o artigo reporta α = 0,95 e ω = 0,95 em estudantes
  universitários; nossa população é diferente, por isso recalcular).

> ⚠️ **Verificar no artigo:** a seção de Instrumentos fala em âncoras "1 (nunca) a 5 (quase sempre)", enquanto a
> introdução descreve a escala original como "1 (nada característico) a 5 (extremamente característico)".
> Os itens são redigidos em termos de frequência ("às vezes", "costumo"), então usamos **Nunca → Quase sempre**.
> Confirmar na leitura completa do artigo e, se necessário, ajustar as âncoras aqui e no script.

---

## Seção D — Perfil

**D1.** Qual é o seu tempo total de experiência profissional com desenvolvimento de software? **[obrigatória]** ·
ordinal (variável de QP2)
- ( ) Menos de 1 ano
- ( ) De 1 a menos de 3 anos
- ( ) De 3 a menos de 5 anos
- ( ) De 5 a menos de 10 anos
- ( ) 10 anos ou mais

**D2.** Qual é a sua faixa etária? *(opcional)* · ordinal (controle)
- ( ) 18 a 24 · ( ) 25 a 34 · ( ) 35 a 44 · ( ) 45 ou mais · ( ) Prefiro não informar

**D3.** Qual é o seu gênero? *(opcional)* · nominal (controle — a literatura aponta diferenças de gênero em
escalas de impostor)
- ( ) Feminino · ( ) Masculino · ( ) Outro · ( ) Prefiro não informar

**D4.** Como você ficou sabendo desta pesquisa? **[obrigatória]** · nominal (usado para avaliar viés de seleção
por canal)
- ( ) Grupo de WhatsApp / Telegram
- ( ) LinkedIn
- ( ) Discord / Slack / comunidade online
- ( ) Colega, amigo(a) ou professor(a)
- ( ) Outro

---

## Tela final

> **Obrigado(a) por participar!** Suas respostas foram registradas de forma anônima.
> Se quiser ajudar, compartilhe a pesquisa com outros desenvolvedores.
> Se algum tema desta pesquisa te afetou, o CVV atende 24h pelo telefone **188** (ligação gratuita).

---

## Resumo de tamanho

| Seção | Perguntas | Obs. |
|---|---|---|
| 0 Consentimento | 1 | |
| A Elegibilidade | 2 | |
| B Uso de IA | 4 (1 se "Nunca") | |
| C Impostor | 7 + 1 de atenção | grade 8 × 5 |
| D Perfil | 4 | 2 opcionais |
| **Total** | **19** (16 se "Nunca") | contando AT1 |
