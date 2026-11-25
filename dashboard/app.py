"""Dashboard do survey "IA e síndrome do impostor" (Parte 2).

Executar a partir desta pasta:  .venv/bin/streamlit run app.py
Lê o CSV bruto exportado do Google Forms em ../dados/ a cada carregamento.
"""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

import analysis as an
import charts as ch

st.set_page_config(page_title="Survey · IA e síndrome do impostor", page_icon="📊", layout="wide")


# --------------------------------------------------------------------------- #
# Formatação (padrão brasileiro)
# --------------------------------------------------------------------------- #


def num(x: float, casas: int = 2) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x:.{casas}f}".replace(".", ",")


def fp(p: float) -> str:
    if p is None or np.isnan(p):
        return "—"
    return "< 0,001" if p < 0.001 else num(p, 3)


def ic(par: tuple[float, float], casas: int = 2) -> str:
    lo, hi = par
    if np.isnan(lo) or np.isnan(hi):
        return "—"
    return f"[{num(lo, casas)}; {num(hi, casas)}]"


def decisao(p: float) -> str:
    if p is None or np.isnan(p):
        return "Não testável"
    return "Rejeita H0" if p < an.ALFA else "Não rejeita H0"


# --------------------------------------------------------------------------- #
# Dados
# --------------------------------------------------------------------------- #


@st.cache_data(show_spinner=False)
def carregar(caminho: str, _mtime: float):
    bruto, textos = an.carregar_bruto(an.Path(caminho))
    return bruto, textos, an.preparar(bruto)


caminho = an.localizar_csv()
mtime = caminho.stat().st_mtime
BRUTO, TEXTOS, TODOS = carregar(str(caminho), mtime)
VALIDAS = TODOS[TODOS["valida"]].copy()

# --------------------------------------------------------------------------- #
# Barra lateral: filtros por segmento e análises de sensibilidade
# --------------------------------------------------------------------------- #

with st.sidebar:
    st.markdown("### Filtros por segmento")
    st.caption("Vazio = todos. Os filtros valem para todas as páginas, exceto a contagem de descartes.")
    f_d1 = st.multiselect("Experiência (D1)", an.D1_ORDEM, placeholder="Todas")
    f_exp = st.multiselect("Faixa de experiência (corte de QP2)", [an.EXP_MENOS, an.EXP_MAIS], placeholder="Todas")
    f_b1 = st.multiselect("Frequência de uso de IA (B1)", an.B1_ORDEM, placeholder="Todas")
    f_d2 = st.multiselect("Faixa etária (D2)", an.D2_ORDEM, placeholder="Todas")
    f_d3 = st.multiselect("Gênero (D3)", an.D3_ORDEM, placeholder="Todos")
    f_d4 = st.multiselect("Canal de origem (D4)", an.D4_ORDEM, placeholder="Todos")

    st.markdown("### Sensibilidade")
    st.caption("Não previstas no protocolo, desligadas por padrão. Servem para ver se um resultado depende de poucas respostas.")
    n_iguais = int(VALIDAS["C_iguais"].sum())
    n_b4 = int((VALIDAS["B4_em_B3"] == False).sum())  # noqa: E712
    n_nunca = int((~VALIDAS["usa_ia"]).sum())
    s_iguais = st.toggle(f"Excluir C1–C7 todos iguais ({n_iguais})")
    s_b4 = st.toggle(f"Excluir B4 fora de B3 ({n_b4})")
    s_nunca = st.toggle(f"Excluir quem nunca usou IA ({n_nunca})")

AMOSTRA = VALIDAS
for col, sel in (("D1", f_d1), ("exp_grupo", f_exp), ("B1", f_b1), ("D2", f_d2), ("D3", f_d3), ("D4", f_d4)):
    if sel:
        AMOSTRA = AMOSTRA[AMOSTRA[col].isin(sel)]
if s_iguais:
    AMOSTRA = AMOSTRA[~AMOSTRA["C_iguais"]]
if s_b4:
    AMOSTRA = AMOSTRA[AMOSTRA["B4_em_B3"] != False]  # noqa: E712
if s_nunca:
    AMOSTRA = AMOSTRA[AMOSTRA["usa_ia"]]
FILTRADO = len(AMOSTRA) != len(VALIDAS)

with st.sidebar:
    st.divider()
    st.metric("Respostas analisadas", f"{len(AMOSTRA)} de {len(VALIDAS)}")
    st.caption(f"Fonte: `dados/{caminho.name}`  \nAtualizado em {datetime.fromtimestamp(mtime):%d/%m/%Y %H:%M}")


