# Diagnóstico do problema

Contribuição de SERS (Soluções em Energias Renováveis e Sustentáveis) ao Neighborhood Action Dashboard — CitizenTech.

## 1. Espaço comunitário escolhido

Uma **Unidade Básica de Saúde (UBS) hipotética**, localizada em São Bernardo do Campo (SP), com funcionamento de segunda a sexta-feira, das 7h às 17h (22 dias úteis por mês). O inventário de equipamentos é uma estimativa do grupo, não uma medição em uma unidade real.

A UBS foi escolhida porque é um serviço essencial, de funcionamento diurno (o que combina com a geração solar) e mantido com recursos públicos, de modo que cada kWh economizado reduz a despesa operacional do município.

## 2. Problema energético

Toda a energia da UBS vem da rede elétrica. O consumo estimado é de **1.466,49 kWh/mês** (17.597,88 kWh/ano), o que, à tarifa provisória de R$ 0,78938/kWh, equivale a cerca de **R$ 1.157,62/mês** (R$ 13.891,41/ano).

O diagnóstico por equipamento mostra onde a energia é gasta:

| Equipamento | Consumo (kWh/mês) | Participação |
|---|---:|---:|
| Ar-condicionado | 792,00 | 54,0% |
| Computadores | 211,20 | 14,4% |
| Geladeira de medicamentos | 180,00 | 12,3% |
| Lâmpadas convencionais | 105,60 | 7,2% |
| Equipamentos médicos | 88,00 | 6,0% |
| Ventiladores | 42,24 | 2,9% |
| Roteadores | 21,60 | 1,5% |
| Impressoras | 17,60 | 1,2% |
| Bomba d'água | 8,25 | 0,6% |
| **Total** | **1.466,49** | **100%** |

Dois pontos orientam a proposta:

- A **climatização domina o consumo**. A iluminação, mais simples de trocar, representa só 7,2%, portanto a eficiência em iluminação sozinha tem alcance limitado.
- Não existe hoje **monitoramento**: a gestão só enxerga o consumo pela fatura mensal, sem saber quais equipamentos pesam mais nem se há desperdício.

Os cálculos estão em `SERS/calculos.py` e em `SERS/consumo_energetico.xlsx`; os dados de entrada, em `dados/consumo_ubs.csv`.

## 3. Público beneficiado

- A **população do território atendido pela UBS**, que passa a contar com um serviço mantido a menor custo e com menor impacto ambiental.
- A **equipe de saúde e a gestão municipal**, que ganham indicadores para decidir onde reduzir desperdícios.
- O **município**, que libera recursos de custeio.

## 4. Condições de funcionamento da solução

- Telhado com área, estrutura, orientação e inclinação adequadas e sem sombreamento relevante. Como ordem de grandeza, 10 kWp correspondem a cerca de 18 a 20 módulos de aproximadamente 550 Wp, ocupando algo em torno de 45 a 50 m².
- Sistema fotovoltaico **conectado à rede**, sujeito às regras da distribuidora e à compensação de energia vigentes.
- Medidores de consumo e geração, com conectividade para enviar as leituras ao dashboard.
- Sensores de presença na iluminação; premissa de que reduzem o tempo de lâmpadas acesas de 10 h para 7 h por dia.

## 5. Benefícios esperados

- Redução da energia comprada da rede, estimada em até **86,76%** na alternativa combinada (LED + sensores + solar).
- Economia líquida projetada de cerca de **R$ 974,36/mês**, com retorno simples em torno de 29 meses.
- Emissões evitadas de cerca de **703,86 kg CO₂/ano**, pelo fator de emissão adotado.
- Transparência: o dashboard transforma o consumo em indicadores que a comunidade e a gestão podem acompanhar.

Todos os números acima são **projeções condicionadas às premissas adotadas**, não resultados garantidos.
