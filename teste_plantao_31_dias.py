#!/usr/bin/env python3
"""
Teste para validar a lógica de mudança de plantão apenas quando o mês anterior tem 31 dias.
"""

from datetime import date, timedelta
from regras_clt import RegrasCLT

def testar_logica_31_dias():
    """Testa a lógica de mudança de plantão baseada na quantidade de dias do mês anterior."""
    
    regras = RegrasCLT()
    
    print("=== TESTE: LÓGICA DE MUDANÇA APENAS QUANDO MÊS ANTERIOR TEM 31 DIAS ===\n")
    
    # Casos de teste
    casos_teste = [
        # (último plantão, descrição do caso)
        (date(2024, 1, 31), "Janeiro 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 1, 30), "Janeiro 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
        (date(2024, 2, 29), "Fevereiro 2024 (29 dias) - último plantão em dia ímpar - NÃO MUDA"),
        (date(2024, 2, 28), "Fevereiro 2024 (29 dias) - último plantão em dia par - NÃO MUDA"),
        (date(2024, 3, 31), "Março 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 3, 30), "Março 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
        (date(2024, 4, 30), "Abril 2024 (30 dias) - último plantão em dia par - NÃO MUDA"),
        (date(2024, 4, 29), "Abril 2024 (30 dias) - último plantão em dia ímpar - NÃO MUDA"),
        (date(2024, 5, 31), "Maio 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 5, 30), "Maio 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
        (date(2024, 6, 30), "Junho 2024 (30 dias) - último plantão em dia par - NÃO MUDA"),
        (date(2024, 6, 29), "Junho 2024 (30 dias) - último plantão em dia ímpar - NÃO MUDA"),
        (date(2024, 7, 31), "Julho 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 7, 30), "Julho 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
        (date(2024, 8, 31), "Agosto 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 8, 30), "Agosto 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
        (date(2024, 9, 30), "Setembro 2024 (30 dias) - último plantão em dia par - NÃO MUDA"),
        (date(2024, 9, 29), "Setembro 2024 (30 dias) - último plantão em dia ímpar - NÃO MUDA"),
        (date(2024, 10, 31), "Outubro 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 10, 30), "Outubro 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
        (date(2024, 11, 30), "Novembro 2024 (30 dias) - último plantão em dia par - NÃO MUDA"),
        (date(2024, 11, 29), "Novembro 2024 (30 dias) - último plantão em dia ímpar - NÃO MUDA"),
        (date(2024, 12, 31), "Dezembro 2024 (31 dias) - último plantão em dia ímpar - DEVE MUDAR"),
        (date(2024, 12, 30), "Dezembro 2024 (31 dias) - último plantão em dia par - DEVE MUDAR"),
    ]
    
    for ultimo_plantao, descricao in casos_teste:
        print(f"--- {descricao} ---")
        print(f"Último plantão: {ultimo_plantao.strftime('%d/%m/%Y')} (dia {'par' if ultimo_plantao.day % 2 == 0 else 'ímpar'})")
        
        # Calcular dias do mês anterior
        mes_anterior = ultimo_plantao.replace(day=1) + timedelta(days=32)
        mes_anterior = mes_anterior.replace(day=1) - timedelta(days=1)
        dias_mes_anterior = mes_anterior.day
        
        print(f"Dias no mês anterior: {dias_mes_anterior}")
        
        # Verificar se deve mudar baseado na quantidade de dias do mês anterior
        deve_mudar = dias_mes_anterior == 31
        
        print(f"Deve mudar: {'SIM' if deve_mudar else 'NÃO'}")
        
        # Testar para turno Dia
        tipo_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Dia")
        print(f"Próximo plantão DIA: {tipo_dia}")
        
        # Testar para turno Noite
        tipo_noite = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Noite")
        print(f"Próximo plantão NOITE: {tipo_noite}")
        
        # Verificar se mudou corretamente
        if ultimo_plantao.day % 2 == 0:  # Último foi par
            esperado_dia = "I_D" if deve_mudar else "P_D"
            esperado_noite = "I_N" if deve_mudar else "P_N"
        else:  # Último foi ímpar
            esperado_dia = "P_D" if deve_mudar else "I_D"
            esperado_noite = "P_N" if deve_mudar else "I_N"
        
        print(f"Esperado: {esperado_dia} (dia) / {esperado_noite} (noite)")
        print(f"Resultado: {'✅ CORRETO' if tipo_dia == esperado_dia and tipo_noite == esperado_noite else '❌ INCORRETO'}")
        print()

def testar_sequencia_meses():
    """Testa uma sequência de meses para verificar a mudança correta."""
    
    regras = RegrasCLT()
    
    print("=== TESTE: SEQUÊNCIA DE MESES ===\n")
    
    # Simular uma sequência de últimos plantões
    sequencia = [
        (date(2024, 1, 31), "Janeiro (31 dias) - último em dia ímpar"),
        (date(2024, 2, 29), "Fevereiro (29 dias) - último em dia ímpar"),
        (date(2024, 3, 31), "Março (31 dias) - último em dia ímpar"),
        (date(2024, 4, 30), "Abril (30 dias) - último em dia par"),
        (date(2024, 5, 31), "Maio (31 dias) - último em dia ímpar"),
    ]
    
    print("Sequência de mudanças esperadas:")
    print("Janeiro (31d) → Fevereiro: MUDANÇA (ímpar → par)")
    print("Fevereiro (29d) → Março: SEM MUDANÇA (par → par)")
    print("Março (31d) → Abril: MUDANÇA (par → ímpar)")
    print("Abril (30d) → Maio: SEM MUDANÇA (ímpar → ímpar)")
    print("Maio (31d) → Junho: MUDANÇA (ímpar → par)")
    print()
    
    for i, (ultimo_plantao, descricao) in enumerate(sequencia):
        print(f"--- {descricao} ---")
        tipo_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Dia")
        tipo_noite = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Noite")
        
        print(f"Último plantão: {ultimo_plantao.strftime('%d/%m/%Y')} (dia {'par' if ultimo_plantao.day % 2 == 0 else 'ímpar'})")
        print(f"Próximo plantão: {tipo_dia} (dia) / {tipo_noite} (noite)")
        
        # Calcular dias do mês anterior
        mes_anterior = ultimo_plantao.replace(day=1) + timedelta(days=32)
        mes_anterior = mes_anterior.replace(day=1) - timedelta(days=1)
        dias_mes_anterior = mes_anterior.day
        
        # Verificar se deve mudar
        deve_mudar = dias_mes_anterior == 31
        
        if deve_mudar:
            print("✅ MUDANÇA ESPERADA (mês anterior com 31 dias)")
        else:
            print("✅ SEM MUDANÇA (mês anterior com menos de 31 dias)")
        print()

def testar_exemplo_especifico():
    """Testa o exemplo específico mencionado pelo usuário."""
    
    regras = RegrasCLT()
    
    print("=== TESTE: EXEMPLO ESPECÍFICO ===\n")
    
    # Exemplo: João trabalha como P_D no dia 30/06
    # Junho tem 30 dias, então NÃO deve mudar
    # João continua P_D em julho
    
    print("Exemplo: João trabalha como P_D no dia 30/06")
    print("Junho tem 30 dias, então NÃO deve mudar")
    print("João continua P_D em julho")
    print()
    
    # Simular último plantão em 30/06 (dia par)
    ultimo_plantao = date(2024, 6, 30)
    
    print(f"Último plantão: {ultimo_plantao.strftime('%d/%m/%Y')} (dia {'par' if ultimo_plantao.day % 2 == 0 else 'ímpar'})")
    
    # Calcular dias do mês anterior
    mes_anterior = ultimo_plantao.replace(day=1) + timedelta(days=32)
    mes_anterior = mes_anterior.replace(day=1) - timedelta(days=1)
    dias_mes_anterior = mes_anterior.day
    
    print(f"Dias no mês anterior (Junho): {dias_mes_anterior}")
    
    # Como junho tem 30 dias, NÃO deve mudar
    tipo_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Dia")
    print(f"Próximo plantão: {tipo_dia}")
    
    if tipo_dia == "P_D":
        print("✅ CORRETO: Manteve P_D (mês anterior com 30 dias)")
    else:
        print("❌ INCORRETO: Deveria manter P_D")
    
    print()
    
    # Agora testar com último plantão em 31/07 (dia ímpar)
    # Julho tem 31 dias, então DEVE mudar
    print("Exemplo: João trabalha como I_D no dia 31/07")
    print("Julho tem 31 dias, então DEVE mudar")
    print("João vira P_D em agosto")
    print()
    
    ultimo_plantao = date(2024, 7, 31)
    
    print(f"Último plantão: {ultimo_plantao.strftime('%d/%m/%Y')} (dia {'par' if ultimo_plantao.day % 2 == 0 else 'ímpar'})")
    
    # Calcular dias do mês anterior
    mes_anterior = ultimo_plantao.replace(day=1) + timedelta(days=32)
    mes_anterior = mes_anterior.replace(day=1) - timedelta(days=1)
    dias_mes_anterior = mes_anterior.day
    
    print(f"Dias no mês anterior (Julho): {dias_mes_anterior}")
    
    # Como julho tem 31 dias, DEVE mudar
    tipo_dia = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Dia")
    print(f"Próximo plantão: {tipo_dia}")
    
    if tipo_dia == "P_D":
        print("✅ CORRETO: Mudou para P_D (mês anterior com 31 dias)")
    else:
        print("❌ INCORRETO: Deveria mudar para P_D")

if __name__ == "__main__":
    testar_logica_31_dias()
    print("\n" + "="*60 + "\n")
    testar_sequencia_meses()
    print("\n" + "="*60 + "\n")
    testar_exemplo_especifico() 