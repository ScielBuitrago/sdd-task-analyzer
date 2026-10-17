# SDD TaskAnalyzer - Módulo de Análise de Produtividade

Este repositório contém a especificação técnica (Software Design Document - SDD) e a estrutura do módulo **TaskAnalyzer**, desenvolvido para processar tarefas executadas e gerar métricas de produtividade.

---

## 1. Identificação do Projeto

- **Estudante:** [Sciel Ramos Rodrigues Buitrago]
- **Curso / Polo / Turma:** [Turma A]
- **E-mail Institucional:** [felipe.buitrago@gmail.com]
- **Data de Elaboração:** [17/10/2026]
- **Versão da Especificação:** 1.0.0

---

## 2. Propósito do Módulo TaskAnalyzer

O **TaskAnalyzer** é um motor de análise em Python projetado para:
- Analisar tarefas executadas e gerar métricas consolidadas de produtividade.
- Calcular o tempo médio de conclusão por tipo e nível de prioridade.
- Identificar a taxa de atraso (percentual de tarefas concluídas após o prazo limite).
- Agrupar e gerar indicadores por prioridade (`baixa`, `média`, `alta`).
- Fornecer métricas confiáveis para apoio à tomada de decisão e melhoria contínua dos processos da equipe.

---

## 3. Contrato Executável de Interface

### 3.1 Entradas (Inputs)
A função do módulo recebe uma lista de tarefas contendo a seguinte estrutura de dados:

| Campo | Tipo | Obrigatório | Descrição / Restrições |
| :--- | :--- | :---: | :--- |
| `id_tarefa` | `int` | Sim | Identificador único da tarefa (`> 0`). |
| `data_criacao` | `datetime` | Sim | Data/hora de criação (fuso UTC). |
| `data_inicio` | `datetime` | Não | Data/hora de início da execução. |
| `data_conclusao` | `datetime` | Não | Data/hora de conclusão da execução. |
| `prazo` | `datetime` | Sim | Data/hora limite para conclusão. |
| `prioridade` | `str enum` | Sim | Valores aceitos: `['baixa', 'média', 'alta']`. |
| `status` | `str enum` | Sim | Valores aceitos: `['concluida', 'pendente', 'cancelada']`. |

### 3.2 Saídas (Outputs)
O retorno da análise é estruturado no seguinte formato:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `tempo_medio_conclusao_min` | `float` | Tempo médio de conclusão em minutos (geral e por prioridade). |
| `taxa_atraso_percentual` | `float` | Percentual de tarefas concluídas após o prazo (geral e por prioridade). |
| `quantidade_tarefas` | `int` | Total de tarefas consideradas na análise (geral e por prioridade). |