"""
Debug - Dados do Formulário
==========================

Script para debugar os dados do formulário e verificar se há diferenças no processamento
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from escala_generator import GeradorEscala
from colaborador_form import FormularioColaboradores

def debug_dados_formulario():
    """Debuga os dados do formulário para identificar diferenças."""
    
    st.title("🔍 Debug - Dados do Formulário")
    
    # Dados de teste idênticos aos da planilha
    dados_planilha = [
        {
            'Nome': 'Plantonista Par Dia',
            'Cargo': 'Enfermeiro',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Plantonista Ímpar Noite',
            'Cargo': 'Técnico',
            'Tipo_Escala': 'I_N',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    # Simular dados do formulário
    st.session_state.colaboradores = dados_planilha
    
    # Criar DataFrame do formulário
    formulario = FormularioColaboradores()
    colaboradores_formulario = formulario.obter_colaboradores()
    df_formulario = pd.DataFrame(colaboradores_formulario)
    
    # Criar DataFrame da planilha
    df_planilha = pd.DataFrame(dados_planilha)
    
    st.subheader("📋 Comparação de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dados do Formulário:**")
        st.dataframe(df_formulario, use_container_width=True)
        
        # Verificar tipos de dados
        st.write("**Tipos de dados do formulário:**")
        st.write(df_formulario.dtypes)
        
        # Verificar valores específicos
        st.write("**Valores de Ultimo_Plantao_Mes_Anterior:**")
        for idx, row in df_formulario.iterrows():
            st.write(f"{row['Nome']}: '{row['Ultimo_Plantao_Mes_Anterior']}' (tipo: {type(row['Ultimo_Plantao_Mes_Anterior'])})")
    
    with col2:
        st.write("**Dados da Planilha:**")
        st.dataframe(df_planilha, use_container_width=True)
        
        # Verificar tipos de dados
        st.write("**Tipos de dados da planilha:**")
        st.write(df_planilha.dtypes)
        
        # Verificar valores específicos
        st.write("**Valores de Ultimo_Plantao_Mes_Anterior:**")
        for idx, row in df_planilha.iterrows():
            st.write(f"{row['Nome']}: '{row['Ultimo_Plantao_Mes_Anterior']}' (tipo: {type(row['Ultimo_Plantao_Mes_Anterior'])})")
    
    # Testar geração de escala com ambos os DataFrames
    st.subheader("🧪 Teste de Geração de Escala")
    
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 28)
    
    feriados_teste = pd.DataFrame({
        'Data': [date(2025, 6, 19)],
        'Descricao': ['Corpus Christi']
    })
    
    if st.button("🧪 Testar Ambos os DataFrames"):
        
        try:
            # Testar com dados do formulário
            st.markdown("---")
            st.subheader("📋 Teste com Dados do Formulário")
            
            gerador_form = GeradorEscala(data_inicio, data_fim, feriados_teste)
            escala_form = gerador_form.gerar_escala_completa(df_formulario)
            
            # Analisar resultados do formulário
            for _, colaborador in df_formulario.iterrows():
                nome = colaborador['Nome']
                dados_colaborador = escala_form[escala_form['Nome'] == nome]
                
                if not dados_colaborador.empty:
                    tipos_unicos = dados_colaborador['Tipo_Escala'].unique()
                    st.write(f"**{nome} (Formulário):** {tipos_unicos}")
                    
                    if len(tipos_unicos) > 1:
                        st.warning(f"⚠️ MUDANÇA DETECTADA no formulário: {tipos_unicos}")
            
            # Testar com dados da planilha
            st.markdown("---")
            st.subheader("📄 Teste com Dados da Planilha")
            
            gerador_plan = GeradorEscala(data_inicio, data_fim, feriados_teste)
            escala_plan = gerador_plan.gerar_escala_completa(df_planilha)
            
            # Analisar resultados da planilha
            for _, colaborador in df_planilha.iterrows():
                nome = colaborador['Nome']
                dados_colaborador = escala_plan[escala_plan['Nome'] == nome]
                
                if not dados_colaborador.empty:
                    tipos_unicos = dados_colaborador['Tipo_Escala'].unique()
                    st.write(f"**{nome} (Planilha):** {tipos_unicos}")
                    
                    if len(tipos_unicos) > 1:
                        st.warning(f"⚠️ MUDANÇA DETECTADA na planilha: {tipos_unicos}")
            
            # Comparar resultados
            st.markdown("---")
            st.subheader("🔍 Comparação de Resultados")
            
            # Verificar se há diferenças
            if escala_form.equals(escala_plan):
                st.success("✅ Resultados idênticos!")
            else:
                st.error("❌ Resultados diferentes!")
                
                # Mostrar diferenças
                st.write("**Diferenças encontradas:**")
                for _, colaborador in df_formulario.iterrows():
                    nome = colaborador['Nome']
                    
                    dados_form = escala_form[escala_form['Nome'] == nome]
                    dados_plan = escala_plan[escala_plan['Nome'] == nome]
                    
                    tipos_form = dados_form['Tipo_Escala'].unique()
                    tipos_plan = dados_plan['Tipo_Escala'].unique()
                    
                    if not (tipos_form == tipos_plan).all():
                        st.warning(f"**{nome}:** Formulário: {tipos_form} | Planilha: {tipos_plan}")
            
        except Exception as e:
            st.error(f"❌ Erro no teste: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    debug_dados_formulario() 