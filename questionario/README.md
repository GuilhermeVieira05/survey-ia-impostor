# Questionário

Responsável: Carlos (montagem e pré-teste).

| Arquivo | Conteúdo |
|---|---|
| [questionario.md](questionario.md) | Texto completo das perguntas, escalas e lógica (versão `0.2`) |
| [criar_formulario.gs](criar_formulario.gs) | Script do Google Apps Script que cria o formulário de pré-teste (aberto) e o oficial (fechado) |
| [rastreabilidade.md](rastreabilidade.md) | Matriz GQM → QP → métrica → pergunta → escala → análise |
| [pretest.md](pretest.md) | Roteiro do pré-teste, mensagem de convite e tabelas de registro (base da Seção 4 do protocolo) |
| [../protocolo/desvios.md](../protocolo/desvios.md) | Log de desvios (preencher durante a coleta) |

## Como criar os formulários (5 minutos)

1. Abra <https://script.google.com> com a conta do grupo → **Novo projeto**.
2. Cole o conteúdo de [criar_formulario.gs](criar_formulario.gs) e troque `EMAIL_GRUPO` no topo.
3. Escolha a função `criarFormularios` → **Executar** → autorize.
4. Pegue os links no **Registro de execução**. Serão criados:
   - **[PRÉ-TESTE]**, aberto: este link vai para as 3–5 pessoas do pré-teste.
   - **Oficial**, **fechado**: só abrir depois da entrega de 13/Nov (Respostas → "Aceitando respostas").
5. Rode **uma vez só** (rodar de novo duplica os formulários).
6. Teste cada ramo respondendo o pré-teste você mesmo e **apague essas respostas** da planilha dele.
   Ramos: consentimento "Não"; A1 "Não"; A2 "Não"; B1 "Nunca usei" (deve pular B2–B4); B1 qualquer outro.

> O script foi escrito mas **ainda não foi executado nem testado** em uma conta real. Se der erro ao rodar,
> o Apps Script mostra a linha; me mande a mensagem.

## Decisões pendentes com o grupo (bloqueiam a versão 1.0)

- [x] **Escala do impostor:** definida provisoriamente como a **LIS PT-BR (7 itens)**, Silva et al. (2026),
      licença CC BY-NC. Grupo precisa confirmar. Conferir no artigo as âncoras (Nunca–Quase sempre).
- [ ] Manter ou não os **não usuários de IA** na amostra (afeta o texto do GQM). Hoje o formulário mantém.
- [ ] Trocar "impacto" por "associação" no objetivo.
- [ ] Corte de experiência para QP2.
- [ ] Gênero e faixa etária: manter como opcionais ou remover (minimização de dados).
- [x] E-mail de contato do TCLE: e-mail do Carlos (`EMAIL_GRUPO` no script).

## Checklist

- [x] Texto do questionário v0.2 com escala definida
- [x] Script executado e formulários criados (07/Nov)
- [x] E-mail de contato no consentimento dos dois formulários trocado pelo do Carlos (08/Nov)
- [x] Fluxo testado no formulário de pré-teste (07/Nov, desktop): consentimento "Não", A1 "Não", A2 "Não",
      B1 "Nunca usei" (pula B2–B4) e B1 com uso (B2–B4 + escala + perfil). Todos gravaram certo na planilha,
      sem coluna de e-mail. Oficial confirmado **fechado**.
- [x] Testar no celular (pré-teste de 11/Nov foi respondido em computador e celular)
- [x] Respostas de teste apagadas antes do pré-teste
- [ ] Revisão do grupo
- [x] Pré-teste com 3 pessoas de fora (11/Nov), ver [pretest.md](pretest.md)
- [x] Mudanças aplicadas no formulário oficial **e** no `.gs`/`questionario.md`; versão `1.0` congelada (11/Nov):
      opção de B3/B4 "Criar protótipos de telas ou interfaces" e item de atenção AT1
- [ ] Cópia do formulário de pré-teste desativada (Respostas → desligar "Aceitando respostas")
- [ ] Link do oficial passado ao Mateus (12/Nov)
- [ ] Depois da entrega de 13/Nov: abrir o oficial

## Linha do tempo (Carlos)

| Data | Entrega |
|---|---|
| 05–06/Nov | Escala decidida; `questionario.md` e `rastreabilidade.md` prontos ✅ |
| 07/Nov | Script rodado, formulários criados, fluxo testado |
| 08/Nov | Revisão do grupo |
| 09–11/Nov | Pré-teste (3–5 pessoas) |
| 11–12/Nov | Mudanças aplicadas, versão `1.0` congelada, texto da Seção 4 para o Guilherme |
| 12/Nov | Link final ao Mateus |
| 13/Nov | Entrega do protocolo; **depois** abrir o formulário |
