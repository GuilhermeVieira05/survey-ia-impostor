"""Gráficos (Plotly) do dashboard. Paleta e estilo num lugar só."""

from __future__ import annotations

import textwrap

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import analysis as an

SUPERFICIE = "#ffffff"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#ecebe7"
EIXO = "#c9c8c3"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # azul, laranja, água (ordem fixa)
NEUTRO = "#b5b4ae"

# Likert divergente: azul (nunca) ↔ cinza (3) ↔ vermelho (quase sempre).
LIKERT_CORES = {1: "#2a78d6", 2: "#86b6ef", 3: "#d6d5d0", 4: "#f09a99", 5: "#e34948"}
LIKERT_ROTULOS = {1: "1 · Nunca", 2: "2", 3: "3", 4: "4", 5: "5 · Quase sempre"}


def _estilo(fig: go.Figure, altura: int, legenda: bool = True) -> go.Figure:
    fig.update_layout(
        height=altura,
        margin=dict(l=8, r=24, t=36 if legenda else 12, b=8),
        paper_bgcolor=SUPERFICIE,
        plot_bgcolor=SUPERFICIE,
        font=dict(family="Inter, system-ui, -apple-system, sans-serif", size=13, color=TEXTO),
        hoverlabel=dict(bgcolor="white", bordercolor=EIXO, font=dict(color=TEXTO, size=13)),
        showlegend=legenda,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, xanchor="left", title=None,
                    font=dict(color=TEXTO_2)),
        bargap=0.28,
        separators=",.",
    )
    fig.update_xaxes(gridcolor=GRADE, zeroline=False, linecolor=EIXO, tickfont=dict(color=TEXTO_2))
    fig.update_yaxes(gridcolor=GRADE, zeroline=False, linecolor=EIXO, tickfont=dict(color=TEXTO_2))
    return fig


def barras_categoria(serie: pd.Series, ordem: list[str], base: int | None = None,
                     grupos: dict[str, str] | None = None,
                     cores_grupo: dict[str, str] | None = None) -> go.Figure:
    """Distribuição de uma variável categórica: n e % (± margem de erro no hover).

    Quando ``grupos`` é informado (categoria -> nome do grupo), colore as barras
    por grupo e exibe legenda horizontal no topo.
    """
    cont = serie.value_counts().reindex(ordem, fill_value=0)
    n = base if base is not None else int(cont.sum())
    pct = cont / n * 100 if n else cont * 0.0
    me = pd.Series([an.margem_erro(n, p / 100) if n else np.nan for p in pct], index=cont.index)

    fig = go.Figure()
    if grupos is None:
        fig.add_trace(go.Bar(
            x=pct.values, y=cont.index, orientation="h",
            marker=dict(color=SERIES[0], cornerradius=4),
            text=[f"{c} · {p:.0f}%" for c, p in zip(cont.values, pct.values)],
            textposition="outside", textfont=dict(color=TEXTO_2),
            customdata=np.column_stack([cont.values, me.values]),
            hovertemplate="<b>%{y}</b><br>%{customdata[0]} respostas · %{x:.1f}%"
                          "<br>margem de erro (95%): ±%{customdata[1]:.1f} p.p.<extra></extra>",
            cliponaxis=False,
        ))
    else:
        ordem_grupos = list(dict.fromkeys(grupos.get(c, "Outro") for c in ordem))
        for i, nome_g in enumerate(ordem_grupos):
            cats = [c for c in ordem if grupos.get(c, "Outro") == nome_g]
            cor = (cores_grupo or {}).get(nome_g, SERIES[i % len(SERIES)])
            c_sub, p_sub, m_sub = cont.loc[cats], pct.loc[cats], me.loc[cats]
            fig.add_trace(go.Bar(
                x=p_sub.values, y=cats, orientation="h", name=nome_g,
                marker=dict(color=cor, cornerradius=4),
                text=[f"{c} · {p:.0f}%" for c, p in zip(c_sub.values, p_sub.values)],
                textposition="outside", textfont=dict(color=TEXTO_2),
                customdata=np.column_stack([c_sub.values, m_sub.values]),
                hovertemplate="<b>%{y}</b><br>%{customdata[0]} respostas · %{x:.1f}%"
                              "<br>margem de erro (95%): ±%{customdata[1]:.1f} p.p.<extra>"
                              + nome_g + "</extra>",
                cliponaxis=False,
            ))
        fig.update_layout(barmode="overlay")

    fig.update_yaxes(categoryorder="array", categoryarray=ordem, autorange="reversed",
                     gridcolor="rgba(0,0,0,0)")
    fig.update_xaxes(range=[0, max(100, float(pct.max()) * 1.25) if n else 100], ticksuffix="%",
                     showticklabels=False, showgrid=False)
    altura = (88 if grupos is not None else 60) + 34 * len(ordem)
    return _estilo(fig, altura, legenda=grupos is not None)


