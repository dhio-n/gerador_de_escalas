"""
Teste da Concatenação de Tipos de Escala
========================================

Testa a nova funcionalidade que concatena os tipos de escala quando há mudança
durante o período, separando por hífen.
"""

import sys
import os
from datetime import date, timedelta
import pandas as pd

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from escala_generator import GeradorEscala

def testar_concatencao_tipos():
    """Testa a concatenação de tipos de escala."""
    print("🧪 Testando concatenação de tipos de escala:")
    
    # Criar dados de teste
    colaboradores_teste = pd.DataFrame([
        {
            'Nome': 'João Silva',
            'Cargo': 'Enfermeiro',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Ultimo_Plantao_Mes_Anterior': '31/05/2025'
        },
        {
            'Nome': 'Maria Santos',
            'Cargo': 'Enfermeira',
            'Tipo_Escala': 'I_N',
            'Turno': 'Noite',
            'Ultimo_Plantao_Mes_Anterior': '30/06/2025'
        },
        {
            'Nome': 'Pedro Costa',
            'Cargo': 'Técnico',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Ultimo_Plantao_Mes_Anterior': ''
        }
    ])
    
    # Criar feriados de teste
    feriados_teste = pd.DataFrame([
        {'Data': '15/08/2025', 'Descricao': 'Feriado Nacional'},
        {'Data': '07/09/2025', 'Descricao': 'Independência do Brasil'}
    ])
    
    # Cenário 1: Período que atravessa meses com 31 dias
    print("\n📅 Cenário 1: Período que atravessa meses com 31 dias (Julho → Agosto)")
    data_inicio = date(2025, 7, 1)
    data_fim = date(2025, 8, 31)
    
    gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
    
    # Testar com cada colaborador
    for idx, colaborador in colaboradores_teste.iterrows():
        print(f"\n👤 Colaborador: {colaborador['Nome']}")
        print(f"   Tipo Original: {colaborador['Tipo_Escala']}")
        print(f"   Último Plantão: {colaborador['Ultimo_Plantao_Mes_Anterior']}")
        
        # Gerar escala para o colaborador
        escala_colaborador = gerador._gerar_escala_colaborador(colaborador)
        
        if not escala_colaborador.empty:
            # Verificar se há tipos concatenados
            tipos_unicos = escala_colaborador['Tipo_Escala'].unique()
            print(f"   Tipos na Escala: {tipos_unicos}")
            
            # Verificar se há concatenação
            for tipo in tipos_unicos:
                if ' - ' in str(tipo):
                    print(f"   ✅ CONCATENAÇÃO DETECTADA: {tipo}")
                else:
                    print(f"   ℹ️ Tipo único: {tipo}")
        else:
            print("   ❌ Nenhuma escala gerada")
    
    # Cenário 2: Período que não atravessa meses com 31 dias
    print("\n📅 Cenário 2: Período que não atravessa meses com 31 dias (Abril)")
    data_inicio = date(2025, 4, 1)
    data_fim = date(2025, 4, 30)
    
    gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
    
    for idx, colaborador in colaboradores_teste.iterrows():
        print(f"\n👤 Colaborador: {colaborador['Nome']}")
        print(f"   Tipo Original: {colaborador['Tipo_Escala']}")
        
        escala_colaborador = gerador._gerar_escala_colaborador(colaborador)
        
        if not escala_colaborador.empty:
            tipos_unicos = escala_colaborador['Tipo_Escala'].unique()
            print(f"   Tipos na Escala: {tipos_unicos}")
            
            for tipo in tipos_unicos:
                if ' - ' in str(tipo):
                    print(f"   ⚠️ CONCATENAÇÃO INESPERADA: {tipo}")
                else:
                    print(f"   ✅ Tipo único (esperado): {tipo}")
        else:
            print("   ❌ Nenhuma escala gerada")

def testar_cenarios_especificos():
    """Testa cenários específicos de concatenação."""
    print("\n🧪 Testando cenários específicos:")
    
    # Cenário: Janeiro (31 dias) → Fevereiro (28 dias) → Março (31 dias)
    print("\n📅 Cenário: Janeiro → Fevereiro → Março (período com 2 meses de 31 dias)")
    
    colaborador_teste = pd.Series({
        'Nome': 'Ana Teste',
        'Cargo': 'Enfermeira',
        'Tipo_Escala': 'P_D',
        'Turno': 'Dia',
        'Ultimo_Plantao_Mes_Anterior': '31/12/2024'
    })
    
    feriados_teste = pd.DataFrame([])
    data_inicio = date(2025, 1, 1)
    data_fim = date(2025, 3, 31)
    
    gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
    escala_colaborador = gerador._gerar_escala_colaborador(colaborador_teste)
    
    if not escala_colaborador.empty:
        tipos_unicos = escala_colaborador['Tipo_Escala'].unique()
        print(f"Tipos encontrados: {tipos_unicos}")
        
        for tipo in tipos_unicos:
            if ' - ' in str(tipo):
                print(f"✅ Concatenação: {tipo}")
                tipos_separados = tipo.split(' - ')
                print(f"   Tipos separados: {tipos_separados}")
            else:
                print(f"ℹ️ Tipo único: {tipo}")

def main():
    """Função principal do teste."""
    print("🚀 TESTE DA CONCATENAÇÃO DE TIPOS DE ESCALA")
    print("=" * 50)
    
    testar_concatencao_tipos()
    testar_cenarios_especificos()
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main() 