def aviso_filtro():
    if FILTRADO:
        st.warning(f"Filtros ou sensibilidade ativos: **n = {len(AMOSTRA)}** de {len(VALIDAS)} válidas. "
                   "Os testes nesta visão são **exploratórios**; o resultado oficial é o da amostra completa.",
                   icon="🔎")


# --------------------------------------------------------------------------- #
# Cálculo das questões de pesquisa (usado na página de QPs)
# --------------------------------------------------------------------------- #


def calcular_qps(d: pd.DataFrame) -> dict:
    r = {}
    r["qp1"] = an.spearman(d["B1_cod"], d["M1"])
    r["qp1_parcial"] = an.spearman_parcial(d["B1_cod"], d["M1"], d["D1_cod"])
    r["qp1_b2"] = an.spearman(d["B2_cod"], d["M1"])
    r["qp1_tarefas"] = an.spearman(d["n_tarefas"], d["M1"])
    usuarios = d[d["usa_ia"]]
    r["qp1_usuarios"] = an.spearman(usuarios["B1_cod"], usuarios["M1"])

    grupos = {g: d[d["exp_grupo"] == g] for g in (an.EXP_MENOS, an.EXP_MAIS)}
    r["qp2_grupos"] = {g: an.spearman(s["B1_cod"], s["M1"]) for g, s in grupos.items()}
    a, b = r["qp2_grupos"][an.EXP_MENOS], r["qp2_grupos"][an.EXP_MAIS]
    r["qp2"] = an.diferenca_correlacoes(a["rho"], a["n"], b["rho"], b["n"])
    r["qp2_b2"] = {g: an.spearman(s["B2_cod"], s["M1"]) for g, s in grupos.items()}
    a2, b2 = r["qp2_b2"][an.EXP_MENOS], r["qp2_b2"][an.EXP_MAIS]
    r["qp2_b2_dif"] = an.diferenca_correlacoes(a2["rho"], a2["n"], b2["rho"], b2["n"])

    r["qp3"] = an.mann_whitney(usuarios.loc[usuarios["M4"] == an.CORE, "M1"],
                               usuarios.loc[usuarios["M4"] == an.AUX, "M1"])
    r["qp3_kw"] = an.kruskal_dunn({g: usuarios.loc[usuarios["B3_grupo"] == g, "M1"] for g in an.GRUPOS_B3})

    p_conf = [r["qp1"]["p"], r["qp2"]["p"], r["qp3"]["p"]]
    r["holm"] = an.holm(p_conf)
    return r


# --------------------------------------------------------------------------- #
# Páginas
# --------------------------------------------------------------------------- #