def likert_divergente(df: pd.DataFrame, itens: list[str], rotulos: dict[str, str],
                      textos: dict[str, str]) -> go.Figure:
    """Barras divergentes centradas no ponto neutro (3), que é dividido ao meio."""
    n = len(df)
    cont = pd.DataFrame({c: df[c].value_counts().reindex(range(1, 6), fill_value=0) for c in itens}).T
    pct = cont.div(cont.sum(axis=1).replace(0, np.nan), axis=0).fillna(0) * 100
    y = [rotulos[c] for c in itens]
    fig = go.Figure()

    def _hover(c: str, destaque: int) -> str:
        """Distribuição completa do item; o nível sob o cursor fica em negrito."""
        linhas = [f"<b>{rotulos[c]}</b>"]
        pergunta = textwrap.wrap(textos.get(c, ""), 55)
        if pergunta:
            linhas.append("<i>" + "<br>".join(pergunta) + "</i>")
        for nivel in range(1, 6):
            txt = f"{LIKERT_ROTULOS[nivel]}: {pct.at[c, nivel]:.0f}% ({cont.at[c, nivel]})".replace(".", ",")
            linhas.append(f"<b>▸ {txt}</b>" if nivel == destaque else f"<span style='color:{TEXTO_2}'>  {txt}</span>")
        linhas.append(f"<span style='color:{TEXTO_2}'>n = {int(cont.loc[c].sum())}</span>")
        return "<br>".join(linhas)

    def _traco(nivel: int, valores, mostra: bool, nome_sufixo: str = ""):
        fig.add_trace(go.Bar(
            x=valores, y=y, orientation="h", name=LIKERT_ROTULOS[nivel] + nome_sufixo,
            legendgroup=str(nivel), showlegend=mostra, legendrank=nivel,
            marker=dict(color=LIKERT_CORES[nivel], line=dict(color=SUPERFICIE, width=1.5)),
            hovertext=[_hover(c, nivel) for c in itens],
            hovertemplate="%{hovertext}<extra></extra>",
        ))

    # Lado esquerdo (negativo): metade do 3, depois 2 e 1, empilhando a partir do zero.
    _traco(3, -pct[3].values / 2, True)
    _traco(2, -pct[2].values, True)
    _traco(1, -pct[1].values, True)
    _traco(3, pct[3].values / 2, False)
    _traco(4, pct[4].values, True)
    _traco(5, pct[5].values, True)

    esquerda = (pct[1] + pct[2]).values
    direita = (pct[4] + pct[5]).values
    lim = max(60.0, float((pct[1] + pct[2] + pct[3] / 2).max()), float((pct[4] + pct[5] + pct[3] / 2).max())) + 12
    for yi, e, dr, meio in zip(y, esquerda, direita, pct[3].values / 2):
        fig.add_annotation(x=-(e + meio), y=yi, text=f"{e:.0f}%", xanchor="right", showarrow=False,
                           font=dict(color=TEXTO_2, size=12), xshift=-4)
        fig.add_annotation(x=dr + meio, y=yi, text=f"{dr:.0f}%", xanchor="left", showarrow=False,
                           font=dict(color=TEXTO_2, size=12), xshift=4)

    ticks = list(range(-100, 101, 20))
    fig.update_layout(barmode="relative")
    fig.update_xaxes(range=[-lim, lim], tickvals=ticks, ticktext=[f"{abs(t)}%" for t in ticks],
                     zeroline=True, zerolinecolor=EIXO, zerolinewidth=1)
    fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
    fig.add_annotation(x=-lim, y=1.0, yref="paper", yanchor="bottom", xanchor="left", showarrow=False,
                       text=f"← menos sentimento de impostor (1–2)   ·   n = {n}", font=dict(color=TEXTO_2, size=12),
                       yshift=-2)
    fig.add_annotation(x=lim, y=1.0, yref="paper", yanchor="bottom", xanchor="right", showarrow=False,
                       text="mais sentimento de impostor (4–5) →", font=dict(color=TEXTO_2, size=12), yshift=-2)
    fig = _estilo(fig, 156 + 44 * len(itens))
    fig.update_layout(legend=dict(y=-0.12, yanchor="top"), margin=dict(t=28, b=72))
    return fig


