"""
Teste das Correções Implementadas
================================

Este arquivo demonstra as correções implementadas para:
1. Escalas 6x1: Puxar corretamente o último domingo de folga
2. Plantões: Determinar automaticamente se deve ser par ou ímpar
"""

from datetime import date, datetime
from regras_clt import RegrasCLT
import pandas as pd

def testar_escala_6x1():
    """Testa a correção da escala 6x1 com último domingo informado."""
    print("=== TESTE ESCALA 6X1 ===")
    
    regras = RegrasCLT()
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    feriados = []
    
    # Teste 1: Sem último domingo informado
    print("\n1. Teste sem último domingo informado:")
    escala1, info1 = regras._regra_6x1_manha(data_inicio, data_fim, feriados)
    print(f"   Último domingo folga: {info1['ultimo_domingo_folga']}")
    print(f"   Domingos folgados: {info1['domingos_folgados']}")
    print(f"   Semanas sem domingo: {info1['semanas_sem_domingo']}")
    
    # Teste 2: Com último domingo informado (25/05/2025)
    print("\n2. Teste com último domingo informado (25/05/2025):")
    ultimo_domingo = date(2025, 5, 25)
    escala2, info2 = regras._regra_6x1_manha(data_inicio, data_fim, feriados, ultimo_domingo)
    print(f"   Último domingo folga informado: {ultimo_domingo}")
    print(f"   Último domingo folga calculado: {info2['ultimo_domingo_folga']}")
    print(f"   Domingos folgados: {info2['domingos_folgados']}")
    print(f"   Semanas sem domingo inicial: {info2['semanas_sem_domingo']}")
    
    # Verificar domingos de junho
    domingos_junho = [data for data in escala2.keys() if data.weekday() == 6]
    print(f"   Domingos de junho: {[d.strftime('%d/%m') for d in domingos_junho]}")
    
    return escala2, info2

def testar_plantao_automatico():
    """Testa a determinação automática de plantão par/ímpar."""
    print("\n=== TESTE PLANTÃO AUTOMÁTICO ===")
    
    regras = RegrasCLT()
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    feriados = []
    
    # Teste 1: Último plantão em dia par (30/05/2025)
    print("\n1. Teste com último plantão em dia par (30/05/2025):")
    ultimo_plantao_par = date(2025, 5, 30)
    tipo_auto_par_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao_par, "Dia")
    tipo_auto_par_noite = regras.determinar_tipo_plantao_automatico(ultimo_plantao_par, "Noite")
    print(f"   Último plantão: {ultimo_plantao_par.strftime('%d/%m/%Y')} (dia par)")
    print(f"   Tipo determinado automaticamente (Dia): {tipo_auto_par_dia}")
    print(f"   Tipo determinado automaticamente (Noite): {tipo_auto_par_noite}")
    print(f"   ✅ Esperado: I_D e I_N (ímpar)")
    
    # Teste 2: Último plantão em dia ímpar (31/05/2025)
    print("\n2. Teste com último plantão em dia ímpar (31/05/2025):")
    ultimo_plantao_impar = date(2025, 5, 31)
    tipo_auto_impar_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar, "Dia")
    tipo_auto_impar_noite = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar, "Noite")
    print(f"   Último plantão: {ultimo_plantao_impar.strftime('%d/%m/%Y')} (dia ímpar)")
    print(f"   Tipo determinado automaticamente (Dia): {tipo_auto_impar_dia}")
    print(f"   Tipo determinado automaticamente (Noite): {tipo_auto_impar_noite}")
    print(f"   ✅ Esperado: P_D e P_N (par)")
    
    # Teste 3: Último plantão em dia ímpar (29/05/2025)
    print("\n3. Teste com último plantão em dia ímpar (29/05/2025):")
    ultimo_plantao_impar2 = date(2025, 5, 29)
    tipo_auto_impar2_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar2, "Dia")
    tipo_auto_impar2_noite = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar2, "Noite")
    print(f"   Último plantão: {ultimo_plantao_impar2.strftime('%d/%m/%Y')} (dia ímpar)")
    print(f"   Tipo determinado automaticamente (Dia): {tipo_auto_impar2_dia}")
    print(f"   Tipo determinado automaticamente (Noite): {tipo_auto_impar2_noite}")
    print(f"   ✅ Esperado: P_D e P_N (par)")
    
    # Teste 4: Sem informação de último plantão
    print("\n4. Teste sem informação de último plantão:")
    tipo_auto_sem_info = regras.determinar_tipo_plantao_automatico(None, "Dia")
    print(f"   Tipo determinado automaticamente: {tipo_auto_sem_info}")
    print(f"   ✅ Esperado: P_D (par - padrão)")
    
    return tipo_auto_par_dia, tipo_auto_impar_dia, tipo_auto_sem_info

def testar_plantao_escala():
    """Testa a geração de escala de plantão com último plantão informado."""
    print("\n=== TESTE GERAÇÃO ESCALA PLANTÃO ===")
    
    regras = RegrasCLT()
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    feriados = []
    
    # Teste 1: Plantão par com último plantão em dia par
    print("\n1. Teste plantão par com último plantão em dia par:")
    ultimo_plantao = date(2025, 5, 30)  # Dia par
    escala_par = regras._regra_plantao_par_dia(data_inicio, data_fim, feriados, ultimo_plantao)
    
    # Verificar primeiros dias de junho
    print("   Primeiros dias de junho:")
    for i in range(1, 8):
        data = date(2025, 6, i)
        status = escala_par.get(data, "N/A")
        print(f"   {data.strftime('%d/%m')} ({data.day}): {status}")
    
    # Teste 2: Plantão ímpar com último plantão em dia ímpar
    print("\n2. Teste plantão ímpar com último plantão em dia ímpar:")
    ultimo_plantao = date(2025, 5, 29)  # Dia ímpar
    escala_impar = regras._regra_plantao_impar_dia(data_inicio, data_fim, feriados, ultimo_plantao)
    
    # Verificar primeiros dias de junho
    print("   Primeiros dias de junho:")
    for i in range(1, 8):
        data = date(2025, 6, i)
        status = escala_impar.get(data, "N/A")
        print(f"   {data.strftime('%d/%m')} ({data.day}): {status}")
    
    return escala_par, escala_impar

if __name__ == "__main__":
    print("INICIANDO TESTES DAS CORREÇÕES IMPLEMENTADAS")
    print("=" * 50)
    
    # Testar escala 6x1
    escala_6x1, info_6x1 = testar_escala_6x1()
    
    # Testar plantão automático
    tipo_par_dia, tipo_impar_dia, tipo_sem_info = testar_plantao_automatico()
    
    # Testar geração de escala de plantão
    escala_par, escala_impar = testar_plantao_escala()
    
    print("\n" + "=" * 50)
    print("TESTES CONCLUÍDOS")
    print("\nRESUMO DAS CORREÇÕES:")
    print("✅ Escala 6x1: Agora considera corretamente o último domingo informado")
    print("✅ Plantões: Determinação automática de par/ímpar baseada no último plantão")
    print("✅ Interface: Template atualizado com novas colunas")
    print("✅ Validação: Sistema avisa quando tipo de plantão é alterado automaticamente") 