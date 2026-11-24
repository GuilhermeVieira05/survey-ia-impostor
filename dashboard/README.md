# Dashboard (Parte 2)

Dashboard em Streamlit que lê o **CSV bruto** exportado do Google Forms (`../dados/*.csv`, o mais recente) a cada
carregamento e calcula tudo na hora: limpeza, descartes, α de Cronbach, testes das QPs, tamanhos de efeito e
margem de erro. Nenhum número é digitado à mão.

## Como rodar

```bash
cd dashboard
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r requirements.txt
# ou: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Abre em http://localhost:8501. Para atualizar os dados, baixe de novo o CSV do Forms para `dados/` e recarregue a página.

## Páginas

| Página | O que mostra | Item do enunciado |
|---|---|---|
| Perfil da amostra | recebidas, descartadas e motivo de cada descarte; coleta por dia; perfil (B1, B2, B3, B4, D1–D4) com margem de erro | perfil da amostra, evidências |
| Escala do impostor | barras divergentes C1–C7; M1; α de Cronbach (IC de Feldt), α se item excluído | Likert divergente, confiabilidade |
| Questões de pesquisa | QP1–QP3 com teste, p, p Holm, tamanho de efeito, IC e margem de erro; sensibilidade; χ² exploratórios | QPs respondidas |
| Metodologia e desvios | `protocolo/desvios.md`, verificações de qualidade, codificação do "Outro" (κ), derivação das variáveis, testes, limitações | metodologia e desvios |
| Dados brutos | export do Forms linha a linha com a situação de cada resposta | consistência com o protocolo |

A barra lateral tem **filtros por segmento** (experiência, uso de IA, idade, gênero, canal) e **análises de
sensibilidade** (desligadas por padrão).

## Arquivos

- `analysis.py`: carga, limpeza, derivação de M1–M4 e funções estatísticas.
- `charts.py`: gráficos Plotly.
- `app.py`: páginas.
- `../protocolo/desvios.md`: texto da tabela de desvios (editar lá, aparece no dashboard).
- `../dados/codificacao_outro.csv`: códigos dos dois codificadores para as respostas "Outro" (core/auxiliar);
  quando preenchido, o dashboard calcula o κ de Cohen.
