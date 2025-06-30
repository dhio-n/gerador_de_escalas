"""
Teste da Correção - Lógica de Plantões
======================================

Script para testar se a correção da lógica de plantões funcionou
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from escala_generator import GeradorEscala

def testar_correcao_plantao():
    """Testa se a correção da lógica de plantões funcionou."""
    
    st.title("🔧 Teste da Correção - Lógica de Plantões")
    
    # Dados de teste - período de junho 2025
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 28)
    
    # Dados de colaboradores de teste
    colaboradores_teste = [
        {
            'Nome': 'Plantonista Par Dia (30/05)',
            'Cargo': 'Enfermeiro',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',  # Dia 30 (par) - deve virar I_D
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Plantonista Ímpar Noite (29/05)',
            'Cargo': 'Técnico',
            'Tipo_Escala': 'I_N',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',  # Dia 29 (ímpar) - deve virar P_N
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    # Feriados de teste
    feriados_teste = pd.DataFrame({
        'Data': [date(2025, 6, 19)],  # Corpus Christi
        'Descricao': ['Corpus Christi']
    })
    
    st.subheader("📋 Dados de Teste")
    st.write(f"**Período:** {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
    st.write(f"**Feriados:** {len(feriados_teste)} feriados")
    
    # Mostrar colaboradores
    df_colaboradores = pd.DataFrame(colaboradores_teste)
    st.dataframe(df_colaboradores, use_container_width=True)
    
    # Testar lógica de plantões
    if st.button("🔧 Testar Correção"):
        
        try:
            # Criar gerador
            gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
            
            # Gerar escala completa
            escala_completa = gerador.gerar_escala_completa(df_colaboradores)
            
            st.success("✅ Escala gerada com sucesso!")
            
            # Analisar resultados
            st.subheader("📊 Análise dos Resultados")
            
            for _, colaborador in df_colaboradores.iterrows():
                nome = colaborador['Nome']
                tipo_original = colaborador['Tipo_Escala']
                ultimo_plantao = colaborador['Ultimo_Plantao_Mes_Anterior']
                
                # Filtrar dados do colaborador
                dados_colaborador = escala_completa[escala_completa['Nome'] == nome]
                
                if not dados_colaborador.empty:
                    st.markdown(f"---")
                    st.subheader(f"🔍 {nome}")
                    
                    # Verificar mudanças de tipo
                    tipos_unicos = dados_colaborador['Tipo_Escala'].unique()
                    
                    if len(tipos_unicos) > 1:
                        st.warning(f"⚠️ **MUDANÇA DETECTADA:** {tipo_original} → {tipos_unicos}")
                        
                        # Mostrar quando ocorreu a mudança
                        for tipo in tipos_unicos:
                            if tipo != tipo_original:
                                primeiro_dia_novo_tipo = dados_colaborador[dados_colaborador['Tipo_Escala'] == tipo]['Data'].min()
                                st.info(f"**Mudança para {tipo} a partir de:** {primeiro_dia_novo_tipo.strftime('%d/%m/%Y')}")
                    else:
                        st.info(f"ℹ️ **Tipo mantido:** {tipos_unicos[0]}")
                    
                    # Mostrar estatísticas
                    dias_trabalho = dados_colaborador[dados_colaborador['Status'] == 'TRABALHO']
                    dias_folga = dados_colaborador[dados_colaborador['Status'] == 'FOLGA']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Dias de Trabalho", len(dias_trabalho))
                    with col2:
                        st.metric("Dias de Folga", len(dias_folga))
                    with col3:
                        st.metric("Total de Dias", len(dados_colaborador))
                    
                    # Mostrar primeiros 10 dias
                    st.write("**Primeiros 10 dias:**")
                    primeiros_dias = dados_colaborador.head(10)
                    st.dataframe(primeiros_dias[['Data', 'Status', 'Tipo_Escala']], use_container_width=True)
            
            # Mostrar escala completa
            st.subheader("📋 Escala Completa")
            st.dataframe(escala_completa, use_container_width=True)
            
            st.success("✅ Teste concluído!")
            
        except Exception as e:
            st.error(f"❌ Erro no teste: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    testar_correcao_plantao() 