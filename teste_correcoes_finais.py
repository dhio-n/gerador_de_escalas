"""
Teste das Correções Finais
==========================

Este arquivo testa as correções finais:
1. Mensagens de aviso corretas para plantões
2. Cálculo correto de dias de trabalho e folga
"""

import pandas as pd
from datetime import date, datetime
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_mensagens_aviso():
    """Testa se as mensagens de aviso estão corretas."""
    print("=== TESTE MENSAGENS DE AVISO ===")
    
    regras = RegrasCLT()
    
    # Teste 1: I_N com último plantão em dia ímpar (31/05)
    print("\n1. Teste I_N com último plantão em dia ímpar (31/05):")
    ultimo_plantao = date(2025, 5, 31)  # Dia ímpar
    tipo_original = "I_N"
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Noite")
    print(f"   Tipo original: {tipo_original}")
    print(f"   Último plantão: {ultimo_plantao.strftime('%d/%m/%Y')} (dia ímpar)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   Mensagem esperada: I_N → {tipo_auto}")
    print(f"   ✅ Correto: {tipo_auto == 'P_N'}")
    
    # Teste 2: P_D com último plantão em dia par (30/05)
    print("\n2. Teste P_D com último plantão em dia par (30/05):")
    ultimo_plantao = date(2025, 5, 30)  # Dia par
    tipo_original = "P_D"
    tipo_auto = regras.determinar_tipo_plantao_automatico(ultimo_plantao, "Dia")
    print(f"   Tipo original: {tipo_original}")
    print(f"   Último plantão: {ultimo_plantao.strftime('%d/%m/%Y')} (dia par)")
    print(f"   Tipo determinado: {tipo_auto}")
    print(f"   Mensagem esperada: P_D → {tipo_auto}")
    print(f"   ✅ Correto: {tipo_auto == 'I_D'}")

def testar_relatorio_plantoes():
    """Testa o cálculo correto de dias de trabalho e folga."""
    print("\n=== TESTE RELATÓRIO PLANTÕES ===")
    
    # Criar dados de teste
    dados_colaboradores = [
        {
            'Nome': 'Ana Costa',
            'Cargo': 'Supervisor',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Carlos Lima',
            'Cargo': 'Operador',
            'Tipo_Escala': 'I_N',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    df_colaboradores = pd.DataFrame(dados_colaboradores)
    df_feriados = pd.DataFrame(columns=['Data', 'Descricao'])
    
    # Configurar período (junho tem 30 dias)
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    
    # Criar gerador
    gerador = GeradorEscala(data_inicio, data_fim, df_feriados)
    
    # Gerar escala completa
    escala_completa = gerador.gerar_escala_completa(df_colaboradores)
    
    print(f"✅ Escala gerada com {len(escala_completa)} registros")
    
    # Gerar relatório de plantões
    relatorio_plantoes = gerador.gerar_relatorio_plantoes(escala_completa)
    
    print("\n📊 RELATÓRIO PLANTÕES:")
    print("=" * 60)
    
    if not relatorio_plantoes.empty:
        for _, row in relatorio_plantoes.iterrows():
            print(f"👤 {row['Nome']} ({row['Cargo']})")
            print(f"   Tipo: {row['Tipo_Escala']} - {row['Turno']}")
            print(f"   Dias Trabalho: {row['Dias_Trabalho']}")
            print(f"   Dias Folga: {row['Dias_Folga']}")
            print(f"   Total Dias: {row['Total_Dias']}")
            print(f"   Último Plantão Mês: {row['Ultimo_Plantao_Mes']}")
            
            # Verificar se o cálculo está correto
            total_calculado = row['Dias_Trabalho'] + row['Dias_Folga']
            print(f"   Soma (Trabalho + Folga): {total_calculado}")
            print(f"   ✅ Correto: {total_calculado == row['Total_Dias']}")
            print("-" * 40)
    else:
        print("❌ Nenhum plantonista encontrado")
    
    return relatorio_plantoes

def testar_escala_plantao():
    """Testa a geração de escala de plantão para verificar os status."""
    print("\n=== TESTE GERAÇÃO ESCALA PLANTÃO ===")
    
    regras = RegrasCLT()
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    feriados = []
    
    # Teste plantão par
    print("\n1. Teste Plantão Par (P_D):")
    ultimo_plantao = date(2025, 5, 30)  # Dia par
    escala_par = regras._regra_plantao_par_dia(data_inicio, data_fim, feriados, ultimo_plantao)
    
    # Contar status
    trabalhos = sum(1 for status in escala_par.values() if status in ['TRABALHO_DIA', 'TRABALHO_NOITE'])
    folgas = sum(1 for status in escala_par.values() if status == 'FOLGA')
    
    print(f"   Dias Trabalho: {trabalhos}")
    print(f"   Dias Folga: {folgas}")
    print(f"   Total: {trabalhos + folgas}")
    print(f"   ✅ Correto: {trabalhos + folgas == 30}")
    
    # Teste plantão ímpar
    print("\n2. Teste Plantão Ímpar (I_N):")
    ultimo_plantao = date(2025, 5, 29)  # Dia ímpar
    escala_impar = regras._regra_plantao_impar_noite(data_inicio, data_fim, feriados, ultimo_plantao)
    
    # Contar status
    trabalhos = sum(1 for status in escala_impar.values() if status in ['TRABALHO_DIA', 'TRABALHO_NOITE'])
    folgas = sum(1 for status in escala_impar.values() if status == 'FOLGA')
    
    print(f"   Dias Trabalho: {trabalhos}")
    print(f"   Dias Folga: {folgas}")
    print(f"   Total: {trabalhos + folgas}")
    print(f"   ✅ Correto: {trabalhos + folgas == 30}")

if __name__ == "__main__":
    print("INICIANDO TESTE DAS CORREÇÕES FINAIS")
    print("=" * 60)
    
    # Testar mensagens de aviso
    testar_mensagens_aviso()
    
    # Testar relatório de plantões
    relatorio = testar_relatorio_plantoes()
    
    # Testar geração de escala
    testar_escala_plantao()
    
    print("\n" + "=" * 60)
    print("✅ TESTE DAS CORREÇÕES FINAIS CONCLUÍDO")
    print("=" * 60) 