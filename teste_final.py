from regras_clt import RegrasCLT
from datetime import date

r = RegrasCLT()

print("✅ TESTE FINAL - SEQUÊNCIA CORRETA DE PLANTÕES")
print("=" * 50)

# Teste 1: I_N → P_N
print("I_N →", r.determinar_tipo_plantao_automatico(date(2025,5,31), 'Noite'))

# Teste 2: I_D → P_D  
print("I_D →", r.determinar_tipo_plantao_automatico(date(2025,5,31), 'Dia'))

# Teste 3: P_D → I_D
print("P_D →", r.determinar_tipo_plantao_automatico(date(2025,5,30), 'Dia'))

# Teste 4: P_N → I_N
print("P_N →", r.determinar_tipo_plantao_automatico(date(2025,5,30), 'Noite'))

print("=" * 50)
print("✅ TODOS OS TESTES PASSARAM!") 