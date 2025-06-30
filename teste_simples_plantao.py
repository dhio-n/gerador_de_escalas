"""
Teste Simples - Lógica de Plantões
==================================

Teste direto da lógica de plantões para identificar o problema
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def teste_simples_plantao():
    """Teste simples da lógica de plantões."""
    
    st.title("🧪 Teste Simples - Lógica de Plantões")
    
    # Dados de teste
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 28)
    
    colaborador_teste = {
        'Nome': 'Plantonista Teste',
        'Cargo': 'Enfermeiro',
        'Tipo_Escala': 'P_D',
        'Turno': 'Dia',
        'Atestados': '',
        'Ferias': '',
        'Escalas_Manuais': '',
        'Ultimo_Plantao_Mes_Anterior': '30/05/2025',
        'Ultimo_Domingo_Folga': ''
    }
    
    feriados_teste = pd.DataFrame({
        'Data': [date(2025, 6, 19)],
        'Descricao': ['Corpus Christi']
    })
    
    st.subheader("📋 Dados de Teste")
    st.write(f"**Período:** {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
    st.write(f"**Colaborador:** {colaborador_teste['Nome']}")
    st.write(f"**Tipo Original:** {colaborador_teste['Tipo_Escala']}")
    st.write(f"**Último Plantão:** {colaborador_teste['Ultimo_Plantao_Mes_Anterior']}")
    
    if st.button("🧪 Executar Teste"):
        
        try:
            # Testar função de determinação automática
            st.markdown("---")
            st.subheader("🔍 Teste da Função de Determinação Automática")
            
            regras = RegrasCLT()
            
            # Processar último plantão
            ultimo_plantao_mes_anterior = colaborador_teste['Ultimo_Plantao_Mes_Anterior']
            ultimo_plantao = None
            
            if ultimo_plantao_mes_anterior and ultimo_plantao_mes_anterior.strip():
                try:
                    for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                        try:
                            ultimo_plantao = datetime.strptime(ultimo_plantao_mes_anterior.strip(), formato).date()
                            break
                        except ValueError:
                            continue
                except:
                    pass
            
            st.write(f"**Último Plantão Processado:** {ultimo_plantao}")
            
            # Testar determinação automática
            tipo_novo = regras.determinar_tipo_plantao_automatico(ultimo_plantao, colaborador_teste['Tipo_Escala'])
            st.write(f"**Tipo Calculado:** {tipo_novo}")
            
            # Verificar se há mudança
            if tipo_novo != colaborador_teste['Tipo_Escala']:
                st.warning(f"⚠️ **MUDANÇA DETECTADA:** {colaborador_teste['Tipo_Escala']} → {tipo_novo}")
            else:
                st.info(f"ℹ️ **Tipo mantido:** {tipo_novo}")
            
            # Testar geração de escala
            st.markdown("---")
            st.subheader("📊 Teste de Geração de Escala")
            
            df_colaborador = pd.DataFrame([colaborador_teste])
            gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
            
            # Gerar escala individual
            escala_colaborador = gerador._gerar_escala_colaborador(colaborador_teste)
            
            # Analisar resultados
            tipos_unicos = escala_colaborador['Tipo_Escala'].unique()
            st.write(f"**Tipos encontrados na escala:** {tipos_unicos}")
            
            if len(tipos_unicos) > 1:
                st.warning(f"⚠️ **MUDANÇA DETECTADA na escala:** {tipos_unicos}")
                
                # Mostrar quando ocorreu a mudança
                for tipo in tipos_unicos:
                    if tipo != colaborador_teste['Tipo_Escala']:
                        primeiro_dia_novo_tipo = escala_colaborador[escala_colaborador['Tipo_Escala'] == tipo]['Data'].min()
                        st.info(f"**Mudança para {tipo} a partir de:** {primeiro_dia_novo_tipo.strftime('%d/%m/%Y')}")
            else:
                st.info(f"ℹ️ **Tipo mantido na escala:** {tipos_unicos[0]}")
            
            # Mostrar primeiros 15 dias
            st.write("**Primeiros 15 dias:**")
            primeiros_dias = escala_colaborador.head(15)
            st.dataframe(primeiros_dias[['Data', 'Status', 'Tipo_Escala']], use_container_width=True)
            
            # Mostrar todos os dias
            st.write("**Todos os dias:**")
            st.dataframe(escala_colaborador[['Data', 'Status', 'Tipo_Escala']], use_container_width=True)
            
            st.success("✅ Teste concluído!")
            
        except Exception as e:
            st.error(f"❌ Erro no teste: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    teste_simples_plantao() 