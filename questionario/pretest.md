# Pré-teste do questionário

> Base da **Seção 4 do protocolo**. Só consta o que de fato aconteceu: dados lidos do formulário de pré-teste em
> 11/Nov e informações passadas por Carlos sobre a aplicação. O que não foi medido está dito como "não medido".

## 1. Regras

- **Quem:** 3 pessoas que atuam com desenvolvimento de software e **não** são do grupo (mínimo exigido: 3).
- **Quando:** 11/Nov/2026, antes da entrega de 13/Nov. Respostas registradas pelo Google Forms às 19h31, 19h32 e 19h42.
- **Onde:** em uma **cópia do formulário** (versão 0.2), separada do oficial. As respostas **não entram** na amostra
  final e o export fica arquivado à parte. A cópia é desativada ao final.
- Participantes identificados só como P1 a P3. Sem nome nem contato neste repositório.
- As 5 respostas que a própria equipe usou para testar os ramos do formulário (07/Nov) foram apagadas antes da aplicação.

## 2. Roteiro de aplicação (~10 min por pessoa)

1. Explicar só o necessário: "responda como responderia normalmente e fale se algo não ficar claro".
2. A pessoa responde o formulário no próprio dispositivo.
3. Perguntas de debrief:
   1. Quanto tempo levou? Pareceu longo?
   2. Alguma pergunta, palavra ou opção não ficou clara?
   3. Faltou alguma opção de resposta?
   4. O consentimento ficou claro? Ficou claro que é anônimo?
   5. Alguma pergunta incomodou?
   6. Conseguiu responder B3 e B4 sem confusão?

## 2.1 Mensagem de convite usada

> Oi! Estou fazendo o pré-teste de uma pesquisa da faculdade (Medição em Engenharia de Software) sobre uso de IA e
> como devs se sentem no trabalho. Preciso de ~10 minutos: você responde o formulário e depois me conta o que
> ficou confuso. Suas respostas **não entram** na pesquisa final e o formulário é anônimo. Link: [LINK DO PRÉ-TESTE]

## 3. Participantes

| ID | Data | Perfil (dados do formulário) | Dispositivo | Tempo de resposta |
|---|---|---|---|---|
| P1–P3 | 11/Nov | Os 3: usam IA **diariamente** (B1); experiência de **1 a menos de 3 anos** (D1); 18 a 24 anos (D2); masculino (D3). Tempo de uso de IA (B2): 1 de 6 meses a 1 ano, 2 de 1 a 2 anos. | Misto (computador e celular; contagem por pessoa não registrada) | Entre 4 e 6 min, segundo o relato dos participantes (cronômetro não usado) |

Canal pelo qual chegaram (D4): 2 por colega/amigo/professor, 1 por grupo de WhatsApp/Telegram.

## 4. Dados do pré-teste (n = 3)

- Z1, A1 e A2: 3 de 3 responderam "Sim" (consentiram, maiores de 18 e atuam com desenvolvimento).
- B3 (múltipla escolha): gerar código novo 3; completar/refatorar 3; documentação 3; depurar 2; testes 2; buscar
  informação 2; entender código 2; **"Fazer o protótipo de telas" (campo Outro) 1**.
- B4 (mais frequente): gerar código novo 2; documentação 1. Nenhum marcou "Outra tarefa".
- Escala C1–C7: todas as 5 âncoras foram usadas em ao menos um item e nenhum item teve resposta idêntica nas 3
  pessoas, ou seja, não houve efeito piso/teto evidente com n = 3. Sem inferência estatística nesse n.
- Nenhuma resposta incompleta ou duplicada.

## 5. Problemas encontrados e mudanças feitas

| # | Pergunta | Problema observado | Quem apontou | Mudança feita | Antes → Depois |
|---|---|---|---|---|---|
| 1 | B3 / B4 | Tarefa não prevista na lista: um participante escreveu "Fazer o protótipo de telas" em "Outro" | P (1 de 3), pelo dado do formulário | Nova opção fixa em B3 e B4, categoria auxiliar | 7 opções (+ Outro) → 8 opções (+ Outro) |
| 2 | Seção C | Falta de item de atenção (exigência do enunciado) | Equipe, ao reler o enunciado; **não** veio do pré-teste | Linha AT1 na grade, fora do escore | 7 linhas → 8 linhas (7 da escala + 1 de atenção) |

Sem problemas relatados nas demais perguntas, no consentimento, no tempo ou no uso em celular/computador: nenhum dos
3 participantes apontou algo confuso, faltando ou incômodo.

**Limites do pré-teste (a declarar no protocolo):**
- Os 3 participantes têm o mesmo perfil (usuários diários, 1–3 anos, 18–24 anos, homens). Não exercitaram o ramo
  "Nunca usei" (que pula B2–B4) nem faixas de experiência maiores. Esse ramo foi testado tecnicamente pela equipe em
  07/Nov, não por respondentes reais.
- O item AT1 foi criado depois do pré-teste e não foi respondido pelos participantes.
- Tempo de resposta autorrelatado, sem cronometragem.

## 6. Resumo para o protocolo

- Nº de participantes do pré-teste: 3
- Tempo: 4 a 6 min (autorrelato)
- Nº de mudanças: 2 (opções adicionadas: 1; item adicionado: 1; perguntas reescritas: 0; lógica/fluxo: 0)
- Versão do questionário antes: `0.2` · depois: `1.0`
