"""
Teste dos Avisos de Plantão
===========================

Este arquivo testa se os avisos de mudança de plantão estão mostrando
corretamente a mudança do tipo original para o tipo calculado.
"""

import pandas as pd
from datetime import date, datetime
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_avisos_plantao():
    """Testa os avisos de mudança de plantão."""
    print("=== TESTE AVISOS DE PLANTÃO ===")
    
    # Criar dados de teste com plantões
    dados_colaboradores = [
        {
            'Nome': 'Ana Costa',
            'Cargo': 'Supervisor',
            'Tipo_Escala': 'I_N',  # Ímpar Noite
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',  # Dia 30 (par)
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Carlos Lima',
            'Cargo': 'Operador',
            'Tipo_Escala': 'P_D',  # Par Dia
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',  # Dia 29 (ímpar)
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    df_colaboradores = pd.DataFrame(dados_colaboradores)
    
    print("📋 Dados de teste:")
    for _, row in df_colaboradores.iterrows():
        print(f"   {row['Nome']}: {row['Tipo_Escala']} - Último plantão: {row['Ultimo_Plantao_Mes_Anterior']}")
    print()
    
    # Criar dados de feriados (vazio para teste)
    df_feriados = pd.DataFrame(columns=['Data', 'Descricao'])
    
    # Configurar período
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 30)
    
    # Criar gerador
    gerador = GeradorEscala(data_inicio, data_fim, df_feriados)
    
    # Testar a função determinar_tipo_plantao_automatico diretamente
    print("🧪 Teste da função determinar_tipo_plantao_automatico:")
    for _, row in df_colaboradores.iterrows():
        nome = row['Nome']
        tipo_original = row['Tipo_Escala']
        turno = row['Turno']
        ultimo_plantao_str = row['Ultimo_Plantao_Mes_Anterior']
        
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
            tipo_calculado = gerador.regras_clt.determinar_tipo_plantao_automatico(ultimo_plantao, turno)
            print(f"   {nome}:")
            print(f"      Tipo original: {tipo_original}")
            print(f"      Último plantão: {ultimo_plantao} (dia {ultimo_plantao.day})")
            print(f"      Tipo calculado: {tipo_calculado}")
            print(f"      Mudança esperada: {tipo_original} → {tipo_calculado}")
            print()
    
    # Gerar escala completa (isso deve mostrar os avisos)
    print("🚀 Gerando escala completa (deve mostrar avisos):")
    escala_completa = gerador.gerar_escala_completa(df_colaboradores)
    
    print(f"✅ Escala gerada com {len(escala_completa)} registros")
    
    # Verificar tipos finais na escala
    print("\n📊 Tipos finais na escala:")
    tipos_finais = escala_completa.groupby('Nome')['Tipo_Escala'].first()
    for nome, tipo_final in tipos_finais.items():
        print(f"   {nome}: {tipo_final}")
    
    return escala_completa

if __name__ == "__main__":
    print("INICIANDO TESTE DOS AVISOS DE PLANTÃO")
    print("=" * 80)
    
    escala = testar_avisos_plantao()
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 80) 