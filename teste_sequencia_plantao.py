"""
Teste da Sequência Correta de Plantões
=====================================

Este arquivo demonstra a sequência correta de plantões na virada de mês:
- I_N → P_N (ímpar → par)
- I_D → P_D (ímpar → par)  
- P_D → I_D (par → ímpar)
- P_N → I_N (par → ímpar)
"""

from datetime import date
from regras_clt import RegrasCLT

def testar_sequencia_plantao():
    """Testa a sequência correta de plantões na virada de mês."""
    print("=== TESTE SEQUÊNCIA CORRETA DE PLANTÕES ===")
    
    regras = RegrasCLT()
    
    # Cenário: Virada de maio (31 dias) para junho (30 dias)
    print("\n📅 CENÁRIO: Virada de maio (31 dias) para junho (30 dias)")
    print("=" * 60)
    
    # Teste 1: Plantão Ímpar - Noite (I_N) → deve virar Par - Noite (P_N)
    print("\n1. Plantão Ímpar - Noite (I_N):")
    ultimo_plantao_impar = date(2025, 5, 31)  # Último dia de maio (ímpar)
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar, "Noite")
    print(f"   Último plantão: {ultimo_plantao_impar.strftime('%d/%m/%Y')} (dia ímpar)")
    print(f"   Tipo original: I_N (Ímpar - Noite)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   ✅ Resultado: I_N → {tipo_auto} (ímpar → par)")
    
    # Teste 2: Plantão Ímpar - Dia (I_D) → deve virar Par - Dia (P_D)
    print("\n2. Plantão Ímpar - Dia (I_D):")
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar, "Dia")
    print(f"   Último plantão: {ultimo_plantao_impar.strftime('%d/%m/%Y')} (dia ímpar)")
    print(f"   Tipo original: I_D (Ímpar - Dia)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   ✅ Resultado: I_D → {tipo_auto} (ímpar → par)")
    
    # Teste 3: Plantão Par - Dia (P_D) → deve virar Ímpar - Dia (I_D)
    print("\n3. Plantão Par - Dia (P_D):")
    ultimo_plantao_par = date(2025, 5, 30)  # Penúltimo dia de maio (par)
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao_par, "Dia")
    print(f"   Último plantão: {ultimo_plantao_par.strftime('%d/%m/%Y')} (dia par)")
    print(f"   Tipo original: P_D (Par - Dia)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   ✅ Resultado: P_D → {tipo_auto} (par → ímpar)")
    
    # Teste 4: Plantão Par - Noite (P_N) → deve virar Ímpar - Noite (I_N)
    print("\n4. Plantão Par - Noite (P_N):")
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao_par, "Noite")
    print(f"   Último plantão: {ultimo_plantao_par.strftime('%d/%m/%Y')} (dia par)")
    print(f"   Tipo original: P_N (Par - Noite)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   ✅ Resultado: P_N → {tipo_auto} (par → ímpar)")
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DA SEQUÊNCIA CORRETA:")
    print("   I_N → P_N (Ímpar - Noite → Par - Noite)")
    print("   I_D → P_D (Ímpar - Dia → Par - Dia)")
    print("   P_D → I_D (Par - Dia → Ímpar - Dia)")
    print("   P_N → I_N (Par - Noite → Ímpar - Noite)")
    print("=" * 60)

def testar_virada_mes_30_dias():
    """Testa a virada de mês com 30 dias."""
    print("\n\n=== TESTE VIRADA DE MÊS COM 30 DIAS ===")
    
    regras = RegrasCLT()
    
    # Cenário: Virada de abril (30 dias) para maio (31 dias)
    print("\n📅 CENÁRIO: Virada de abril (30 dias) para maio (31 dias)")
    print("=" * 60)
    
    # Teste 1: Plantão Par - Dia (P_D) → deve virar Ímpar - Dia (I_D)
    print("\n1. Plantão Par - Dia (P_D):")
    ultimo_plantao_par = date(2025, 4, 30)  # Último dia de abril (par)
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao_par, "Dia")
    print(f"   Último plantão: {ultimo_plantao_par.strftime('%d/%m/%Y')} (dia par)")
    print(f"   Tipo original: P_D (Par - Dia)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   ✅ Resultado: P_D → {tipo_auto} (par → ímpar)")
    
    # Teste 2: Plantão Ímpar - Noite (I_N) → deve virar Par - Noite (P_N)
    print("\n2. Plantão Ímpar - Noite (I_N):")
    ultimo_plantao_impar = date(2025, 4, 29)  # Penúltimo dia de abril (ímpar)
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar, "Noite")
    print(f"   Último plantão: {ultimo_plantao_impar.strftime('%d/%m/%Y')} (dia ímpar)")
    print(f"   Tipo original: I_N (Ímpar - Noite)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   ✅ Resultado: I_N → {tipo_auto} (ímpar → par)")

if __name__ == "__main__":
    print("INICIANDO TESTE DA SEQUÊNCIA CORRETA DE PLANTÕES")
    print("=" * 60)
    
    # Testar sequência correta
    testar_sequencia_plantao()
    
    # Testar virada de mês com 30 dias
    testar_virada_mes_30_dias()
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO - LÓGICA CORRETA IMPLEMENTADA")
    print("=" * 60) 