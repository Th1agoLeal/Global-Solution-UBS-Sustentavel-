"""
SERS | Global Solution 2026.2 | UBS Sustentável
Cálculos de consumo, comparação de alternativas e indicadores.

Uso (a partir da raiz do repositório):
    python SERS/calculos.py

Fórmula do consumo (enunciado, item 4.2):  E = (P x t) / 1000   [kWh]
    P = potência (W) x quantidade;  t = horas/dia x dias/mês

Todos os valores são ESTIMATIVAS ACADÊMICAS condicionadas às premissas da
classe `Premissas`. Não são medições nem garantia de resultado.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV_INVENTARIO = RAIZ / "dados" / "consumo_ubs.csv"
CSV_RESULTADOS = RAIZ / "dados" / "resultados_cenarios.csv"

MESES_ANO = 12


@dataclass(frozen=True)
class Premissas:
    # Sistema fotovoltaico (alternativa renovável)
    potencia_fv_kwp: float = 10.0
    produtividade_kwh_kwp_mes: float = 120.0  # hipótese a validar (irradiação local)
    custo_fv: float = 26600.0                 # R$, estimativa (não é orçamento)
    manutencao_fv_ano: float = 300.0          # R$/ano, estimativa
    # Eficiência energética (LED + sensores de presença)
    potencia_led_w: float = 18.0              # W por lâmpada LED
    horas_dia_led: float = 7.0                # sensores reduzem de 10 h para 7 h (hipótese)
    custo_led: float = 1500.0                 # R$, LEDs + sensores + instalação
    manutencao_led_ano: float = 60.0          # R$/ano, estimativa
    # Tarifa e emissões
    tarifa_kwh: float = 0.78938               # R$/kWh, provisória: validar na fatura real
    fator_emissao_kg_kwh: float = 0.0461      # kg CO2/kWh, confirmar fonte e ano no MCTI


# ----------------------------------------------------------------------------
# Consumo
# ----------------------------------------------------------------------------
def energia_kwh(quantidade: float, potencia_w: float, horas_dia: float, dias_mes: float) -> float:
    """E = (P x t) / 1000, em kWh/mês."""
    return quantidade * potencia_w * horas_dia * dias_mes / 1000


def carregar_inventario(caminho: Path = CSV_INVENTARIO) -> list[dict]:
    itens = []
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        for linha in csv.DictReader(f):
            q = float(linha["quantidade"])
            p = float(linha["potencia_w"])
            h = float(linha["horas_dia"])
            d = float(linha["dias_mes"])
            itens.append(
                {
                    "equipamento": linha["equipamento"],
                    "quantidade": q,
                    "potencia_w": p,
                    "horas_dia": h,
                    "dias_mes": d,
                    "observacao": linha.get("observacao", ""),
                    "consumo_kwh_mes": energia_kwh(q, p, h, d),
                }
            )
    return itens


def consumo_total(itens: list[dict]) -> float:
    return sum(i["consumo_kwh_mes"] for i in itens)


def _linha_iluminacao(itens: list[dict]) -> dict:
    for i in itens:
        if i["equipamento"].lower().startswith("lâmpadas"):
            return i
    raise ValueError("Linha de iluminação não encontrada no inventário.")


def economia_led(itens: list[dict], pr: Premissas) -> float:
    """Economia mensal (kWh) ao trocar as lâmpadas por LED com sensores de presença."""
    luz = _linha_iluminacao(itens)
    novo = energia_kwh(luz["quantidade"], pr.potencia_led_w, pr.horas_dia_led, luz["dias_mes"])
    return luz["consumo_kwh_mes"] - novo


# ----------------------------------------------------------------------------
# Cenários / alternativas (mesma necessidade energética, mesmo período de referência)
# ----------------------------------------------------------------------------
def cenario(nome: str, descricao: str, itens: list[dict], pr: Premissas,
            usa_eficiencia: bool, usa_solar: bool) -> dict:
    total = consumo_total(itens)
    economia_ef = economia_led(itens, pr) if usa_eficiencia else 0.0
    consumo_pos = total - economia_ef

    geracao = pr.potencia_fv_kwp * pr.produtividade_kwh_kwp_mes if usa_solar else 0.0
    # Simplificação: sem excedente/créditos; só é aproveitada a geração até o limite do consumo.
    solar_aproveitado = min(geracao, consumo_pos)
    consumo_rede = consumo_pos - solar_aproveitado
    reducao_kwh = total - consumo_rede

    investimento = (pr.custo_led if usa_eficiencia else 0.0) + (pr.custo_fv if usa_solar else 0.0)
    manut_mes = ((pr.manutencao_led_ano if usa_eficiencia else 0.0)
                 + (pr.manutencao_fv_ano if usa_solar else 0.0)) / MESES_ANO
    economia_bruta = reducao_kwh * pr.tarifa_kwh
    economia_liquida = economia_bruta - manut_mes
    payback = investimento / economia_liquida if investimento > 0 and economia_liquida > 0 else None

    return {
        "cenario": nome,
        "descricao": descricao,
        "consumo_original_kwh_mes": total,
        "consumo_pos_eficiencia_kwh_mes": consumo_pos,
        "geracao_solar_kwh_mes": geracao,
        "solar_aproveitado_kwh_mes": solar_aproveitado,
        "consumo_rede_kwh_mes": consumo_rede,
        "reducao_kwh_mes": reducao_kwh,
        "reducao_pct": reducao_kwh / total * 100,
        "participacao_solar_pct": solar_aproveitado / consumo_pos * 100 if consumo_pos else 0.0,
        "economia_bruta_rs_mes": economia_bruta,
        "manutencao_rs_mes": manut_mes,
        "economia_liquida_rs_mes": economia_liquida,
        "custo_energia_rede_rs_ano": consumo_rede * pr.tarifa_kwh * MESES_ANO,
        "investimento_rs": investimento,
        "payback_meses": payback,
        "emissoes_evitadas_kg_ano": reducao_kwh * MESES_ANO * pr.fator_emissao_kg_kwh,
    }


def calcular_todos(itens: list[dict], pr: Premissas = Premissas()) -> list[dict]:
    return [
        cenario("Situação atual", "Sem melhorias; toda a energia vem da rede.",
                itens, pr, usa_eficiencia=False, usa_solar=False),
        cenario("A - LED + sensores", "Eficiência energética na iluminação.",
                itens, pr, usa_eficiencia=True, usa_solar=False),
        cenario("B - Solar FV", "Geração fotovoltaica conectada à rede (fonte renovável).",
                itens, pr, usa_eficiencia=False, usa_solar=True),
        cenario("C - LED + sensores + solar", "Combinação de eficiência e geração renovável (proposta).",
                itens, pr, usa_eficiencia=True, usa_solar=True),
    ]


def fluxo_acumulado(c: dict, meses: int = 120) -> list[float]:
    """Saldo acumulado (R$) mês a mês: -investimento + economia líquida acumulada."""
    return [-c["investimento_rs"] + c["economia_liquida_rs_mes"] * m for m in range(meses + 1)]


def sensibilidade_payback(itens: list[dict], pr: Premissas,
                          tarifas: list[float], produtividades: list[float]) -> list[dict]:
    """Payback (meses) do cenário C variando tarifa e produtividade do sistema FV."""
    linhas = []
    for t in tarifas:
        linha = {"tarifa_rs_kwh": t}
        for p in produtividades:
            novo = replace(pr, tarifa_kwh=t, produtividade_kwh_kwp_mes=p)
            c = cenario("C", "", itens, novo, True, True)
            linha[p] = c["payback_meses"]
        linhas.append(linha)
    return linhas


# ----------------------------------------------------------------------------
# Execução em linha de comando
# ----------------------------------------------------------------------------
def _fmt(v, casas=2):
    return "-" if v is None else f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def salvar_resultados(cenarios: list[dict], caminho: Path = CSV_RESULTADOS) -> None:
    campos = list(cenarios[0].keys())
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for c in cenarios:
            w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()})


def main() -> None:
    pr = Premissas()
    itens = carregar_inventario()

    print("== Inventário (kWh/mês) ==")
    total = consumo_total(itens)
    for i in itens:
        print(f"{i['equipamento']:<28} {_fmt(i['consumo_kwh_mes']):>10}  ({i['consumo_kwh_mes']/total*100:4.1f}%)")
    print(f"{'TOTAL':<28} {_fmt(total):>10}   anual: {_fmt(total * MESES_ANO)} kWh\n")

    cenarios = calcular_todos(itens, pr)
    print("== Comparação de alternativas ==")
    for c in cenarios:
        print(f"\n{c['cenario']}")
        for k in ("consumo_rede_kwh_mes", "reducao_kwh_mes", "reducao_pct", "participacao_solar_pct",
                  "economia_liquida_rs_mes", "investimento_rs", "payback_meses", "emissoes_evitadas_kg_ano"):
            print(f"  {k:<28} {_fmt(c[k])}")

    print("\n== Sensibilidade: payback do cenário C (meses) ==")
    prods = [100.0, 120.0, 135.0]
    print("tarifa R$/kWh | " + " | ".join(f"{p:.0f} kWh/kWp/mês" for p in prods))
    for linha in sensibilidade_payback(itens, pr, [0.60, pr.tarifa_kwh, 0.95], prods):
        print(f"{linha['tarifa_rs_kwh']:.5f}       | " + " | ".join(f"{_fmt(linha[p]):>16}" for p in prods))

    salvar_resultados(cenarios)
    print(f"\nResultados salvos em {CSV_RESULTADOS.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
