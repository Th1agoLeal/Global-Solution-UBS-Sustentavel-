# Comparação de alternativas

Contribuição de SERS ao Neighborhood Action Dashboard — CitizenTech.

## 1. Base de comparação

As três alternativas atendem à **mesma necessidade energética** da UBS (1.466,49 kWh/mês, ou 17.597,88 kWh/ano) e usam o **mesmo período de referência** (mês e ano). Todas as contas estão em `SERS/calculos.py`; as premissas estão listadas na seção 5.

| Alternativa | O que inclui | Fonte renovável? |
|---|---|---|
| **A** | Troca das 12 lâmpadas convencionais (40 W) por LED (18 W) com sensores de presença | Não (eficiência) |
| **B** | Sistema fotovoltaico conectado à rede, 10 kWp | **Sim** |
| **C** | A + B combinadas (proposta do grupo) | **Sim** |

## 2. Resultados quantitativos

| Indicador | Situação atual | A: LED + sensores | B: Solar FV | C: LED + sensores + solar |
|---|---:|---:|---:|---:|
| Consumo da rede (kWh/mês) | 1.466,49 | 1.394,15 | 266,49 | **194,15** |
| Economia energética (kWh/mês) | 0 | 72,34 | 1.200,00 | **1.272,34** |
| Economia energética (%) | 0 | 4,93 | 81,83 | **86,76** |
| Participação solar no consumo (%) | 0 | 0 | 81,83 | 86,07 |
| Custo da energia da rede (R$/ano) | 13.891,41 | 13.206,21 | 2.524,34 | **1.839,14** |
| Investimento estimado (R$) | 0 | 1.500 | 26.600 | 28.100 |
| Manutenção (R$/ano) | 0 | 60 | 300 | 360 |
| Economia líquida (R$/mês) | 0 | 52,10 | 922,26 | **974,36** |
| Retorno simples (meses) | — | 28,79 | 28,84 | 28,84 |
| Emissões evitadas (kg CO₂/ano) | 0 | 40,02 | 663,84 | **703,86** |

Fórmulas principais:

- Consumo: `E = (P × t) / 1000`.
- Geração solar: `10 kWp × 120 kWh/kWp/mês = 1.200 kWh/mês`.
- Economia financeira: `kWh economizados × R$ 0,78938/kWh − manutenção mensal`.
- Retorno simples: `investimento ÷ economia líquida mensal`.
- Emissões evitadas: `kWh economizados × 12 × 0,0461 kg CO₂/kWh`.

Na alternativa C, a geração solar (1.200 kWh/mês) é inferior ao consumo após a eficiência (1.394,15 kWh/mês); por isso não há excedente, e a simplificação de não considerar créditos de energia não altera o resultado.

## 3. Análise por critério

### Viabilidade técnica

- **A** é a mais simples: troca de lâmpadas e instalação de sensores, sem obra relevante.
- **B** exige avaliação do telhado (estrutura, área, orientação, inclinação, sombreamento), projeto e aprovação da distribuidora para conexão.
- **C** soma as duas e não cria incompatibilidade: a eficiência reduz a carga e a geração solar cobre a maior parte do que restar.

### Custos

- **A** custa pouco (R$ 1.500), mas economiza só R$ 52,10/mês.
- **B** concentra o investimento (R$ 26.600) e responde por quase toda a economia.
- **C** custa R$ 1.500 a mais que B para economizar mais 72,34 kWh/mês e R$ 52,10/mês adicionais.

### Impactos ambientais

- **A** e **B** reduzem a energia comprada da rede e, com isso, as emissões associadas (40,02 e 663,84 kg CO₂/ano); **C** soma os dois efeitos (703,86 kg CO₂/ano).
- O fator de emissão do SIN brasileiro é baixo por causa da matriz com forte participação hídrica, então a redução absoluta de CO₂ é modesta em comparação com países de rede mais intensiva em carbono.
- Não foram contabilizadas as emissões da fabricação dos módulos e das lâmpadas, nem o descarte. Lâmpadas fluorescentes antigas contêm mercúrio e exigem descarte adequado; módulos e inversores também têm fim de vida a ser tratado.

### Benefícios e limitações

| Alternativa | Benefícios | Limitações |
|---|---|---|
| A | Baixo custo, implantação rápida, sensores geram dados de uso | Alcance pequeno (a iluminação é só 7,2% do consumo); não usa fonte renovável |
| B | Maior redução de consumo e de custo; fonte renovável; combina com funcionamento diurno | Investimento alto; depende do telhado, da irradiação e das regras de compensação; não funciona como reserva em falta de energia |
| C | Maior redução (86,76%) e maior participação renovável; os sensores alimentam o dashboard | Soma as limitações de A e B; resultado depende das premissas |

## 4. Sensibilidade

Retorno simples (meses) da alternativa C ao variar a tarifa e a produtividade do sistema, que são as premissas mais incertas (faixas ilustrativas):

| Tarifa (R$/kWh) | 100 kWh/kWp/mês | 120 kWh/kWp/mês | 135 kWh/kWp/mês |
|---:|---:|---:|---:|
| 0,60 | 45,81 | 38,31 | 34,13 |
| 0,78938 | 34,42 | **28,84** | 25,71 |
| 0,95 | 28,42 | 23,84 | 21,27 |

Mesmo no cenário menos favorável da tabela, o retorno fica em cerca de 46 meses, bem abaixo da vida útil usual de sistemas fotovoltaicos (a ser confirmada em ficha técnica do fabricante).

## 5. Conclusão

As três alternativas têm retorno simples parecido (cerca de 29 meses), então o critério de decisão é o **tamanho do benefício**. A alternativa **C** entrega a maior redução de consumo (86,76%), a maior participação renovável e as maiores emissões evitadas pelo acréscimo de apenas R$ 1.500 sobre B, e por isso é a proposta do grupo. A alternativa B sozinha é uma boa opção se o orçamento permitir só uma das frentes; A sozinha é útil como primeiro passo, mas não resolve o problema.

Esta conclusão vale para as premissas adotadas e não é garantia de resultado.

## 6. Premissas utilizadas

| Premissa | Valor | Observação |
|---|---|---|
| Dias úteis por mês | 22 | Segunda a sexta, 7h às 17h |
| Potência FV | 10 kWp | Proposta conceitual |
| Produtividade FV | 120 kWh/kWp/mês | Hipótese a validar com dados de irradiação local |
| Tarifa | R$ 0,78938/kWh | Provisória; validar na fatura real da UBS |
| Custo do sistema FV | R$ 26.600 | Estimativa, não é orçamento |
| Custo de LED + sensores + instalação | R$ 1.500 | Estimativa preliminar |
| Manutenção FV | R$ 300/ano | Estimativa |
| Manutenção LED + sensores | R$ 60/ano | Estimativa |
| LED | 18 W, 7 h/dia | Sensores reduzem de 10 h para 7 h (hipótese) |
| Fator de emissão | 0,0461 kg CO₂/kWh | Confirmar fonte e ano no MCTI |
