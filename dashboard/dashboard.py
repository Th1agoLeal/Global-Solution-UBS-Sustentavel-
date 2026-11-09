"""
Neighborhood Action Dashboard | contribuição de SERS (UBS Sustentável)

Execução (a partir da raiz do repositório):
    pip install -r requirements.txt
    streamlit run dashboard/dashboard.py

Todos os indicadores vêm de SERS/calculos.py e do inventário em dados/consumo_ubs.csv.
Os valores são estimativas condicionadas às premissas e não resultados garantidos.
"""
import sys
from dataclasses import replace
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "SERS"))
import calculos as calc  # noqa: E402

st.set_page_config(page_title="UBS Sustentável | SERS", page_icon="☀️", layout="wide")


def br(valor, casas=2, sufixo=""):
    """Formata número no padrão brasileiro (1.234,56)."""
    if valor is None:
        return "—"
    txt = f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{txt}{sufixo}"


# ----------------------------------------------------------------------------
# Premissas ajustáveis (valores iniciais = README / planilha)
# ----------------------------------------------------------------------------
padrao = calc.Premissas()
st.sidebar.header("Premissas")
kwp = st.sidebar.slider("Potência fotovoltaica (kWp)", 2.0, 20.0, padrao.potencia_fv_kwp, 0.5)
prod = st.sidebar.slider("Produtividade (kWh/kWp/mês)", 90.0, 150.0, padrao.produtividade_kwh_kwp_mes, 1.0)
tarifa = st.sidebar.number_input("Tarifa (R$/kWh)", 0.30, 1.50, padrao.tarifa_kwh, 0.01, format="%.5f")
fator = st.sidebar.number_input("Fator de emissão (kg CO₂/kWh)", 0.010, 0.200, padrao.fator_emissao_kg_kwh, 0.001, format="%.4f")
horas_led = st.sidebar.slider("Horas/dia das lâmpadas com sensores", 4.0, 10.0, padrao.horas_dia_led, 0.5)
st.sidebar.caption(
    "O custo do sistema FV é proporcional à potência escolhida "
    f"(R$ {br(padrao.custo_fv / padrao.potencia_fv_kwp, 0)}/kWp, estimativa)."
)

pr = replace(
    padrao,
    potencia_fv_kwp=kwp,
    produtividade_kwh_kwp_mes=prod,
    tarifa_kwh=tarifa,
    fator_emissao_kg_kwh=fator,
    horas_dia_led=horas_led,
    custo_fv=padrao.custo_fv / padrao.potencia_fv_kwp * kwp,
    manutencao_fv_ano=padrao.manutencao_fv_ano / padrao.potencia_fv_kwp * kwp,
)

itens = calc.carregar_inventario()
cenarios = calc.calcular_todos(itens, pr)
por_nome = {c["cenario"]: c for c in cenarios}

# ----------------------------------------------------------------------------
# Cabeçalho
# ----------------------------------------------------------------------------
st.title("☀️ UBS Sustentável")
st.caption(
    "Neighborhood Action Dashboard · CitizenTech · Global Solution 2026.2 · "
    "SERS — Soluções em Energias Renováveis e Sustentáveis"
)

escolhido = st.selectbox("Alternativa analisada", list(por_nome)[1:], index=2)
c = por_nome[escolhido]
base = por_nome["Situação atual"]

# ----------------------------------------------------------------------------
# Indicadores
# ----------------------------------------------------------------------------
st.subheader("Indicadores energéticos e ambientais")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Consumo da rede (kWh/mês)", br(c["consumo_rede_kwh_mes"]),
          delta=f"{br(c['consumo_rede_kwh_mes'] - base['consumo_rede_kwh_mes'])} vs. atual",
          delta_color="inverse")
k2.metric("Geração solar aproveitada (kWh/mês)", br(c["solar_aproveitado_kwh_mes"]))
k3.metric("Economia energética", f"{br(c['reducao_kwh_mes'])} kWh/mês", delta=f"{br(c['reducao_pct'])} %")
k4.metric("Participação solar (%)", br(c["participacao_solar_pct"]))

k5, k6, k7, k8 = st.columns(4)
k5.metric("Economia financeira líquida (R$/mês)", br(c["economia_liquida_rs_mes"]))
k6.metric("Emissões evitadas (kg CO₂/ano)", br(c["emissoes_evitadas_kg_ano"]))
k7.metric("Investimento estimado (R$)", br(c["investimento_rs"], 0))
k8.metric("Retorno simples (meses)", br(c["payback_meses"], 1))

