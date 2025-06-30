"""
Teste do Relatório 6x1
=====================

Este arquivo testa se o relatório 6x1 está exibindo corretamente:
- Último domingo de folga
- Próximo domingo para folgar
- Status de controle
"""

import pandas as pd
from datetime import date, datetime
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_relatorio_6x1():
    """Testa o relatório 6x1."""
    print("=== TESTE RELATÓRIO 6X1 ===")
    
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
            'Nome': 'Maria Santos',
            'Cargo': 'Técnico',
            'Tipo_Escala': 'T6X1',
            'Turno': 'Tarde',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '',
            'Ultimo_Domingo_Folga': ''
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
            'Ultimo_Domingo_Folga': '18/05/2025'
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
    
    # Gerar relatório 6x1
    relatorio_6x1 = gerador.gerar_relatorio_6x1(escala_completa)
    
    print("\n📊 RELATÓRIO 6X1:")
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
    
    return relatorio_6x1

def testar_formatacao_data():
    """Testa a formatação de datas."""
    print("\n=== TESTE FORMATAÇÃO DE DATAS ===")
    
    gerador = GeradorEscala(date(2025, 6, 1), date(2025, 6, 30), pd.DataFrame())
    
    # Testes de formatação
    datas_teste = [
        '2025-05-25',
        '25/05/2025',
        '25-05-2025',
        date(2025, 5, 25),
        None,
        ''
    ]
    
    for data_teste in datas_teste:
        resultado = gerador._formatar_data(data_teste)
        print(f"   {data_teste} → {resultado}")

if __name__ == "__main__":
    print("INICIANDO TESTE DO RELATÓRIO 6X1")
    print("=" * 80)
    
    # Testar formatação de datas
    testar_formatacao_data()
    
    # Testar relatório 6x1
    relatorio = testar_relatorio_6x1()
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 80) 