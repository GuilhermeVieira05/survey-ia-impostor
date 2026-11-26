"""Carga, limpeza, derivação de variáveis e testes estatísticos do survey.

Tudo o que o dashboard mostra sai deste módulo, calculado a partir do CSV bruto
exportado do Google Forms (pasta ``dados/``). Nenhum número é digitado à mão.
As regras seguem o protocolo (seção 5) e a matriz de rastreabilidade (seção 5).
"""

from __future__ import annotations

import re
from datetime import date
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parent.parent
DIR_DADOS = RAIZ / "dados"
ARQ_DESVIOS = RAIZ / "protocolo" / "desvios.md"
ARQ_CODIFICACAO = DIR_DADOS / "codificacao_outro.csv"

ALFA = 0.05
FIM_PREVISTO = date(2026, 11, 24)  # fim da prorrogação prevista no protocolo (seção 8)
Z_95 = 1.959963984540054

# --------------------------------------------------------------------------- #
# Dicionário de dados (texto exato das opções no export do Forms)
# --------------------------------------------------------------------------- #

ITENS_C = [f"C{i}" for i in range(1, 8)]

ROTULO_CURTO_C = {
    "C1": "C1 · Medo de ser descoberto(a)",
    "C2": "C2 · Sinto-me um(a) falso(a)",
    "C3": "C3 · Medo de quem importa descobrir",
    "C4": "C4 · Sinto-me impostor(a)",
    "C5": "C5 · Medo de descobrirem o que me falta",
    "C6": "C6 · Não sou tão genuíno(a) quanto pensam",
    "C7": "C7 · Ajo como impostor(a)",
}

B1_COD = {
    "Nunca usei": 0,
    "Menos de uma vez por mês": 1,
    "Algumas vezes por mês": 2,
    "Algumas vezes por semana": 3,
    "Diariamente": 4,
}
B1_ORDEM = list(B1_COD)

B2_ORDEM = [
    "Menos de 6 meses",
    "De 6 meses a menos de 1 ano",
    "De 1 a 2 anos",
    "Mais de 2 anos",
]

D1_ORDEM = [
    "Menos de 1 ano",
    "De 1 a menos de 3 anos",
    "De 3 a menos de 5 anos",
    "De 5 a menos de 10 anos",
    "10 anos ou mais",
]
EXP_MENOS, EXP_MAIS = "< 3 anos", "≥ 3 anos"

NAO_INFORMADO = "Não informado"
D2_ORDEM = ["18 a 24", "25 a 34", "35 a 44", "45 ou mais", NAO_INFORMADO]
D3_ORDEM = ["Feminino", "Masculino", "Outro", NAO_INFORMADO]
D4_ORDEM = [
    "Grupo de WhatsApp / Telegram",
    "LinkedIn",
    "Discord / Slack / comunidade online",
    "Colega, amigo(a) ou professor(a)",
    "Outro",
]

TAREFAS_CORE = [
    "Gerar código novo (funções ou trechos de código)",
    "Completar ou refatorar código existente",
    "Depurar / corrigir bugs",
    "Escrever testes automatizados",
]
TAREFAS_AUX = [
    "Escrever ou revisar documentação (README e comentários)",
    "Buscar informação / tirar dúvidas conceituais (substituindo busca na web)",
    "Entender ou explicar código existente",
    "Criar protótipos de telas ou interfaces",
]
TAREFAS = TAREFAS_CORE + TAREFAS_AUX
TAREFA_OUTRA = "Outra (campo aberto)"

CORE, AUX = "Core", "Auxiliar"
GRUPOS_B3 = ["Só core", "Misto", "Só auxiliar"]

FREQ_DIARIA, FREQ_MENOS = "Diariamente", "Menos que diariamente"

# Códigos das colunas a partir do cabeçalho do Forms ("B1. ...", "[C3. ...]").
_RE_CODIGO = re.compile(r"(?:^|\[)\s*(Z1|A1|A2|B[1-4]|C[1-7]|AT1|D[1-4])\.")


# --------------------------------------------------------------------------- #
# Carga
# --------------------------------------------------------------------------- #