def pagina_perfil():
    st.title("Perfil da amostra")
    st.caption("Assistentes de IA e síndrome do impostor entre desenvolvedores · survey pré-registrado")

    n_total = len(TODOS)
    n_validas = len(VALIDAS)
    n_desc = n_total - n_validas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Respostas recebidas", n_total)
    c2.metric("Descartadas", n_desc, help="Recusas, inelegíveis, falha no item de atenção e duplicatas")
    c3.metric("Válidas", n_validas, delta=f"{n_validas - 50:+d} em relação ao mínimo de 50",
              delta_color="normal")
    c4.metric("Margem de erro (95%, p = 0,5)", f"±{num(an.margem_erro(n_validas), 1)} p.p.",
              help="e = 1,96 × √(p(1 − p)/n). Indicativa: a amostra não é probabilística.")

    st.subheader("Descartes e motivos")
    cont = TODOS["motivo"].value_counts()
    ordem = [an.MOTIVOS[k] for k in ("Z1", "A1", "A2", "AT1", "DUP")]
    tab = pd.DataFrame({"Motivo": ordem, "Respostas": [int(cont.get(m, 0)) for m in ordem]})
    tab["Regra do protocolo"] = ["Seção 5 · limpeza"] * len(tab)
    col_a, col_b = st.columns([2, 3])
    with col_a:
        st.dataframe(pd.concat([tab, pd.DataFrame([{"Motivo": "Total descartado", "Respostas": n_desc,
                                                     "Regra do protocolo": ""}])]),
                     hide_index=True, width="stretch")
    with col_b:
        desc = TODOS[~TODOS["valida"]][["linha_csv", "timestamp", "motivo", "AT1"]].rename(
            columns={"linha_csv": "Linha do CSV", "timestamp": "Carimbo de data/hora",
                     "motivo": "Motivo", "AT1": "Resposta em AT1"})
        st.dataframe(desc, hide_index=True, width="stretch", height=250)
    st.caption("Recusas e inelegíveis geram uma linha parcial no export (o formulário encerra e pede para enviar). "
               "Elas são contadas, mas não analisadas.")

    st.subheader("Coleta ao longo do tempo")
    t1, t2 = st.columns(2)
    with t1:
        st.plotly_chart(ch.linha_do_tempo(TODOS), width="stretch")
    with t2:
        st.plotly_chart(ch.acumulado_validas(TODOS), width="stretch")
    st.caption(f"Primeira resposta: {TODOS['ts'].min():%d/%m/%Y %H:%M} · última: {TODOS['ts'].max():%d/%m/%Y %H:%M} "
               "(horário de Brasília, carimbo do Google Forms).")

    st.subheader("Quem respondeu")
    aviso_filtro()
    n = len(AMOSTRA)
    st.caption(f"Percentuais sobre n = {n}. Passe o mouse para ver a margem de erro de cada proporção.")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**Frequência de uso de IA nos últimos 3 meses (B1)**")
        st.plotly_chart(ch.barras_categoria(AMOSTRA["B1"], an.B1_ORDEM[::-1]), width="stretch")
        st.markdown("**Experiência profissional (D1)**")
        st.plotly_chart(ch.barras_categoria(AMOSTRA["D1"], an.D1_ORDEM), width="stretch")
        st.markdown("**Faixa etária (D2)**")
        st.plotly_chart(ch.barras_categoria(AMOSTRA["D2"], an.D2_ORDEM), width="stretch")
    with g2:
        usuarios = AMOSTRA[AMOSTRA["usa_ia"]]
        st.markdown(f"**Há quanto tempo usa IA (B2)** · só quem usa, n = {len(usuarios)}")
        st.plotly_chart(ch.barras_categoria(usuarios["B2"], an.B2_ORDEM), width="stretch")
        st.markdown("**Canal de origem (D4)**")
        st.plotly_chart(ch.barras_categoria(AMOSTRA["D4"], an.D4_ORDEM), width="stretch")
        st.markdown("**Gênero (D3)**")
        st.plotly_chart(ch.barras_categoria(AMOSTRA["D3"], an.D3_ORDEM), width="stretch")

    st.markdown(f"**Tarefas em que usa IA (B3, múltipla escolha)** · % de quem usa IA, n = {len(usuarios)}")
    marcadas = usuarios["B3_lista"].explode().dropna()
    marcadas = pd.concat([marcadas, pd.Series([an.TAREFA_OUTRA] * int((usuarios["B3_outro"] != "").sum()))])
    ordem_t = an.TAREFAS + [an.TAREFA_OUTRA]
    st.plotly_chart(ch.barras_categoria(marcadas, ordem_t, base=len(usuarios)), width="stretch")
    st.markdown(f"**Tarefa que mais realiza com IA (B4) → M4**")
    b4 = usuarios["B4"].where(~usuarios["B4"].str.startswith("Outra tarefa"), an.TAREFA_OUTRA)
    st.plotly_chart(ch.barras_categoria(b4, ordem_t), width="stretch")
    m4 = usuarios["M4"].value_counts()
    st.caption(f"Core (gerar, completar, depurar, testes): {m4.get(an.CORE, 0)} · "
               f"Auxiliar (documentação, busca, entender código, protótipos, outra): {m4.get(an.AUX, 0)}.")