st.caption(
    "Participação solar = geração aproveitada ÷ consumo após eficiência. "
    "Economia energética = redução da energia comprada da rede em relação à situação atual."
)

# ----------------------------------------------------------------------------
# Consumo por equipamento
# ----------------------------------------------------------------------------
st.subheader("Onde a energia é consumida")
df_inv = pd.DataFrame(itens)
total = df_inv["consumo_kwh_mes"].sum()
df_inv["participacao_pct"] = df_inv["consumo_kwh_mes"] / total * 100
df_inv = df_inv.sort_values("consumo_kwh_mes", ascending=False)

col_a, col_b = st.columns([3, 2])
col_a.bar_chart(df_inv.set_index("equipamento")["consumo_kwh_mes"], horizontal=True)
col_b.dataframe(
    df_inv[["equipamento", "consumo_kwh_mes", "participacao_pct"]].rename(
        columns={"equipamento": "Equipamento", "consumo_kwh_mes": "kWh/mês", "participacao_pct": "%"}
    ),
    hide_index=True,
    width="stretch",
    column_config={
        "kWh/mês": st.column_config.NumberColumn(format="%.2f"),
        "%": st.column_config.NumberColumn(format="%.1f"),
    },
)
st.caption(f"Consumo total estimado: {br(total)} kWh/mês ({br(total * 12)} kWh/ano). E = (P × t) / 1000.")

# ----------------------------------------------------------------------------
# Comparação entre alternativas
# ----------------------------------------------------------------------------
st.subheader("Comparação entre alternativas")
alternativas = cenarios[1:]
df_cmp = pd.DataFrame(
    {
        "Alternativa": [x["cenario"] for x in cenarios],
        "Consumo da rede (kWh/mês)": [x["consumo_rede_kwh_mes"] for x in cenarios],
        "Redução (%)": [x["reducao_pct"] for x in cenarios],
        "Economia líquida (R$/mês)": [x["economia_liquida_rs_mes"] for x in cenarios],
        "Investimento (R$)": [x["investimento_rs"] for x in cenarios],
        "Retorno (meses)": [x["payback_meses"] for x in cenarios],
        "Emissões evitadas (kg CO₂/ano)": [x["emissoes_evitadas_kg_ano"] for x in cenarios],
    }
)
g1, g2 = st.columns(2)
g1.markdown("**Consumo da rede (kWh/mês)**")
g1.bar_chart(df_cmp.set_index("Alternativa")["Consumo da rede (kWh/mês)"])
g2.markdown("**Saldo acumulado (R$) ao longo de 10 anos**")
fluxo = pd.DataFrame({x["cenario"]: calc.fluxo_acumulado(x, 120) for x in alternativas})
fluxo.index.name = "mês"
g2.line_chart(fluxo)
g2.caption("Sem reajuste de tarifa, degradação dos painéis ou troca de inversor. Cruza o zero no retorno simples.")

st.dataframe(
    df_cmp,
    hide_index=True,
    width="stretch",
    column_config={
        "Consumo da rede (kWh/mês)": st.column_config.NumberColumn(format="%.2f"),
        "Redução (%)": st.column_config.NumberColumn(format="%.2f"),
        "Economia líquida (R$/mês)": st.column_config.NumberColumn(format="%.2f"),
        "Investimento (R$)": st.column_config.NumberColumn(format="%.0f"),
        "Retorno (meses)": st.column_config.NumberColumn(format="%.1f"),
        "Emissões evitadas (kg CO₂/ano)": st.column_config.NumberColumn(format="%.2f"),
    },
)
st.download_button(
    "Baixar comparação (CSV)",
    df_cmp.to_csv(index=False).encode("utf-8"),
    file_name="comparacao_alternativas.csv",
    mime="text/csv",
)

# ----------------------------------------------------------------------------
# Limitações
# ----------------------------------------------------------------------------
with st.expander("Premissas e limitações"):
    st.markdown(
        """
- UBS **hipotética**: inventário e horários são estimativas acadêmicas, não medições.
- Economias, geração e emissões são **projeções condicionadas às premissas**, não resultados garantidos.
- Tarifa e fator de emissão são valores adotados; confirmar na fatura real e na fonte oficial (MCTI).
- Geração solar depende de telhado, orientação, inclinação e sombreamento; sem créditos de excedente.
- Não considera reajustes de tarifa, degradação dos módulos, troca de inversor nem emissões do ciclo de vida.
"""
    )
