"""
Teste da Lógica de Alternância de Plantão - Mês Anterior
========================================================

Testa a nova implementação da regra de alternância que considera o mês anterior
para determinar se deve inverter a paridade dos plantões.
"""

import sys
import os
from datetime import date, timedelta

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_verificacao_mes_anterior():
    """Testa a função _verificar_mes_anterior_31_dias."""
    print("🧪 Testando verificação de mês anterior com 31 dias:")
    
    # Criar instância do gerador (datas não importam para este teste)
    gerador = GeradorEscala(date(2025, 1, 1), date(2025, 1, 31), None)
    
    # Testes para diferentes datas de início
    testes = [
        # (data_inicio, esperado, descricao)
        (date(2025, 2, 1), True, "Fevereiro 2025 (mês anterior: Janeiro com 31 dias)"),
        (date(2025, 4, 1), True, "Abril 2025 (mês anterior: Março com 31 dias)"),
        (date(2025, 6, 1), True, "Junho 2025 (mês anterior: Maio com 31 dias)"),
        (date(2025, 8, 1), True, "Agosto 2025 (mês anterior: Julho com 31 dias)"),
        (date(2025, 9, 1), True, "Setembro 2025 (mês anterior: Agosto com 31 dias)"),
        (date(2025, 11, 1), True, "Novembro 2025 (mês anterior: Outubro com 31 dias)"),
        (date(2025, 12, 1), False, "Dezembro 2025 (mês anterior: Novembro com 30 dias)"),
        (date(2025, 3, 1), False, "Março 2025 (mês anterior: Fevereiro com 28 dias)"),
        (date(2025, 5, 1), False, "Maio 2025 (mês anterior: Abril com 30 dias)"),
        (date(2025, 7, 1), False, "Julho 2025 (mês anterior: Junho com 30 dias)"),
        (date(2025, 10, 1), False, "Outubro 2025 (mês anterior: Setembro com 30 dias)"),
    ]
    
    for data_inicio, esperado, descricao in testes:
        resultado = gerador._verificar_mes_anterior_31_dias(data_inicio)
        status = "✅" if resultado == esperado else "❌"
        print(f"{status} {descricao}: {resultado} (esperado: {esperado})")

def testar_determinacao_tipo_plantao_inicial():
    """Testa a função _determinar_tipo_plantao_inicial."""
    print("\n🧪 Testando determinação do tipo de plantão inicial:")
    
    # Criar instância do gerador
    gerador = GeradorEscala(date(2025, 1, 1), date(2025, 1, 31), None)
    
    # Testes para diferentes cenários
    testes = [
        # (tipo_original, data_inicio, ultimo_plantao, esperado, descricao)
        ("P_D", date(2025, 2, 1), None, "I_D", "P_D → I_D (mês anterior com 31 dias)"),
        ("P_N", date(2025, 2, 1), None, "I_N", "P_N → I_N (mês anterior com 31 dias)"),
        ("I_D", date(2025, 2, 1), None, "P_D", "I_D → P_D (mês anterior com 31 dias)"),
        ("I_N", date(2025, 2, 1), None, "P_N", "I_N → P_N (mês anterior com 31 dias)"),
        ("P_D", date(2025, 3, 1), None, "P_D", "P_D → P_D (mês anterior com 28 dias)"),
        ("P_N", date(2025, 3, 1), None, "P_N", "P_N → P_N (mês anterior com 28 dias)"),
        ("I_D", date(2025, 3, 1), None, "I_D", "I_D → I_D (mês anterior com 28 dias)"),
        ("I_N", date(2025, 3, 1), None, "I_N", "I_N → I_N (mês anterior com 28 dias)"),
        ("M44", date(2025, 2, 1), None, "M44", "M44 → M44 (não é plantão)"),
        ("T6X1", date(2025, 2, 1), None, "T6X1", "T6X1 → T6X1 (não é plantão)"),
    ]
    
    for tipo_original, data_inicio, ultimo_plantao, esperado, descricao in testes:
        resultado = gerador._determinar_tipo_plantao_inicial(tipo_original, data_inicio, ultimo_plantao)
        status = "✅" if resultado == esperado else "❌"
        print(f"{status} {descricao}: {resultado} (esperado: {esperado})")

def testar_cenarios_completos():
    """Testa cenários completos de alternância."""
    print("\n🧪 Testando cenários completos de alternância:")
    
    # Cenário 1: Janeiro (31 dias) → Fevereiro (28 dias)
    print("\n📅 Cenário 1: Janeiro (31 dias) → Fevereiro (28 dias)")
    gerador = GeradorEscala(date(2025, 2, 1), date(2025, 2, 28), None)
    
    # Simular colaborador com P_D
    tipo_original = "P_D"
    tipo_ajustado = gerador._determinar_tipo_plantao_inicial(tipo_original, date(2025, 2, 1))
    print(f"Tipo original: {tipo_original}")
    print(f"Tipo ajustado: {tipo_ajustado}")
    print(f"Deve alternar: {'Sim' if tipo_ajustado != tipo_original else 'Não'}")
    
    # Cenário 2: Março (31 dias) → Abril (30 dias)
    print("\n📅 Cenário 2: Março (31 dias) → Abril (30 dias)")
    gerador = GeradorEscala(date(2025, 4, 1), date(2025, 4, 30), None)
    
    tipo_original = "I_N"
    tipo_ajustado = gerador._determinar_tipo_plantao_inicial(tipo_original, date(2025, 4, 1))
    print(f"Tipo original: {tipo_original}")
    print(f"Tipo ajustado: {tipo_ajustado}")
    print(f"Deve alternar: {'Sim' if tipo_ajustado != tipo_original else 'Não'}")
    
    # Cenário 3: Abril (30 dias) → Maio (31 dias)
    print("\n📅 Cenário 3: Abril (30 dias) → Maio (31 dias)")
    gerador = GeradorEscala(date(2025, 5, 1), date(2025, 5, 31), None)
    
    tipo_original = "P_D"
    tipo_ajustado = gerador._determinar_tipo_plantao_inicial(tipo_original, date(2025, 5, 1))
    print(f"Tipo original: {tipo_original}")
    print(f"Tipo ajustado: {tipo_ajustado}")
    print(f"Deve alternar: {'Sim' if tipo_ajustado != tipo_original else 'Não'}")

def main():
    """Função principal do teste."""
    print("🚀 TESTE DA LÓGICA DE ALTERNÂNCIA DE PLANTÃO - MÊS ANTERIOR")
    print("=" * 70)
    
    testar_verificacao_mes_anterior()
    testar_determinacao_tipo_plantao_inicial()
    testar_cenarios_completos()
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main() 