def pagina_escala():
    st.title("Síndrome do impostor (LIS, 7 itens)")
    aviso_filtro()
    d = AMOSTRA
    st.markdown("Leary Impostorism Scale, adaptação brasileira (Silva et al., 2026). Frequência de 1 = Nunca a "
                "5 = Quase sempre. **M1** = média de C1–C7; o item de atenção AT1 não entra no escore.")
    st.subheader("Distribuição das respostas por item")
    st.plotly_chart(ch.likert_divergente(d, an.ITENS_C, an.ROTULO_CURTO_C, TEXTOS), width="stretch")
    st.caption("Barras divergentes centradas no ponto neutro (3), dividido ao meio. À esquerda, % que marcou 1 ou 2; "
               "à direita, % que marcou 4 ou 5.")

    c1, c2 = st.columns([3, 2])
    alfa = an.cronbach(d[an.ITENS_C])
    with c2:
        st.subheader("Confiabilidade")
        m1, m2 = st.columns(2)
        m1.metric("α de Cronbach", num(alfa["alfa"], 2),
                  help="Meta do protocolo: α ≥ 0,70. No estudo de validação (estudantes), α = 0,95.")
        m2.metric("IC 95% (Feldt)", ic(alfa["ic"]))
        if not np.isnan(alfa["alfa"]):
            if alfa["alfa"] >= 0.7:
                st.success(f"α ≥ 0,70 (meta do protocolo) com {alfa['k']} itens e n = {alfa['n']}.", icon="✅")
            else:
                st.warning("α abaixo de 0,70: interpretar M1 com cautela (protocolo, seção 5).", icon="⚠️")
        tab = alfa["itens"].copy()
        tab["Item"] = tab["Item"].map(an.ROTULO_CURTO_C)
        st.dataframe(tab, hide_index=True, width="stretch",
                     column_config={c: st.column_config.NumberColumn(format="%.2f")
                                    for c in tab.columns if c != "Item"})
    with c1:
        st.subheader("Escore M1")
        dm = an.descreve(d["M1"])
        k1, k2, k3 = st.columns(3)
        k1.metric("Mediana", num(dm["mediana"]))
        k2.metric("Intervalo interquartil", f"{num(dm['q1'])} – {num(dm['q3'])}")
        k3.metric("Média (DP)", f"{num(dm['media'])} ({num(dm['dp'])})", help="Só descritiva; M1 é tratado como ordinal.")
        st.plotly_chart(ch.histograma_m1(d["M1"]), width="stretch")
        alto = (d["M1"] >= 3).mean() * 100 if len(d) else np.nan
        st.caption(f"{num(alto, 0)}% dos respondentes têm M1 ≥ 3 (ponto médio da escala), "
                   f"±{num(an.margem_erro(len(d), alto / 100 if len(d) else 0.5), 1)} p.p. (95%).")


def _linha_resumo(qp, hipotese, teste, n, estat, p, p_holm, efeito, magnitude, me):
    return {"QP": qp, "Hipótese": hipotese, "Teste": teste, "n": n, "Estatística": estat, "p": fp(p),
            "p (Holm)": fp(p_holm), "Tamanho de efeito (IC 95%)": efeito, "Magnitude": magnitude,
            "Margem de erro": f"±{num(me, 1)} p.p.", "Decisão (α = 0,05, Holm)": decisao(p_holm)}