def caixa_pontos(df: pd.DataFrame, x: str, y: str, ordem: list[str], cor: str | None = None,
                 ordem_cor: list[str] | None = None, rotulo_y: str = "M1 (escore de impostor, 1–5)") -> go.Figure:
    """Boxplot com todos os pontos (útil com n pequeno: mostra cada respondente)."""
    fig = go.Figure()
    grupos = [(None, df)] if cor is None else [(g, df[df[cor] == g]) for g in (ordem_cor or [])]
    for i, (nome, sub) in enumerate(grupos):
        cont = sub[x].value_counts()
        fig.add_trace(go.Box(
            x=sub[x], y=sub[y], name=nome or "", boxpoints="all", jitter=0.45, pointpos=0,
            marker=dict(color=SERIES[i % len(SERIES)], size=8, opacity=0.75,
                        line=dict(color=SUPERFICIE, width=1)),
            line=dict(color=SERIES[i % len(SERIES)], width=2),
            fillcolor="rgba(0,0,0,0)",
            customdata=np.column_stack([sub["linha_csv"], sub[x].map(cont)]),
            hovertemplate="<b>%{x}</b><br>M1 = %{y:.2f}<br>linha %{customdata[0]} do CSV<extra>"
                          + (nome or "") + "</extra>",
            showlegend=cor is not None,
        ))
    contagem = df[x].value_counts()
    presentes = [c for c in ordem if contagem.get(c, 0) > 0]
    fig.update_xaxes(categoryorder="array", categoryarray=presentes,
                     tickvals=presentes, ticktext=[f"{c}<br>(n = {contagem.get(c, 0)})" for c in presentes])
    fig.update_yaxes(range=[0.7, 5.3], dtick=1, title=dict(text=rotulo_y, font=dict(color=TEXTO_2, size=12)))
    if cor is not None:
        fig.update_layout(boxmode="group")
    return _estilo(fig, 380, legenda=cor is not None)


def linha_do_tempo(d: pd.DataFrame) -> go.Figure:
    """Respostas recebidas por dia, por situação (válida / descartada / recusa)."""
    etapas = [("Válida", SERIES[0]), ("Descartada na limpeza", SERIES[1]), ("Recusa / inelegível", NEUTRO)]
    dias = pd.date_range(d["ts"].min().normalize(), d["ts"].max().normalize(), freq="D")
    fig = go.Figure()
    for nome, cor in etapas:
        cont = d[d["etapa"] == nome].groupby(d["ts"].dt.normalize()).size().reindex(dias, fill_value=0)
        fig.add_trace(go.Bar(x=dias, y=cont.values, name=nome,
                             marker=dict(color=cor, line=dict(color=SUPERFICIE, width=1.5)),
                             hovertemplate="%{x|%d/%m}: %{y} " + nome.lower() + "<extra></extra>"))
    fig.update_layout(barmode="stack")
    fig.update_xaxes(tickformat="%d/%m", dtick=86400000)
    fig.update_yaxes(title=dict(text="respostas", font=dict(color=TEXTO_2, size=12)))
    return _estilo(fig, 300)


def acumulado_validas(d: pd.DataFrame, meta: int = 50) -> go.Figure:
    v = d[d["valida"]].sort_values("ts")
    fig = go.Figure(go.Scatter(
        x=v["ts"], y=np.arange(1, len(v) + 1), mode="lines", line=dict(color=SERIES[0], width=2, shape="hv"),
        hovertemplate="%{x|%d/%m %H:%M}<br>%{y} válidas acumuladas<extra></extra>", name="Válidas acumuladas",
    ))
    fig.add_hline(y=meta, line=dict(color=TEXTO_2, width=1, dash="dot"),
                  annotation_text=f"mínimo exigido: {meta}", annotation_position="top left",
                  annotation_font=dict(color=TEXTO_2, size=12))

    # Marcos do protocolo (seção 8): encerramento inicial (20/11) e fim da prorrogação (24/11).
    if not v.empty:
        marcos = [
            (pd.Timestamp("2026-11-20 23:59:59"), "20/11 · prazo inicial", EIXO, "dot"),
            (pd.Timestamp(an.FIM_PREVISTO) + pd.Timedelta(hours=23, minutes=59, seconds=59),
             f"{an.FIM_PREVISTO:%d/%m} · prorrogação", SERIES[1], "dash"),
        ]
        tmin, tmax = v["ts"].min(), v["ts"].max()
        for ts_marco, rotulo, cor, estilo in marcos:
            if tmin <= ts_marco <= tmax + pd.Timedelta(days=1):
                fig.add_shape(type="line", x0=ts_marco, x1=ts_marco, y0=0, y1=1,
                              xref="x", yref="paper", line=dict(color=cor, width=1.5, dash=estilo))
                fig.add_annotation(x=ts_marco, y=1.0, xref="x", yref="paper", yanchor="bottom",
                                   xanchor="center", text=rotulo, showarrow=False,
                                   font=dict(color=TEXTO_2 if cor == EIXO else cor, size=11), yshift=4)

    fig.update_yaxes(range=[0, max(meta, len(v)) * 1.12],
                     title=dict(text="respostas válidas", font=dict(color=TEXTO_2, size=12)))
    fig.update_xaxes(tickformat="%d/%m", dtick=86400000)
    fig = _estilo(fig, 310, legenda=False)
    fig.update_layout(margin=dict(t=32))
    return fig