def localizar_csv() -> Path:
    """CSV mais recente exportado do Forms em ``dados/``."""
    candidatos = sorted(
        (p for p in DIR_DADOS.glob("*.csv") if p.name != ARQ_CODIFICACAO.name),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidatos:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {DIR_DADOS}")
    return candidatos[0]


def carregar_bruto(caminho: Path) -> tuple[pd.DataFrame, dict[str, str]]:
    """Lê o CSV exatamente como exportado e renomeia as colunas para os códigos.

    Devolve o DataFrame e o mapa código -> texto original da pergunta.
    """
    bruto = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    mapa, textos = {}, {}
    for col in bruto.columns:
        if col.startswith("Carimbo"):
            mapa[col] = "timestamp"
            continue
        m = _RE_CODIGO.search(col)
        if not m:
            raise ValueError(f"Coluna não reconhecida no CSV: {col!r}")
        cod = m.group(1)
        mapa[col] = cod
        texto = col.split("[", 1)[1].rstrip("]") if "[" in col else col
        textos[cod] = re.sub(rf"^{cod}\.\s*", "", texto.strip())
    df = bruto.rename(columns=mapa)
    df.insert(0, "linha_csv", np.arange(2, len(df) + 2))  # linha 1 = cabeçalho
    return df, textos


def _parse_timestamp(s: pd.Series) -> pd.Series:
    limpo = s.str.replace(r"\s*GMT[+-]\d+$", "", regex=True)
    return pd.to_datetime(limpo, format="%Y/%m/%d %I:%M:%S %p", errors="coerce")


def _likert(s: pd.Series) -> pd.Series:
    """'1 - Nunca' -> 1, '3' -> 3, '' -> NaN."""
    return pd.to_numeric(s.str.extract(r"^\s*(\d)")[0], errors="coerce")


def _parse_b3(valor: str) -> tuple[list[str], str]:
    """Separa as opções conhecidas de B3 do texto livre de "Outro"."""
    if not valor:
        return [], ""
    conhecidas, outros = [], []
    for parte in (p.strip() for p in valor.split(";")):
        if parte in TAREFAS:
            conhecidas.append(parte)
        elif parte:
            outros.append(parte)
    return conhecidas, "; ".join(outros)


# --------------------------------------------------------------------------- #
# Limpeza e derivação
# --------------------------------------------------------------------------- #

MOTIVOS = {
    "Z1": "Recusou o consentimento (Z1 ≠ Sim)",
    "A1": "Menor de 18 anos (A1 ≠ Sim)",
    "A2": "Inelegível: não atua com desenvolvimento (A2 ≠ Sim)",
    "AT1": "Falhou no item de atenção (AT1 ≠ 4)",
    "DUP": "Resposta duplicada",
}
VALIDA = "Válida"


def carregar_codificacao() -> dict[int, str]:
    """Classificação de consenso (core/auxiliar) das respostas "Outro", por linha do CSV."""
    if not ARQ_CODIFICACAO.exists():
        return {}
    cod = pd.read_csv(ARQ_CODIFICACAO, dtype=str, keep_default_na=False)
    return {int(r.linha_csv): r.consenso.strip().lower()
            for r in cod.itertuples() if r.linha_csv.strip() and r.consenso.strip()}


def preparar(df: pd.DataFrame, codificacao: dict[int, str] | None = None) -> pd.DataFrame:
    """Aplica as regras de descarte do protocolo e deriva M1–M4.

    ``codificacao`` (linha do CSV -> "core"/"auxiliar") classifica o texto livre de
    "Outro"; sem codificação, "Outro" conta como auxiliar (regra do protocolo).
    """
    d = df.copy()
    if codificacao is None:
        codificacao = carregar_codificacao()
    outro_core = d["linha_csv"].map(codificacao).eq("core")
    d["ts"] = _parse_timestamp(d["timestamp"])
    d["data"] = d["ts"].dt.date
    d["apos_prazo"] = d["data"] > FIM_PREVISTO
    for c in ITENS_C + ["AT1"]:
        d[c] = _likert(d[c])

    # Motivo de descarte, na ordem em que o formulário filtra.
    motivo = pd.Series(VALIDA, index=d.index, dtype=object)
    motivo[~d["Z1"].str.startswith("Sim")] = MOTIVOS["Z1"]
    motivo[(motivo == VALIDA) & (d["A1"] != "Sim")] = MOTIVOS["A1"]
    motivo[(motivo == VALIDA) & (d["A2"] != "Sim")] = MOTIVOS["A2"]
    motivo[(motivo == VALIDA) & (d["AT1"] != 4)] = MOTIVOS["AT1"]

    # Duplicata evidente: todas as respostas iguais e enviadas a menos de 5 min.
    respostas = [c for c in df.columns if c not in ("linha_csv", "timestamp")]
    candidatos = d[motivo == VALIDA].sort_values("ts")
    for _, grupo in candidatos.groupby(respostas, dropna=False, sort=False):
        if len(grupo) < 2:
            continue
        ultimo = grupo["ts"].iloc[0]
        for idx, ts in grupo["ts"].iloc[1:].items():
            if (ts - ultimo) <= pd.Timedelta(minutes=5):
                motivo[idx] = MOTIVOS["DUP"]
            ultimo = ts
    d["motivo"] = motivo
    d["valida"] = motivo == VALIDA
    d["etapa"] = np.select(
        [d["valida"], motivo.isin([MOTIVOS["Z1"], MOTIVOS["A1"], MOTIVOS["A2"]])],
        ["Válida", "Recusa / inelegível"],
        default="Descartada na limpeza",
    )

    # M1: escore de impostor (média C1–C7; AT1 fica de fora).
    d["M1"] = d[ITENS_C].mean(axis=1)
    d["C_iguais"] = d[ITENS_C].nunique(axis=1).eq(1) & d[ITENS_C].notna().all(axis=1)

    # M2: frequência de uso (0–4) e indicadores complementares.
    d["B1_cod"] = d["B1"].map(B1_COD)
    d["usa_ia"] = d["B1_cod"] > 0
    d["freq_grupo"] = np.where(d["B1"] == "Diariamente", FREQ_DIARIA, FREQ_MENOS)
    b2 = d["B2"].map({v: i + 1 for i, v in enumerate(B2_ORDEM)})
    d["B2_cod"] = np.where(d["B1_cod"] == 0, 0, b2)  # não usuário = 0 meses de uso

    parsed = d["B3"].map(_parse_b3)
    d["B3_lista"] = parsed.map(lambda t: t[0])
    d["B3_outro"] = parsed.map(lambda t: t[1])
    d["n_tarefas"] = d["B3_lista"].map(len) + (d["B3_outro"] != "").astype(int)
    tem_outro = d["B3_outro"] != ""
    tem_core = d["B3_lista"].map(lambda l: any(t in TAREFAS_CORE for t in l)) | (tem_outro & outro_core)
    tem_aux = d["B3_lista"].map(lambda l: any(t in TAREFAS_AUX for t in l)) | (tem_outro & ~outro_core)
    d["B3_grupo"] = np.select(
        [~d["usa_ia"], tem_core & tem_aux, tem_core, tem_aux],
        [None, "Misto", "Só core", "Só auxiliar"],
        default=None,
    )

    # M4: tarefa predominante (B4) em core × auxiliar.
    b4_outra = d["B4"].str.startswith("Outra tarefa")
    d["M4"] = np.select(
        [d["B4"].isin(TAREFAS_CORE) | (b4_outra & outro_core), d["B4"].isin(TAREFAS_AUX) | b4_outra],
        [CORE, AUX],
        default=None,
    )
    d["B4_em_B3"] = np.where(
        ~d["usa_ia"],
        None,
        np.where(
            b4_outra,
            d["B3_outro"] != "",
            [b4 in lst for b4, lst in zip(d["B4"], d["B3_lista"])],
        ),
    )

    # M3: experiência.
    d["D1_cod"] = d["D1"].map({v: i for i, v in enumerate(D1_ORDEM)})
    d["exp_grupo"] = np.where(d["D1_cod"] >= 2, EXP_MAIS, EXP_MENOS)
    d.loc[d["D1_cod"].isna(), "exp_grupo"] = None

    for c in ("D2", "D3"):
        d[c] = d[c].replace({"": NAO_INFORMADO, "Prefiro não informar": NAO_INFORMADO})
    return d


# --------------------------------------------------------------------------- #
# Estatística
# --------------------------------------------------------------------------- #


def margem_erro(n: int, p: float = 0.5) -> float:
    """Margem de erro (95%) de uma proporção, em pontos percentuais."""
    if n <= 0:
        return float("nan")
    return 100 * Z_95 * np.sqrt(p * (1 - p) / n)


def classe_correlacao(r: float) -> str:
    if np.isnan(r):
        return "—"
    a = abs(r)
    return "desprezível" if a < 0.1 else "pequeno" if a < 0.3 else "moderado" if a < 0.5 else "grande"


def classe_epsilon2(e: float) -> str:
    if np.isnan(e):
        return "—"
    return "desprezível" if e < 0.01 else "pequeno" if e < 0.08 else "moderado" if e < 0.26 else "grande"


def _ic_fisher(r: float, n: int, k_controle: int = 0) -> tuple[float, float]:
    """IC 95% por transformação z de Fisher (EP = 1/√(n − 3 − k))."""
    gl = n - 3 - k_controle
    if gl <= 0 or np.isnan(r) or abs(r) >= 1:
        return float("nan"), float("nan")
    z, ep = np.arctanh(r), 1 / np.sqrt(gl)
    return float(np.tanh(z - Z_95 * ep)), float(np.tanh(z + Z_95 * ep))


def spearman(x, y) -> dict:
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 4 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return {"rho": np.nan, "p": np.nan, "n": n, "ic": (np.nan, np.nan),
                "aviso": "variável constante ou n < 4: correlação indefinida"}
    res = stats.spearmanr(x, y)
    rho = float(res.statistic)
    return {"rho": rho, "p": float(res.pvalue), "n": n, "ic": _ic_fisher(rho, n), "aviso": None}


def spearman_parcial(x, y, z) -> dict:
    """Spearman parcial de x e y controlando z (Pearson dos resíduos dos postos)."""
    m = pd.DataFrame({"x": x, "y": y, "z": z}).astype(float).dropna()
    n = len(m)
    if n < 5 or (m.nunique() < 2).any():
        return {"rho": np.nan, "p": np.nan, "n": n, "ic": (np.nan, np.nan),
                "aviso": "variável constante ou n < 5"}
    r = m.rank()
    rxy, rxz, ryz = r["x"].corr(r["y"]), r["x"].corr(r["z"]), r["y"].corr(r["z"])
    den = np.sqrt((1 - rxz**2) * (1 - ryz**2))
    if den == 0:
        return {"rho": np.nan, "p": np.nan, "n": n, "ic": (np.nan, np.nan), "aviso": "colinearidade"}
    rp = float((rxy - rxz * ryz) / den)
    gl = n - 3
    t = rp * np.sqrt(gl / max(1 - rp**2, 1e-12))
    p = float(2 * stats.t.sf(abs(t), gl))
    return {"rho": rp, "p": p, "n": n, "ic": _ic_fisher(rp, n, 1), "aviso": None}


def diferenca_correlacoes(r1: float, n1: int, r2: float, n2: int) -> dict:
    """Teste z de Fisher para ρ1 − ρ2 (amostras independentes) e IC de Zou (2007)."""
    if any(np.isnan(v) for v in (r1, r2)) or n1 <= 3 or n2 <= 3:
        return {"delta": np.nan, "z": np.nan, "p": np.nan, "ic": (np.nan, np.nan)}
    z = (np.arctanh(r1) - np.arctanh(r2)) / np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    p = float(2 * stats.norm.sf(abs(z)))
    l1, u1 = _ic_fisher(r1, n1)
    l2, u2 = _ic_fisher(r2, n2)
    d = r1 - r2
    ic = (d - np.sqrt((r1 - l1) ** 2 + (u2 - r2) ** 2), d + np.sqrt((u1 - r1) ** 2 + (r2 - l2) ** 2))
    return {"delta": float(d), "z": float(z), "p": p, "ic": (float(ic[0]), float(ic[1]))}


def _termo_empates(valores: np.ndarray) -> float:
    _, cont = np.unique(valores, return_counts=True)
    return float(np.sum(cont**3 - cont))


def mann_whitney(a, b) -> dict:
    """Mann-Whitney U bilateral (aproximação normal com correção de empates).

    Tamanhos de efeito: r = |Z|/√N (previsto no protocolo) e correlação
    bisserial de postos (= δ de Cliff), com sinal: > 0 quando ``a`` tende a ser maior.
    """
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    n1, n2 = len(a), len(b)
    N = n1 + n2
    if n1 < 2 or n2 < 2:
        return {"U": np.nan, "Z": np.nan, "p": np.nan, "r": np.nan, "rbc": np.nan,
                "n1": n1, "n2": n2, "dif_mediana": np.nan, "aviso": "grupo com menos de 2 respostas"}
    res = stats.mannwhitneyu(a, b, alternative="two-sided", method="asymptotic", use_continuity=False)
    U = float(res.statistic)
    T = _termo_empates(np.concatenate([a, b]))
    sigma = np.sqrt(n1 * n2 / 12 * ((N + 1) - T / (N * (N - 1))))
    Z = (U - n1 * n2 / 2) / sigma if sigma > 0 else np.nan
    return {
        "U": U, "Z": float(Z), "p": float(res.pvalue), "r": float(abs(Z) / np.sqrt(N)),
        "rbc": float(2 * U / (n1 * n2) - 1), "n1": n1, "n2": n2,
        "dif_mediana": float(np.median(a) - np.median(b)), "aviso": None,
    }


def holm(pvalores) -> list[float]:
    """Correção de Holm-Bonferroni (ignora NaN)."""
    p = np.asarray(pvalores, float)
    ajust = np.full_like(p, np.nan)
    idx = np.where(~np.isnan(p))[0]
    m = len(idx)
    corrente = 0.0
    for pos, i in enumerate(idx[np.argsort(p[idx])]):
        corrente = max(corrente, min(1.0, (m - pos) * p[i]))
        ajust[i] = corrente
    return ajust.tolist()


def kruskal_dunn(grupos: dict[str, np.ndarray]) -> dict:
    """Kruskal-Wallis + ε² + pós-teste de Dunn (correção de empates, Holm)."""
    grupos = {k: np.asarray(v, float)[~np.isnan(np.asarray(v, float))] for k, v in grupos.items()}
    grupos = {k: v for k, v in grupos.items() if len(v) > 0}
    if len(grupos) < 2:
        return {"H": np.nan, "p": np.nan, "eps2": np.nan, "gl": 0, "n": 0, "dunn": pd.DataFrame()}
    todos = np.concatenate(list(grupos.values()))
    N = len(todos)
    if np.ptp(todos) == 0:
        return {"H": np.nan, "p": np.nan, "eps2": np.nan, "gl": len(grupos) - 1, "n": N, "dunn": pd.DataFrame()}
    H, p = stats.kruskal(*grupos.values())
    postos = stats.rankdata(todos)
    medias, ini = {}, 0
    for k, v in grupos.items():
        medias[k] = postos[ini: ini + len(v)].mean()
        ini += len(v)
    fator = N * (N + 1) / 12 - _termo_empates(todos) / (12 * (N - 1))
    linhas = []
    for g1, g2 in combinations(grupos, 2):
        z = (medias[g1] - medias[g2]) / np.sqrt(fator * (1 / len(grupos[g1]) + 1 / len(grupos[g2])))
        linhas.append({"Comparação": f"{g1} × {g2}", "z": z, "p": 2 * stats.norm.sf(abs(z))})
    dunn = pd.DataFrame(linhas)
    dunn["p (Holm)"] = holm(dunn["p"])
    return {"H": float(H), "p": float(p), "eps2": float(H / (N - 1)), "gl": len(grupos) - 1, "n": N, "dunn": dunn}


def qui_quadrado(df: pd.DataFrame, linha: str, coluna: str, n_perm: int = 20000, semente: int = 2026) -> dict | None:
    """χ² de independência com V de Cramér.

    Se alguma frequência esperada < 5: Fisher exato em tabelas 2×2; em tabelas
    maiores, p-valor exato aproximado por Monte Carlo (permutação com margens fixas).
    """
    m = df[[linha, coluna]].dropna()
    tab = pd.crosstab(m[linha], m[coluna])
    tab = tab.loc[tab.sum(axis=1) > 0, tab.sum(axis=0) > 0]
    if tab.shape[0] < 2 or tab.shape[1] < 2:
        return None
    chi2, p, gl, esp = stats.chi2_contingency(tab, correction=False)
    n = int(tab.values.sum())
    v = float(np.sqrt(chi2 / (n * (min(tab.shape) - 1))))
    metodo = "χ² de Pearson"
    if (esp < 5).any():
        if tab.shape == (2, 2):
            metodo = "Fisher exato (esperado < 5)"
            p = float(stats.fisher_exact(tab.values).pvalue)
        else:
            n_fmt = f"{n_perm:,}".replace(",", ".")
            metodo = f"χ² exato por Monte Carlo, {n_fmt} permutações (esperado < 5)"
            rng = np.random.default_rng(semente)
            x = pd.Categorical(m[linha], categories=tab.index).codes
            y = pd.Categorical(m[coluna], categories=tab.columns).codes
            nc = tab.shape[1]
            esp_flat = esp.ravel()
            maiores = 0
            for _ in range(n_perm):
                obs = np.bincount(x * nc + rng.permutation(y), minlength=esp_flat.size)
                if np.sum((obs - esp_flat) ** 2 / esp_flat) >= chi2 - 1e-9:
                    maiores += 1
            p = (maiores + 1) / (n_perm + 1)
    return {"tabela": tab, "chi2": float(chi2), "gl": int(gl), "p": float(p), "V": v,
            "n": n, "metodo": metodo, "min_esperado": float(esp.min())}


def cronbach(itens: pd.DataFrame) -> dict:
    """α de Cronbach com IC 95% de Feldt, α se item excluído e correlação item-total corrigida."""
    itens = itens.dropna()
    n, k = itens.shape

    def _alfa(m: pd.DataFrame) -> float:
        vt = m.sum(axis=1).var(ddof=1)
        if vt == 0 or m.shape[1] < 2:
            return float("nan")
        return float(m.shape[1] / (m.shape[1] - 1) * (1 - m.var(ddof=1).sum() / vt))

    alfa = _alfa(itens)
    if n > 2 and not np.isnan(alfa):
        gl1, gl2 = n - 1, (n - 1) * (k - 1)
        ic = (1 - (1 - alfa) * stats.f.ppf(0.975, gl1, gl2), 1 - (1 - alfa) * stats.f.ppf(0.025, gl1, gl2))
    else:
        ic = (np.nan, np.nan)
    linhas = []
    for c in itens.columns:
        resto = itens.drop(columns=c)
        linhas.append({
            "Item": c,
            "Média": itens[c].mean(),
            "DP": itens[c].std(ddof=1),
            "Correlação item-total corrigida": itens[c].corr(resto.sum(axis=1)),
            "α se item excluído": _alfa(resto),
        })
    return {"alfa": alfa, "ic": ic, "n": n, "k": k, "itens": pd.DataFrame(linhas)}


def kappa_cohen(a: pd.Series, b: pd.Series) -> float:
    m = pd.DataFrame({"a": a, "b": b}).replace("", np.nan).dropna()
    if m.empty:
        return float("nan")
    cats = sorted(set(m["a"]) | set(m["b"]))
    po = float((m["a"] == m["b"]).mean())
    pe = sum((m["a"] == c).mean() * (m["b"] == c).mean() for c in cats)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def descreve(s: pd.Series) -> dict:
    s = s.dropna()
    if s.empty:
        return {"n": 0, "mediana": np.nan, "q1": np.nan, "q3": np.nan, "media": np.nan, "dp": np.nan}
    return {"n": len(s), "mediana": s.median(), "q1": s.quantile(0.25), "q3": s.quantile(0.75),
            "media": s.mean(), "dp": s.std(ddof=1)}
