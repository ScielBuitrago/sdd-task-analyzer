"""
Ficheiro de Testes Automatizados (Test Harness) para o Módulo TaskAnalyzer.

Implementa a suíte de testes com pytest traduzindo diretamente os cenários
de aceite e casos de borda definidos na especificação.
"""

from datetime import datetime, timezone, timedelta
import pytest

# Importação da função principal e da exceção customizada do módulo src/
from src.task_analyzer import analisar_tarefas, TaskValidationError


# ==============================================================================
# FIXTURES (Preparação de Dados)
# ==============================================================================

@pytest.fixture
def conjunto_tarefas_validas() -> list[dict]:
    """
    Conjunto de tarefas válidas com diferentes prioridades, prazos e status.
    """
    agora = datetime.now(timezone.utc)
    
    return [
        # Tarefa 1: Concluída No Prazo | Prioridade: alta | Duração: 2 horas
        {
            "id_tarefa": 1,
            "data_criacao": agora - timedelta(hours=5),
            "data_inicio": agora - timedelta(hours=3),
            "data_conclusao": agora - timedelta(hours=1), # 2 horas
            "prazo": agora,
            "prioridade": "alta",
            "status": "concluida"
        },
        # Tarefa 2: Concluída Com Atraso | Prioridade: alta | Duração: 4 horas
        {
            "id_tarefa": 2,
            "data_criacao": agora - timedelta(hours=10),
            "data_inicio": agora - timedelta(hours=8),
            "data_conclusao": agora - timedelta(hours=4), # 4 horas
            "prazo": agora - timedelta(hours=6), # Atrasada
            "prioridade": "alta",
            "status": "concluida"
        },
        # Tarefa 3: Concluída No Prazo | Prioridade: baixa | Duração: 1 hora
        {
            "id_tarefa": 3,
            "data_criacao": agora - timedelta(hours=3),
            "data_inicio": agora - timedelta(hours=2),
            "data_conclusao": agora - timedelta(hours=1), # 1 hora
            "prazo": agora,
            "prioridade": "baixa",
            "status": "concluida"
        },
        # Tarefa 4: Pendente | Prioridade: média
        {
            "id_tarefa": 4,
            "data_criacao": agora - timedelta(hours=1),
            "data_inicio": None,
            "data_conclusao": None,
            "prazo": agora + timedelta(hours=2),
            "prioridade": "média",
            "status": "pendente"
        }
    ]


# ==============================================================================
# 1. TESTE DE SUCESSO (CENÁRIO 1)
# ==============================================================================

def test_cenario_1_sucesso_calculo_metricas(conjunto_tarefas_validas):
    """
    Validação dos cálculos de total_tarefas, total_concluidas, total_pendentes,
    tempo_medio_conclusao_horas (geral e por prioridade) e taxa_atraso_percentual.
    """
    resultado = analisar_tarefas(conjunto_tarefas_validas)
    
    # Validações de Totais Globais
    assert resultado["total_tarefas"] == 4
    assert resultado["total_concluidas"] == 3
    assert resultado["total_pendentes"] == 1
    
    # Média de Tempo Geral: (2h + 4h + 1h) / 3 = 2.33 horas
    assert resultado["tempo_medio_conclusao_horas"] == 2.33
    
    # Taxa de Atraso Geral: 1 atrasada em 3 concluídas = 33.33%
    assert resultado["taxa_atraso_percentual"] == 33.33
    
    # Validações por Prioridade (Exemplo: Alta)
    indicadores = resultado["indicadores_por_prioridade"]
    assert indicadores["alta"]["total_concluidas"] == 2
    assert indicadores["alta"]["tempo_medio_conclusao_horas"] == 3.0  # (2h + 4h) / 2
    assert indicadores["alta"]["taxa_atraso_percentual"] == 50.0       # 1 em 2 atrasadas


# ==============================================================================
# 2. TESTE DE EXCEÇÃO / ERRO (CENÁRIO 2)
# ==============================================================================

def test_cenario_2_excecao_data_conclusao_anterior_criacao():
    """
    Validação de datas inconsistentes (data_conclusao < data_criacao)
    disparando a exceção TaskValidationError.
    """
    agora = datetime.now(timezone.utc)
    tarefa_invalida = [{
        "id_tarefa": 5,
        "data_criacao": agora,
        "data_inicio": agora - timedelta(hours=1),
        "data_conclusao": agora - timedelta(hours=2),  # Conclusão ANTES da criação
        "prazo": agora + timedelta(hours=5),
        "prioridade": "alta",
        "status": "concluida"
    }]
    
    with pytest.raises(TaskValidationError, match="data_conclusao não pode ser anterior a data_criacao"):
        analisar_tarefas(tarefa_invalida)


# ==============================================================================
# 3. TESTE DE CASOS DE BORDA
# ==============================================================================

def test_caso_de_borda_entrada_vazia():
    """
    Validação de entradas vazias, garantindo retorno de 0.0 para médias
    sem lançar exceções não tratadas.
    """
    resultado = analisar_tarefas([])
    
    assert resultado["total_tarefas"] == 0
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 0
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0


def test_caso_de_borda_apenas_tarefas_pendentes():
    """
    Validação de listas contendo apenas tarefas pendentes, garantindo
    retorno de 0.0 para médias sem lançar exceções não tratadas (divisão por zero).
    """
    agora = datetime.now(timezone.utc)
    tarefas_pendentes = [
        {
            "id_tarefa": 6,
            "data_criacao": agora,
            "data_inicio": None,
            "data_conclusao": None,
            "prazo": agora + timedelta(days=1),
            "prioridade": "baixa",
            "status": "pendente"
        }
    ]
    
    resultado = analisar_tarefas(tarefas_pendentes)
    
    assert resultado["total_tarefas"] == 1
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 1
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0