"""
Teste Específico - Pedro Oliveira 6x1
====================================

Este arquivo testa especificamente o problema com o Pedro Oliveira
no relatório 6x1, onde o último domingo não está sendo exibido.
"""

import pandas as pd
from datetime import date, datetime
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_pedro_oliveira():
    """Testa especificamente o Pedro Oliveira."""
    print("=== TESTE PEDRO OLIVEIRA 6X1 ===")
    
    # Criar dados específicos do Pedro Oliveira
    dados_colaboradores = [
        {
            'Nome': 'Pedro Oliveira',
            'Cargo': 'Auxiliar',
            'Tipo_Escala': 'N6X1',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '',
            'Ultimo_Domingo_Folga': '18/05/2025'
        }
    ]
    
    df_colaboradores = pd.DataFrame(dados_colaboradores)
    
    print("📋 Dados do Pedro Oliveira:")
    print(f"   Nome: {df_colaboradores.iloc[0]['Nome']}")
    print(f"   Tipo Escala: {df_colaboradores.iloc[0]['Tipo_Escala']}")
    print(f"   Último Domingo Folga: {df_colaboradores.iloc[0]['Ultimo_Domingo_Folga']}")
    print()
    
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
    
    # Verificar dados do Pedro na escala completa
    pedro_escala = escala_completa[escala_completa['Nome'] == 'Pedro Oliveira']
    
    if not pedro_escala.empty:
        print(f"\n📊 Dados do Pedro na escala completa:")
        print(f"   Registros: {len(pedro_escala)}")
        print(f"   Último Domingo Folga: {pedro_escala.iloc[0]['Ultimo_Domingo_Folga']}")
        print(f"   Domingos Folgados: {pedro_escala.iloc[0]['Domingos_Folgados']}")
        print(f"   Semanas Sem Domingo: {pedro_escala.iloc[0]['Semanas_Sem_Domingo']}")
        
        # Verificar se há valores diferentes
        ultimos_domingos = pedro_escala['Ultimo_Domingo_Folga'].unique()
        print(f"   Valores únicos de Último Domingo: {ultimos_domingos}")
    else:
        print("❌ Pedro Oliveira não encontrado na escala")
    
    # Gerar relatório 6x1
    relatorio_6x1 = gerador.gerar_relatorio_6x1(escala_completa)
    
    print(f"\n📊 RELATÓRIO 6X1:")
    print("=" * 80)
    
    if not relatorio_6x1.empty:
        for _, row in relatorio_6x1.iterrows():
            print(f"👤 {row['Nome']} ({row['Cargo']})")
            print(f"   Tipo: {row['Tipo_Escala']} - {row['Turno']}")
            print(f"   Último Domingo Folga (original): {row['Ultimo_Domingo_Folga']}")
            print(f"   Último Domingo Folga (formatado): {row['Ultimo_Domingo_Folga_Formatado']}")
            print(f"   Próximo Domingo Folga: {row['Proximo_Domingo_Folga']}")
            print(f"   Domingos Folgados: {row['Domingos_Folgados']}")
            print(f"   Semanas Sem Domingo: {row['Semanas_Sem_Domingo']}")
            print(f"   Status: {row['Status_Controle']}")
            print("-" * 40)
    else:
        print("❌ Nenhum colaborador 6x1 encontrado")
    
    return relatorio_6x1

def testar_processamento_data():
    """Testa o processamento de data do último domingo."""
    print("\n=== TESTE PROCESSAMENTO DE DATA ===")
    
    gerador = GeradorEscala(date(2025, 6, 1), date(2025, 6, 30), pd.DataFrame())
    
    # Testar diferentes formatos
    datas_teste = [
        '18/05/2025',
        '2025-05-18',
        '18-05-2025',
        '25/05/2025',
        '2025-05-25'
    ]
    
    for data_teste in datas_teste:
        print(f"\n🔍 Testando: {data_teste}")
        
        # Simular processamento como no _gerar_escala_colaborador
        ultimo_domingo = None
        if data_teste and data_teste.strip():
            try:
                for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                    try:
                        ultimo_domingo = datetime.strptime(data_teste.strip(), formato).date()
                        print(f"   ✅ Processado: {ultimo_domingo} (formato: {formato})")
                        break
                    except ValueError:
                        continue
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        
        if ultimo_domingo:
            # Testar formatação
            formatado = gerador._formatar_data(ultimo_domingo)
            print(f"   📅 Formatado: {formatado}")
            
            # Testar cálculo do próximo domingo
            proximo = gerador._calcular_proximo_domingo_folga(str(ultimo_domingo))
            print(f"   ➡️ Próximo domingo: {proximo}")
        else:
            print(f"   ❌ Não foi possível processar a data")

if __name__ == "__main__":
    print("INICIANDO TESTE ESPECÍFICO - PEDRO OLIVEIRA")
    print("=" * 80)
    
    # Testar processamento de data
    testar_processamento_data()
    
    # Testar Pedro Oliveira
    relatorio = testar_pedro_oliveira()
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 80) 