def pagina_qps():
    st.title("Questões de pesquisa")
    aviso_filtro()
    d = AMOSTRA
    r = calcular_qps(d)
    qp1, qp2, qp3 = r["qp1"], r["qp2"], r["qp3"]
    g = r["qp2_grupos"]

    st.subheader("Resumo dos testes confirmatórios")
    linhas = [
        _linha_resumo("QP1", "ρ(uso de IA, impostor) < 0", "Spearman", qp1["n"], f"ρ = {num(qp1['rho'])}",
                      qp1["p"], r["holm"][0], f"ρ = {num(qp1['rho'])} {ic(qp1['ic'])}",
                      an.classe_correlacao(qp1["rho"]), an.margem_erro(qp1["n"])),
        _linha_resumo("QP2", "ρ difere entre < 3 e ≥ 3 anos", "z de Fisher (ρ por faixa)",
                      f"{g[an.EXP_MENOS]['n']} + {g[an.EXP_MAIS]['n']}", f"z = {num(qp2['z'])}", qp2["p"],
                      r["holm"][1], f"Δρ = {num(qp2['delta'])} {ic(qp2['ic'])}",
                      an.classe_correlacao(qp2["delta"]),
                      an.margem_erro(min(g[an.EXP_MENOS]["n"], g[an.EXP_MAIS]["n"]))),
        _linha_resumo("QP3", "impostor difere entre core e auxiliar", "Mann-Whitney U",
                      qp3["n1"] + qp3["n2"], f"U = {num(qp3['U'], 1)}; Z = {num(qp3['Z'])}", qp3["p"],
                      r["holm"][2], f"r = {num(qp3['r'])}; δ de Cliff = {num(qp3['rbc'])}",
                      an.classe_correlacao(qp3["r"]), an.margem_erro(qp3["n1"] + qp3["n2"])),
    ]
    st.dataframe(pd.DataFrame(linhas), hide_index=True, width="stretch")
    n_testes = sum(not np.isnan(p) for p in (qp1["p"], qp2["p"], qp3["p"]))
    st.caption(f"Família de {n_testes} teste(s) confirmatório(s) com correção de Holm-Bonferroni (α familiar = 0,05); "
               "testes não computáveis saem da família. Margem de erro: pior caso (p = 0,5) para o n do teste; em QP2, "
               "a do menor grupo. Survey transversal: os resultados indicam **associação**, não causa.")

    # ---------------- QP1 ----------------
    st.divider()
    st.subheader("QP1 · Quem usa IA com mais frequência relata menos síndrome do impostor?")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(ch.caixa_pontos(d, "B1", "M1", an.B1_ORDEM), width="stretch")
    with c2:
        st.markdown(f"**Spearman, M1 × B1 (0–4):** ρ = {num(qp1['rho'])}, IC 95% {ic(qp1['ic'])}, "
                    f"p = {fp(qp1['p'])}, p Holm = {fp(r['holm'][0])}, n = {qp1['n']}.")
        if qp1["aviso"]:
            st.error(qp1["aviso"])
        moda = d["B1"].value_counts(normalize=True)
        if len(moda):
            st.info(f"**Pouca variação em B1:** {num(moda.iloc[0] * 100, 0)}% responderam “{moda.index[0]}”. "
                    "Com quase todos na mesma categoria, o ρ é instável e depende de poucas respostas "
                    "(ver “só quem usa IA” abaixo e a opção de sensibilidade na barra lateral).", icon="ℹ️")
        pp = r["qp1_parcial"]
        st.markdown(f"**Complemento — Spearman parcial controlando experiência (D1):** ρ = {num(pp['rho'])}, "
                    f"IC 95% {ic(pp['ic'])}, p = {fp(pp['p'])}.")
    sens = pd.DataFrame([
        {"rotulo": "QP1 · B1 × M1 (protocolo)", **_forest(qp1)},
        {"rotulo": "QP1 · parcial, controlando D1", **_forest(r["qp1_parcial"])},
        {"rotulo": "Sensib. · só quem usa IA (B1 ≥ 1)", **_forest(r["qp1_usuarios"])},
        {"rotulo": "Sensib. · tempo de uso (B2) × M1", **_forest(r["qp1_b2"])},
        {"rotulo": "Sensib. · nº de tarefas (B3) × M1", **_forest(r["qp1_tarefas"])},
    ])
    st.markdown("**Estimativas de QP1 e análises de sensibilidade** (exploratórias, sem correção)")
    st.plotly_chart(ch.forest(sens.dropna(subset=["est"])), width="stretch")
    st.dataframe(sens.assign(**{"IC 95%": [ic((lo, hi)) for lo, hi in zip(sens["lo"], sens["hi"])],
                                "ρ": sens["est"].map(num), "p": sens["p"].map(fp)})
                 [["rotulo", "n", "ρ", "IC 95%", "p"]].rename(columns={"rotulo": "Análise"}),
                 hide_index=True, width="stretch")

    # ---------------- QP2 ----------------
    st.divider()
    st.subheader("QP2 · A relação varia com o tempo de experiência?")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(ch.caixa_pontos(d, "B1", "M1", an.B1_ORDEM, cor="exp_grupo",
                                        ordem_cor=[an.EXP_MENOS, an.EXP_MAIS]), width="stretch")
    with c2:
        tab = pd.DataFrame([{"Faixa": k, "n": v["n"], "ρ": num(v["rho"]), "IC 95%": ic(v["ic"]), "p": fp(v["p"])}
                            for k, v in g.items()])
        st.dataframe(tab, hide_index=True, width="stretch")
        st.markdown(f"**Diferença (z de Fisher):** Δρ = {num(qp2['delta'])}, IC 95% (Zou) {ic(qp2['ic'])}, "
                    f"z = {num(qp2['z'])}, p = {fp(qp2['p'])}, p Holm = {fp(r['holm'][1])}.")
        for k, v in g.items():
            if v["aviso"]:
                b1_vals = d.loc[d["exp_grupo"] == k, "B1"].unique()
                st.error(f"**{k}:** ρ indefinido — {v['aviso']}. Valores de B1 nesse grupo: "
                         f"{', '.join(map(str, b1_vals)) or 'nenhum'}. O teste de QP2 previsto no protocolo "
                         "**não pode ser calculado** com estes dados (registrado em desvios).")
        st.markdown("**Alternativa exploratória (desvio): tempo de uso de IA (B2) no lugar de B1**")
        tab2 = pd.DataFrame([{"Faixa": k, "n": v["n"], "ρ (B2 × M1)": num(v["rho"]), "IC 95%": ic(v["ic"]),
                              "p": fp(v["p"])} for k, v in r["qp2_b2"].items()])
        st.dataframe(tab2, hide_index=True, width="stretch")
        dif = r["qp2_b2_dif"]
        st.caption(f"Δρ = {num(dif['delta'])}, IC 95% {ic(dif['ic'])}, z = {num(dif['z'])}, p = {fp(dif['p'])} "
                   "(exploratório, fora da família de Holm).")

    # ---------------- QP3 ----------------
    st.divider()
    st.subheader("QP3 · O nível de impostor difere entre quem usa IA em tarefas core e auxiliares?")
    usuarios = d[d["usa_ia"]]
    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(ch.caixa_pontos(usuarios, "M4", "M1", [an.CORE, an.AUX]), width="stretch")
    with c2:
        mc = an.descreve(usuarios.loc[usuarios["M4"] == an.CORE, "M1"])
        ma = an.descreve(usuarios.loc[usuarios["M4"] == an.AUX, "M1"])
        st.dataframe(pd.DataFrame([
            {"Grupo (B4)": an.CORE, "n": mc["n"], "Mediana": num(mc["mediana"]), "IIQ": f"{num(mc['q1'])} – {num(mc['q3'])}"},
            {"Grupo (B4)": an.AUX, "n": ma["n"], "Mediana": num(ma["mediana"]), "IIQ": f"{num(ma['q1'])} – {num(ma['q3'])}"},
        ]), hide_index=True, width="stretch")
        st.markdown(f"**Mann-Whitney U** = {num(qp3['U'], 1)}, Z = {num(qp3['Z'])}, p = {fp(qp3['p'])}, "
                    f"p Holm = {fp(r['holm'][2])}.  \n**Efeito:** r = |Z|/√N = {num(qp3['r'])} "
                    f"({an.classe_correlacao(qp3['r'])}); δ de Cliff = {num(qp3['rbc'])}; "
                    f"diferença de medianas (core − auxiliar) = {num(qp3['dif_mediana'])}.")
        if qp3["aviso"]:
            st.error(qp3["aviso"])
        st.caption("Só quem usa IA (B1 ≠ Nunca). δ de Cliff > 0 indica M1 maior no grupo core.")

    kw = r["qp3_kw"]
    st.markdown("**Sensibilidade · Kruskal-Wallis pela composição de B3** (só core, misto, só auxiliar)")
    k1, k2 = st.columns([3, 2])
    with k1:
        st.plotly_chart(ch.caixa_pontos(usuarios.dropna(subset=["B3_grupo"]), "B3_grupo", "M1", an.GRUPOS_B3),
                        width="stretch")
    with k2:
        cont = usuarios["B3_grupo"].value_counts().reindex(an.GRUPOS_B3, fill_value=0)
        st.dataframe(cont.rename("n").rename_axis("Grupo (B3)").reset_index(), hide_index=True, width="stretch")
        st.markdown(f"H = {num(kw['H'])}, gl = {kw['gl']}, p = {fp(kw['p'])}, "
                    f"ε² = {num(kw['eps2'], 3)} ({an.classe_epsilon2(kw['eps2'])}).")
        vazios = [gname for gname in an.GRUPOS_B3 if cont[gname] == 0]
        if vazios:
            st.info(f"Grupo(s) sem respondentes: {', '.join(vazios)}. O teste fica com {kw['gl'] + 1} grupos.", icon="ℹ️")
        if not kw["dunn"].empty:
            st.markdown("Pós-teste de Dunn (Holm)")
            st.dataframe(kw["dunn"].assign(z=kw["dunn"]["z"].map(num), p=kw["dunn"]["p"].map(fp),
                                           **{"p (Holm)": kw["dunn"]["p (Holm)"].map(fp)}),
                         hide_index=True, width="stretch")

    # ---------------- Exploratórios ----------------
    st.divider()
    st.subheader("Análises exploratórias · χ² de independência")
    st.caption("Previstas no protocolo como exploratórias: reportadas sem correção para múltiplas comparações.")
    e1, e2 = st.columns(2)
    for col, (titulo, base, lin, colu) in zip(
        (e1, e2),
        (("Tarefa predominante (M4) × experiência", usuarios, "M4", "exp_grupo"),
         ("Canal de origem (D4) × frequência de uso", d, "D4", "freq_grupo")),
    ):
        with col:
            st.markdown(f"**{titulo}**")
            res = an.qui_quadrado(base, lin, colu)
            if res is None:
                st.info("Tabela com menos de 2 linhas ou colunas nesta seleção.")
                continue
            st.dataframe(res["tabela"], width="stretch")
            st.markdown(f"{res['metodo']}: χ² = {num(res['chi2'])}, gl = {res['gl']}, p = {fp(res['p'])}, "
                        f"V de Cramér = {num(res['V'])} ({an.classe_correlacao(res['V'])}), n = {res['n']}. "
                        f"Menor frequência esperada: {num(res['min_esperado'], 1)}.")