def histograma_m1(s: pd.Series) -> go.Figure:
    s_limpo = s.dropna()
    bordas = np.arange(1.0, 5.01, 0.5)
    centros = (bordas[:-1] + bordas[1:]) / 2
    cont, _ = np.histogram(s_limpo, bins=bordas)
    faixas = [f"{a:.1f}–{b:.1f}".replace(".", ",") for a, b in zip(bordas[:-1], bordas[1:])]
    fig = go.Figure(go.Bar(
        x=centros, y=cont, width=0.42, marker=dict(color=SERIES[0], cornerradius=4),
        customdata=faixas,
        hovertemplate="M1 entre %{customdata}: %{y} respondentes<extra></extra>",
    ))
    if not s_limpo.empty:
        med = float(s_limpo.median())
        ponto_medio = 3.0
        fig.add_shape(type="line", x0=ponto_medio, x1=ponto_medio, y0=0, y1=1,
                      xref="x", yref="paper", line=dict(color=TEXTO_2, width=1.2, dash="dot"))
        fig.add_annotation(x=ponto_medio, y=1.0, xref="x", yref="paper", yanchor="bottom",
                           xanchor="left", xshift=4, text="ponto médio (3,0)", showarrow=False,
                           font=dict(color=TEXTO_2, size=11), yshift=4)
        fig.add_shape(type="line", x0=med, x1=med, y0=0, y1=1,
                      xref="x", yref="paper", line=dict(color=SERIES[1], width=2, dash="dash"))
        med_lado = "right" if abs(med - ponto_medio) < 0.55 else "left"
        fig.add_annotation(x=med, y=1.0, xref="x", yref="paper", yanchor="bottom",
                           xanchor=med_lado, xshift=-4 if med_lado == "right" else 4,
                           text=f"mediana: {med:.2f}".replace(".", ","), showarrow=False,
                           font=dict(color=SERIES[1], size=11), yshift=4)

    ticks = list(bordas)
    fig.update_xaxes(range=[0.95, 5.05], tickvals=ticks,
                     ticktext=[f"{t:.1f}".replace(".", ",") for t in ticks],
                     title=dict(text="M1 (média de C1–C7)", font=dict(color=TEXTO_2, size=12)),
                     showgrid=False)
    fig.update_yaxes(title=dict(text="respondentes", font=dict(color=TEXTO_2, size=12)))
    fig = _estilo(fig, 315, legenda=False)
    fig.update_layout(margin=dict(t=32))
    return fig


def forest(linhas: pd.DataFrame) -> go.Figure:
    """Estimativas com IC 95% (colunas: rotulo, est, lo, hi)."""
    fig = go.Figure(go.Scatter(
        x=linhas["est"], y=linhas["rotulo"], mode="markers",
        marker=dict(color=SERIES[0], size=10, line=dict(color=SUPERFICIE, width=2)),
        error_x=dict(type="data", symmetric=False, array=linhas["hi"] - linhas["est"],
                     arrayminus=linhas["est"] - linhas["lo"], color=SERIES[0], thickness=2, width=0),
        customdata=np.column_stack([linhas["lo"], linhas["hi"]]),
        hovertemplate="<b>%{y}</b><br>ρ = %{x:.2f}<br>IC 95%: [%{customdata[0]:.2f}; %{customdata[1]:.2f}]<extra></extra>",
    ))
    fig.add_vline(x=0, line=dict(color=EIXO, width=1))
    fig.update_xaxes(range=[-1, 1], dtick=0.25, title=dict(text="ρ de Spearman (IC 95%)", font=dict(color=TEXTO_2, size=12)))
    fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
    return _estilo(fig, 90 + 44 * len(linhas), legenda=False)
