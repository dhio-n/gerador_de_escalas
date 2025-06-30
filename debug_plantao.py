"""
Debug Plantão
============

Este arquivo debuga exatamente o que está acontecendo com a função
determinar_tipo_plantao_automatico.
"""

import pandas as pd
from datetime import date, datetime
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def debug_plantao():
    """Debuga a função determinar_tipo_plantao_automatico."""
    print("=== DEBUG PLANTÃO ===")
    
    # Criar dados de teste
    dados_colaboradores = [
        {
            'Nome': 'Ana Costa',
            'Cargo': 'Supervisor',
            'Tipo_Escala': 'I_N',  # Ímpar Noite
            'Turno': 'Noite',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',  # Dia 30 (par)
        },
        {
            'Nome': 'Carlos Lima',
            'Cargo': 'Operador',
            'Tipo_Escala': 'P_D',  # Par Dia
            'Turno': 'Dia',
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',  # Dia 29 (ímpar)
        }
    ]
    
    # Criar gerador
    gerador = GeradorEscala(date(2025, 6, 1), date(2025, 6, 30), pd.DataFrame())
    
    print("🧪 Teste detalhado da função determinar_tipo_plantao_automatico:")
    print()
    
    for colaborador in dados_colaboradores:
        nome = colaborador['Nome']
        tipo_original = colaborador['Tipo_Escala']
        turno = colaborador['Turno']
        ultimo_plantao_str = colaborador['Ultimo_Plantao_Mes_Anterior']
        
        print(f"👤 {nome}:")
        print(f"   Tipo original: {tipo_original}")
        print(f"   Turno: {turno}")
        print(f"   Último plantão: {ultimo_plantao_str}")
        
        # Processar último plantão
        ultimo_plantao = None
        if ultimo_plantao_str and ultimo_plantao_str.strip():
            try:
                for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                    try:
                        ultimo_plantao = datetime.strptime(ultimo_plantao_str.strip(), formato).date()
                        break
                    except ValueError:
                        continue
            except:
                pass
        
        if ultimo_plantao:
            print(f"   Último plantão processado: {ultimo_plantao} (dia {ultimo_plantao.day})")
            print(f"   Dia é par? {ultimo_plantao.day % 2 == 0}")
            
            # Testar a função
            tipo_calculado = gerador.regras_clt.determinar_tipo_plantao_automatico(ultimo_plantao, turno)
            print(f"   Tipo calculado: {tipo_calculado}")
            
            # Verificar se deveria mudar
            if tipo_calculado != tipo_original:
                print(f"   ✅ DEVERIA MUDAR: {tipo_original} → {tipo_calculado}")
            else:
                print(f"   ❌ NÃO DEVERIA MUDAR: {tipo_original} = {tipo_calculado}")
        else:
            print(f"   ❌ Erro ao processar último plantão")
        
        print()
    
    # Testar a lógica manualmente
    print("🔍 Teste manual da lógica:")
    print("   Se último plantão foi em dia PAR (30), próximo deve ser ÍMPAR")
    print("   Se último plantão foi em dia ÍMPAR (29), próximo deve ser PAR")
    print()
    
    # Teste Ana Costa
    print("   Ana Costa (I_N, Noite, dia 30):")
    print("   - Dia 30 é par")
    print("   - Próximo deve ser ímpar")
    print("   - Turno Noite → I_N")
    print("   - Resultado esperado: I_N (não muda)")
    print("   - Resultado atual: P_N (muda)")
    print()
    
    # Teste Carlos Lima
    print("   Carlos Lima (P_D, Dia, dia 29):")
    print("   - Dia 29 é ímpar")
    print("   - Próximo deve ser par")
    print("   - Turno Dia → P_D")
    print("   - Resultado esperado: P_D (não muda)")
    print("   - Resultado atual: I_D (muda)")
    print()
    
    print("❓ PROBLEMA IDENTIFICADO:")
    print("   A lógica está invertida! Se o último plantão foi em dia par,")
    print("   o próximo plantão deve ser em dia par também (não ímpar).")
    print("   E vice-versa.")

if __name__ == "__main__":
    print("INICIANDO DEBUG PLANTÃO")
    print("=" * 80)
    
    debug_plantao()
    
    print("\n" + "=" * 80)
    print("✅ DEBUG CONCLUÍDO")
    print("=" * 80) 