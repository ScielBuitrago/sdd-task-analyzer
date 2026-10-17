"""Módulo de análise de produtividade para tarefas executadas.

Este módulo processa uma lista de tarefas e calcula indicadores de desempenho
como tempo médio de conclusão, taxa de atraso e consolidação por prioridade.

Attributes:
    logger: Logger do módulo para registrar avisos e eventos relevantes.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

VALID_PRIORIDADES: tuple[str, ...] = ("baixa", "média", "alta")
VALID_STATUS: tuple[str, ...] = ("concluida", "pendente", "cancelada")


class TaskValidationError(ValueError):
    """Exceção customizada para erros de validação de datas e integridade de tarefas."""
    pass


def _round_metric(value: float) -> float:
    """Arredonda valores numéricos para duas casas decimais."""
    return round(float(value), 2)


def _metricas_vazias() -> dict[str, float | int]:
    """Retorna a estrutura de métricas zeradas por prioridade."""
    return {
        "total_concluidas": 0,
        "tempo_medio_conclusao_min": 0.0,
        "tempo_medio_conclusao_horas": 0.0,
        "taxa_atraso_percentual": 0.0,
    }


def _calcular_indicadores_tarefas(concluidas: list[dict[str, Any]]) -> tuple[float, float, float, int]:
    """Calcula métricas para tarefas concluídas."""
    total_minutos = 0.0
    total_atrasadas = 0

    for tarefa in concluidas:
        data_criacao = tarefa.get("data_criacao")
        data_inicio = tarefa.get("data_inicio")
        data_conclusao = tarefa.get("data_conclusao")
        prazo = tarefa.get("prazo")

        # Validação de Inconsistência Temporal (Cenário 2)
        if isinstance(data_conclusao, datetime):
            if isinstance(data_criacao, datetime) and data_conclusao < data_criacao:
                raise TaskValidationError("data_conclusao não pode ser anterior a data_criacao")
            if isinstance(data_inicio, datetime) and data_conclusao < data_inicio:
                raise TaskValidationError("data_conclusao não pode ser anterior a data_inicio")

        ref_inicio = data_inicio if isinstance(data_inicio, datetime) else data_criacao

        if not isinstance(ref_inicio, datetime) or not isinstance(data_conclusao, datetime):
            logger.warning(
                "Tarefa ignorada por falta ou invalidade de datas para cálculo de tempo",
                extra={"id_tarefa": tarefa.get("id_tarefa")},
            )
            continue

        total_minutos += (data_conclusao - ref_inicio).total_seconds() / 60

        if isinstance(prazo, datetime) and data_conclusao > prazo:
            total_atrasadas += 1

    quantidade = len(concluidas)
    if quantidade == 0:
        return 0.0, 0.0, 0.0, 0

    tempo_medio_min = total_minutos / quantidade
    tempo_medio_horas = tempo_medio_min / 60
    taxa_atraso = (total_atrasadas / quantidade) * 100

    return (
        _round_metric(tempo_medio_min),
        _round_metric(tempo_medio_horas),
        _round_metric(taxa_atraso),
        quantidade,
    )


def _calcular_indicadores_por_prioridade(tarefas: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    """Agrupa indicadores por prioridade."""
    indicadores: dict[str, dict[str, float | int]] = {}

    for prioridade in VALID_PRIORIDADES:
        tarefas_prioridade = [
            tarefa for tarefa in tarefas 
            if isinstance(tarefa, dict) and tarefa.get("status") == "concluida" and tarefa.get("prioridade") == prioridade
        ]

        if not tarefas_prioridade:
            indicadores[prioridade] = _metricas_vazias()
            continue

        tempo_min, tempo_horas, taxa_atraso, quantidade = _calcular_indicadores_tarefas(tarefas_prioridade)
        indicadores[prioridade] = {
            "total_concluidas": quantidade,
            "quantidade_tarefas": quantidade,
            "tempo_medio_conclusao_min": tempo_min,
            "tempo_medio_conclusao_horas": tempo_horas,
            "taxa_atraso_percentual": taxa_atraso,
        }

    return indicadores


def analisar_tarefas(tarefas: list[dict[str, Any]]) -> dict[str, Any]:
    """Processa a lista de tarefas e retorna os indicadores consolidados."""
    # Caso de borda: entrada vazia
    if not tarefas:
        indicadores_vazios = {p: _metricas_vazias() for p in VALID_PRIORIDADES}
        return {
            "total_tarefas": 0,
            "total_concluidas": 0,
            "total_pendentes": 0,
            "quantidade_tarefas": 0,
            "tempo_medio_conclusao_min": 0.0,
            "tempo_medio_conclusao_horas": 0.0,
            "taxa_atraso_percentual": 0.0,
            "indicadores_por_prioridade": indicadores_vazios,
        }

    total_tarefas = len(tarefas)
    concluidas = [t for t in tarefas if isinstance(t, dict) and t.get("status") == "concluida"]
    pendentes = [t for t in tarefas if isinstance(t, dict) and t.get("status") == "pendente"]

    total_concluidas = len(concluidas)
    total_pendentes = len(pendentes)

    # Validação de datas antes do cálculo acumulado
    tempo_min, tempo_horas, taxa_atraso, quantidade = _calcular_indicadores_tarefas(concluidas)
    indicadores_por_prioridade = _calcular_indicadores_por_prioridade(tarefas)

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "quantidade_tarefas": quantidade,
        "tempo_medio_conclusao_min": tempo_min,
        "tempo_medio_conclusao_horas": tempo_horas,
        "taxa_atraso_percentual": taxa_atraso,
        "indicadores_por_prioridade": indicadores_por_prioridade,
    }


__all__ = ["analisar_tarefas", "TaskValidationError"]