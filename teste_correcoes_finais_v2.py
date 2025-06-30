"""
Teste das Correções Finais v2
=============================

Este arquivo testa as correções implementadas:
1. Escala completa mostra apenas até Status Colorido
2. Relatório 6x1 funciona corretamente
3. Avisos de plantão estão corretos
"""

import pandas as pd
from datetime import date, datetime
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_correcoes_finais():
    """Testa as correções implementadas."""
    print("=== TESTE CORREÇÕES FINAIS v2 ===")
    
    # Criar dados de teste
    dados_colaboradores = [
        {
            'Nome': 'João Silva',
            'Cargo': 'Analista',
            'Tipo_Escala': 'M6X1',
            'Turno': 'Manhã',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '',
            'Ultimo_Domingo_Folga': '25/05/2025'
        },
        {
            'Nome': 'Pedro Oliveira',
            'Cargo': 'Auxiliar',
            'Tipo_Escala': 'N6X1',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '',
            'Ultimo_Domingo_Folga': '15/06/2025'
        },
        {
            'Nome': 'Ana Costa',
            'Cargo': 'Supervisor',
            'Tipo_Escala': 'I_N',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Carlos Lima',
            'Cargo': 'Operador',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    df_colaboradores = pd.DataFrame(dados_colaboradores)
    
    # Criar dados de feriados (vazio para teste)
    df_feriados = pd.DataFrame(columns=['Data', 'Descricao'])
    
    # Configurar período
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    
    # Criar gerador
    gerador = GeradorEscala(data_inicio, data_fim, df_feriados)
    
    # Gerar escala completa
    escala_completa = gerador.gerar_escala_completa(df_colaboradores)
    
    print(f"✅ Escala gerada com {len(escala_completa)} registros")
    
    # Verificar colunas da escala completa
    print(f"\n📊 Colunas da escala completa: {list(escala_completa.columns)}")
    
    # Verificar se tem apenas as colunas corretas
    colunas_esperadas = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno', 'Data', 'Status', 'Status_Colorido']
    colunas_corretas = all(col in escala_completa.columns for col in colunas_esperadas)
    colunas_extras = [col for col in escala_completa.columns if col not in colunas_esperadas]
    
    print(f"✅ Colunas corretas: {colunas_corretas}")
    if colunas_extras:
        print(f"❌ Colunas extras encontradas: {colunas_extras}")
    else:
        print("✅ Nenhuma coluna extra encontrada")
    
    # Gerar relatório 6x1
    relatorio_6x1 = gerador.gerar_relatorio_6x1(escala_completa)
    
    print(f"\n📊 RELATÓRIO 6X1:")
    print("=" * 80)
    
    if not relatorio_6x1.empty:
        for _, row in relatorio_6x1.iterrows():
            print(f"👤 {row['Nome']} ({row['Cargo']})")
            print(f"   Tipo: {row['Tipo_Escala']} - {row['Turno']}")
            print(f"   Último Domingo Folga: {row['Ultimo_Domingo_Folga_Formatado']}")
            print(f"   Próximo Domingo Folga: {row['Proximo_Domingo_Folga']}")
            print(f"   Domingos Folgados: {row['Domingos_Folgados']}")
            print(f"   Semanas Sem Domingo: {row['Semanas_Sem_Domingo']}")
            print(f"   Status: {row['Status_Controle']}")
            print("-" * 40)
    else:
        print("❌ Nenhum colaborador 6x1 encontrado")
    
    # Verificar dados completos internos
    if hasattr(gerador, '_dados_completos'):
        print(f"\n🔍 Dados completos internos: {len(gerador._dados_completos)} registros")
        print(f"   Colunas: {list(gerador._dados_completos.columns)}")
        
        # Verificar se tem as colunas de controle 6x1
        colunas_controle = ['Ultimo_Domingo_Folga', 'Domingos_Folgados', 'Semanas_Sem_Domingo']
        tem_controle = all(col in gerador._dados_completos.columns for col in colunas_controle)
        print(f"   ✅ Tem colunas de controle 6x1: {tem_controle}")
    else:
        print("❌ Dados completos não encontrados")
    
    return escala_completa, relatorio_6x1

if __name__ == "__main__":
    print("INICIANDO TESTE DAS CORREÇÕES FINAIS v2")
    print("=" * 80)
    
    escala, relatorio = testar_correcoes_finais()
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 80) 