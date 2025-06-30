#!/usr/bin/env python3
"""
Teste simples para demonstrar a lógica de mudança de plantão.
"""

from datetime import date, timedelta
from regras_clt import RegrasCLT

def testar_exemplos():
    """Testa exemplos específicos da lógica."""
    
    regras = RegrasCLT()
    
    print("=== LOGICA DE MUDANCA DE PLANTAO ===")
    print("Regra: Só muda quando o mes anterior tem 31 dias")
    print()
    
    # Exemplo 1: Janeiro (31 dias) -> Fevereiro
    print("EXEMPLO 1:")
    print("Ultimo plantao: 31/01/2024 (dia impar)")
    print("Janeiro tem 31 dias -> DEVE MUDAR")
    
    ultimo = date(2024, 1, 31)
    tipo = regras.determinar_tipo_plantao_automatico(ultimo, "Dia")
    print(f"Proximo plantao: {tipo}")
    print()
    
    # Exemplo 2: Junho (30 dias) -> Julho  
    print("EXEMPLO 2:")
    print("Ultimo plantao: 30/06/2024 (dia par)")
    print("Junho tem 30 dias -> NAO MUDA")
    
    ultimo = date(2024, 6, 30)
    tipo = regras.determinar_tipo_plantao_automatico(ultimo, "Dia")
    print(f"Proximo plantao: {tipo}")
    print()
    
    # Exemplo 3: Julho (31 dias) -> Agosto
    print("EXEMPLO 3:")
    print("Ultimo plantao: 31/07/2024 (dia impar)")
    print("Julho tem 31 dias -> DEVE MUDAR")
    
    ultimo = date(2024, 7, 31)
    tipo = regras.determinar_tipo_plantao_automatico(ultimo, "Dia")
    print(f"Proximo plantao: {tipo}")
    print()
    
    # Exemplo 4: Abril (30 dias) -> Maio
    print("EXEMPLO 4:")
    print("Ultimo plantao: 30/04/2024 (dia par)")
    print("Abril tem 30 dias -> NAO MUDA")
    
    ultimo = date(2024, 4, 30)
    tipo = regras.determinar_tipo_plantao_automatico(ultimo, "Dia")
    print(f"Proximo plantao: {tipo}")
    print()

if __name__ == "__main__":
    testar_exemplos() 