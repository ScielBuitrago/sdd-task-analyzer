# Especificação SDD - Módulo TaskAnalyzer

## 1. Visão Geral e Propósito do Sistema

### 1.1 Propósito do Módulo
O **TaskAnalyzer** é um módulo de análise de dados e métricas em Python. O seu objetivo é processar um conjunto de tarefas recebidas e calcular indicadores acionáveis de produtividade e eficiência da equipa, tais como tempo médio de conclusão, taxa de atraso e distribuição por níveis de prioridade.

---

## 2. Contrato Executável de Interface

### 2.1 Entradas (Inputs)
A entrada do sistema é uma lista de dicionários, onde cada elemento representa uma tarefa com a seguinte estrutura:

| Campo | Tipo | Obrigatório | Descrição / Restrições |
| :--- | :--- | :---: | :--- |
| `id_tarefa` | `int` | Sim | Identificador único da tarefa (`> 0`). |
| `data_criacao` | `datetime` | Sim | Data/hora de criação (UTC). |
| `data_inicio` | `datetime` | Não | Data/hora de início da execução. |
| `data_conclusao` | `datetime` | Não | Data/hora de conclusão da execução. |
| `prazo` | `datetime` | Sim | Data/hora limite para conclusão. |
| `prioridade` | `str enum` | Sim | Valores aceites: `['baixa', 'média', 'alta']`. |
| `status` | `str enum` | Sim | Valores aceites: `['concluida', 'pendente', 'cancelada']`. |

### 2.2 Saídas (Outputs)
O módulo retorna um dicionário consolidado com a seguinte estrutura de dados:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `tempo_medio_conclusao_min` | `float` | Tempo médio de conclusão em minutos (por prioridade e geral). |
| `taxa_atraso_percentual` | `float` | Percentual de tarefas concluídas após o prazo (por prioridade e geral). |
| `quantidade_tarefas` | `int` | Total de tarefas consideradas na análise (por prioridade e geral). |
| `indicadores_por_prioridade` | `dict` | Estrutura com métricas agrupadas por prioridade (`baixa`, `média`, `alta`). |

### 2.3 Regras de Negócio e Restrições
- **Filtro por Status:** Considerar apenas tarefas com `status = 'concluida'` para o cálculo de tempo e atraso.
- **Cálculo de Tempo:** $\text{Tempo de conclusão} = \text{data\_conclusao} - \text{data\_inicio}$ (em minutos).
- **Regra de Atraso:** Uma tarefa é considerada em atraso quando `data_conclusao > prazo`.
- **Validação de Inconsistências:** Ignorar tarefas com datas inconsistentes (ex.: `data_conclusao` anterior a `data_inicio`).
- **Divisão por Zero:** Deve ser devidamente tratado quando não houver tarefas concluídas na amostra.
- **Fuso Horário:** Fuso horário sempre em **UTC**.
- **Arredondamento:** Arredondar métricas numéricas para **2 casas decimais**.

### 2.4 Assinatura da Função Pública
```python
from typing import List, Dict, Any

def analisar_tarefas(tarefas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Processa uma lista de tarefas e retorna os indicadores consolidados de desempenho.
    
    Args:
        tarefas (List[Dict[str, Any]]): Lista de dicionários no formato do contrato.
        
    Returns:
        Dict[str, Any]: Dicionário contendo os indicadores calculados e o agrupamento por prioridade.
    """
    pass