def _forest(res: dict) -> dict:
    return {"est": res["rho"], "lo": res["ic"][0], "hi": res["ic"][1], "p": res["p"], "n": res["n"]}


def pagina_metodologia():
    st.title("Metodologia e desvios")
    st.markdown(
        "O protocolo (Parte 1) foi entregue em **13/11/2026** e versionado antes da primeira resposta. "
        "Esta página mostra como os dados foram tratados e **o que mudou em relação ao protocolo, e por quê**."
    )

    st.subheader("Desvios em relação ao protocolo")
    if an.ARQ_DESVIOS.exists():
        st.markdown(an.ARQ_DESVIOS.read_text(encoding="utf-8"))
    else:
        st.warning("Arquivo protocolo/desvios.md não encontrado.")

    st.subheader("Verificações de qualidade calculadas dos dados")
    v = VALIDAS
    inconsist = v[v["B4_em_B3"] == False]  # noqa: E712
    iguais = v[v["C_iguais"]]
    q1, q2, q3 = st.columns(3)
    q1.metric("B4 fora de B3", len(inconsist), help="Tarefa predominante não marcada entre as tarefas usadas.")
    q2.metric("C1–C7 todos iguais", len(iguais), help="Padrão possível de resposta automática (não previsto como descarte).")
    q3.metric("Respostas em “Outro” (B3)", int((v["B3_outro"] != "").sum()))
    if len(inconsist):
        st.markdown("**B4 fora de B3** (mantidas na análise principal; ver sensibilidade na barra lateral)")
        st.dataframe(inconsist[["linha_csv", "B3", "B4"]].rename(columns={"linha_csv": "Linha do CSV"}),
                     hide_index=True, width="stretch")
    if len(iguais):
        st.markdown("**C1–C7 com o mesmo valor** (todas acertaram AT1)")
        st.dataframe(iguais.assign(valor=iguais["C1"].astype(int))[["linha_csv", "valor", "B1", "D1"]]
                     .rename(columns={"linha_csv": "Linha do CSV", "valor": "Valor em C1–C7"}),
                     hide_index=True, width="stretch")

    st.subheader("Codificação das respostas abertas (“Outro” em B3)")
    outros = v[v["B3_outro"] != ""][["linha_csv", "B3_outro", "B4"]].rename(
        columns={"linha_csv": "linha_csv", "B3_outro": "Texto"})
    if an.ARQ_CODIFICACAO.exists():
        cod = pd.read_csv(an.ARQ_CODIFICACAO, dtype=str, keep_default_na=False)
        cod["linha_csv"] = pd.to_numeric(cod["linha_csv"], errors="coerce")
        outros = outros.merge(cod, on="linha_csv", how="left")
        kap = an.kappa_cohen(outros.get("codificador_A", pd.Series(dtype=str)),
                             outros.get("codificador_B", pd.Series(dtype=str)))
        st.markdown(f"κ de Cohen entre os dois codificadores: **{num(kap)}**" if not np.isnan(kap)
                    else "κ de Cohen não calculado: só um codificador preencheu `dados/codificacao_outro.csv` (desvio D12).")
    st.dataframe(outros.rename(columns={"linha_csv": "Linha do CSV"}), hide_index=True, width="stretch")
    st.caption("A coluna “consenso” define se o “Outro” conta como core ou auxiliar em M4 e nos grupos de B3. "
               "Sem codificação, “Outro” conta como auxiliar (regra do protocolo).")

    st.subheader("Como cada variável foi derivada")
    st.dataframe(pd.DataFrame([
        {"Métrica": "M1 · Síndrome do impostor", "Origem": "C1–C7", "Regra": "média dos 7 itens (1–5); AT1 fora", "Escala": "ordinal"},
        {"Métrica": "M2 · Frequência de uso de IA", "Origem": "B1", "Regra": "Nunca = 0 … Diariamente = 4", "Escala": "ordinal"},
        {"Métrica": "M2' · Tempo de uso (sensib.)", "Origem": "B2", "Regra": "não usa = 0; < 6 meses = 1 … > 2 anos = 4", "Escala": "ordinal"},
        {"Métrica": "M2'' · Amplitude (sensib.)", "Origem": "B3", "Regra": "nº de tarefas marcadas (inclui Outro)", "Escala": "razão"},
        {"Métrica": "M3 · Experiência", "Origem": "D1", "Regra": "5 faixas (0–4); corte de QP2: < 3 × ≥ 3 anos", "Escala": "ordinal"},
        {"Métrica": "M4 · Tarefa predominante", "Origem": "B4", "Regra": "gerar, completar, depurar, testes = core; demais = auxiliar; Outra = conforme codificação", "Escala": "nominal"},
        {"Métrica": "Grupo B3 (sensib. QP3)", "Origem": "B3", "Regra": "só core / misto / só auxiliar (Outro conforme codificação)", "Escala": "nominal"},
    ]), hide_index=True, width="stretch")

    st.subheader("Testes e por que foram escolhidos")
    st.markdown(
        "- **Escalas ordinais** (M1, M2, M3) → testes não paramétricos baseados em postos.\n"
        "- **QP1:** correlação de Spearman (ordinal × ordinal), IC 95% pela transformação z de Fisher "
        "(EP = 1/√(n − 3)); complemento: Spearman parcial controlando D1.\n"
        "- **QP2:** Spearman em cada faixa de experiência e teste z de Fisher para a diferença; IC de Δρ pelo método de Zou (2007).\n"
        "- **QP3:** Mann-Whitney U (ordinal × nominal com 2 grupos), aproximação normal com correção de empates; "
        "efeito r = |Z|/√N e δ de Cliff. Sensibilidade: Kruskal-Wallis (ε²) com pós-teste de Dunn (Holm).\n"
        "- **Exploratórios:** χ² de independência com V de Cramér; Fisher exato (2×2) ou Monte Carlo (tabelas maiores) "
        "quando alguma frequência esperada é < 5.\n"
        "- **Múltiplas comparações:** Holm-Bonferroni na família QP1–QP3.\n"
        "- **Confiabilidade:** α de Cronbach com IC 95% de Feldt; α se item excluído e correlação item-total corrigida.\n"
        "- **Margem de erro:** e = 1,96 × √(p(1 − p)/n), pior caso p = 0,5. A amostra é por conveniência "
        "(bola de neve), então a margem é indicativa e as conclusões valem para a amostra."
    )

    st.subheader("Limitações")
    st.markdown(
        "- **Autosseleção e conveniência:** quase todos vieram de grupos de WhatsApp/Telegram e de colegas; não generalizar.\n"
        "- **Não resposta:** não há como saber quantas pessoas viram o convite e não responderam; reportamos recusas e inelegíveis.\n"
        "- **Desejabilidade social:** a escala pede autorrelato de sentimentos negativos; anonimato reforçado no consentimento.\n"
        "- **Pouca variação no uso de IA:** quase todos usam diariamente, o que limita QP1 e impede QP2 como planejado.\n"
        "- **Poder baixo:** com n ≈ 45, só correlações de |ρ| ≳ 0,4 seriam detectadas com 80% de poder.\n"
        "- **Causalidade:** survey transversal — associação, não efeito da IA."
    )


