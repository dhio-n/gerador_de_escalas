"""
Teste de Leitura da Planilha
============================

Este arquivo testa se a leitura da planilha está preservando
corretamente o formato das datas, especialmente o campo Ultimo_Domingo_Folga.
"""

import pandas as pd
from datetime import date, datetime
from io import BytesIO
from excel_utils import ler_planilha_colaboradores

def testar_leitura_planilha():
    """Testa a leitura da planilha com dados de exemplo."""
    print("=== TESTE LEITURA PLANILHA ===")
    
    # Criar dados de exemplo com diferentes formatos de data
    dados_exemplo = [
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
        }
    ]
    
    # Criar DataFrame
    df_original = pd.DataFrame(dados_exemplo)
    
    print("📋 Dados originais:")
    print(df_original[['Nome', 'Ultimo_Domingo_Folga']])
    print()
    
    # Criar arquivo Excel em memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_original.to_excel(writer, sheet_name='Colaboradores', index=False)
    
    output.seek(0)
    
    # Simular upload do Streamlit
    class MockUploader:
        def __init__(self, data):
            self.data = data
        
        def read(self):
            return self.data
        
        def seek(self, pos):
            pass
    
    arquivo_mock = MockUploader(output.getvalue())
    
    # Ler planilha usando a função
    try:
        df_lido = ler_planilha_colaboradores(arquivo_mock)
        
        print("✅ Planilha lida com sucesso!")
        print(f"📊 Colunas: {list(df_lido.columns)}")
        print()
        
        print("📋 Dados lidos:")
        print(df_lido[['Nome', 'Ultimo_Domingo_Folga']])
        print()
        
        # Verificar se os valores foram preservados
        print("🔍 Verificação dos valores:")
        for _, row in df_lido.iterrows():
            nome = row['Nome']
            ultimo_domingo = row['Ultimo_Domingo_Folga']
            print(f"   {nome}: '{ultimo_domingo}' (tipo: {type(ultimo_domingo)})")
        
        # Testar processamento da data
        print("\n🧪 Teste de processamento da data:")
        for _, row in df_lido.iterrows():
            nome = row['Nome']
            ultimo_domingo = row['Ultimo_Domingo_Folga']
            
            if ultimo_domingo and ultimo_domingo.strip():
                print(f"\n   {nome}:")
                print(f"      Valor original: '{ultimo_domingo}'")
                
                # Simular processamento como no _gerar_escala_colaborador
                ultimo_domingo_processado = None
                if ultimo_domingo and ultimo_domingo.strip():
                    try:
                        for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                            try:
                                ultimo_domingo_processado = datetime.strptime(ultimo_domingo.strip(), formato).date()
                                print(f"      ✅ Processado: {ultimo_domingo_processado} (formato: {formato})")
                                break
                            except ValueError:
                                continue
                    except Exception as e:
                        print(f"      ❌ Erro: {e}")
                
                if ultimo_domingo_processado:
                    # Testar formatação
                    from escala_generator import GeradorEscala
                    gerador = GeradorEscala(date(2025, 6, 1), date(2025, 6, 30), pd.DataFrame())
                    formatado = gerador._formatar_data(ultimo_domingo_processado)
                    proximo = gerador._calcular_proximo_domingo_folga(str(ultimo_domingo_processado))
                    
                    print(f"      📅 Formatado: {formatado}")
                    print(f"      ➡️ Próximo domingo: {proximo}")
                else:
                    print(f"      ❌ Não foi possível processar a data")
            else:
                print(f"   {nome}: Campo vazio")
        
        return df_lido
        
    except Exception as e:
        print(f"❌ Erro ao ler planilha: {e}")
        return None

if __name__ == "__main__":
    print("INICIANDO TESTE DE LEITURA DA PLANILHA")
    print("=" * 80)
    
    df_resultado = testar_leitura_planilha()
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 80) 