def pagina_dados():
    st.title("Dados brutos")
    st.markdown("Export do Google Forms **exatamente como baixado** (colunas renomeadas para os códigos do "
                "questionário), com a situação de cada linha após a limpeza. Não há identificadores pessoais.")
    so_validas = st.toggle("Mostrar só as válidas")
    tab = BRUTO.merge(TODOS[["linha_csv", "motivo"]], on="linha_csv")
    if so_validas:
        tab = tab[tab["motivo"] == an.VALIDA]
    st.dataframe(tab.rename(columns={"linha_csv": "Linha do CSV", "motivo": "Situação"}),
                 hide_index=True, width="stretch", height=600)
    st.download_button("Baixar variáveis derivadas (CSV)",
                       VALIDAS[["linha_csv", "M1", "B1_cod", "B2_cod", "n_tarefas", "M4", "B3_grupo",
                                "D1_cod", "exp_grupo", "D2", "D3", "D4"]].to_csv(index=False).encode("utf-8"),
                       file_name="variaveis_derivadas.csv", mime="text/csv")
    with st.expander("Dicionário: código → pergunta"):
        st.dataframe(pd.DataFrame(list(TEXTOS.items()), columns=["Código", "Pergunta"]), hide_index=True, width="stretch")


paginas = st.navigation([
    st.Page(pagina_perfil, title="Perfil da amostra", icon="👥", url_path="perfil", default=True),
    st.Page(pagina_escala, title="Escala do impostor", icon="📏", url_path="escala"),
    st.Page(pagina_qps, title="Questões de pesquisa", icon="🧪", url_path="questoes"),
    st.Page(pagina_metodologia, title="Metodologia e desvios", icon="📝", url_path="metodologia"),
    st.Page(pagina_dados, title="Dados brutos", icon="🗂️", url_path="dados"),
])
paginas.run()
