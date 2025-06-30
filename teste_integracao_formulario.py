"""
Teste de Integração do Formulário de Colaboradores
=================================================

Script para testar se a integração entre o formulário e o gerador está funcionando.
"""

import streamlit as st
import pandas as pd
from datetime import date
from colaborador_form import FormularioColaboradores

def testar_integracao():
    """Testa a integração do formulário com o gerador."""
    
    st.title("🧪 Teste de Integração - Formulário de Colaboradores")
    
    # Simular dados de colaboradores
    colaboradores_teste = [
        {
            'Nome': 'João Silva',
            'Cargo': 'Enfermeiro',
            'Tipo_Escala': 'M44',
            'Turno': 'Manhã',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '',
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Maria Santos',
            'Cargo': 'Técnico de Enfermagem',
            'Tipo_Escala': 'T44',
            'Turno': 'Tarde',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '',
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    # Testar se o formulário pode processar os dados
    try:
        formulario = FormularioColaboradores()
        
        # Simular dados no session state
        st.session_state.colaboradores = colaboradores_teste
        
        st.success("✅ Formulário inicializado com sucesso!")
        
        # Testar geração de Excel
        df_teste = pd.DataFrame(colaboradores_teste)
        excel_bytes = formulario._gerar_excel()
        
        st.success("✅ Geração de Excel funcionando!")
        
        # Testar download
        st.download_button(
            label="📥 Download Teste",
            data=excel_bytes,
            file_name="teste_colaboradores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Mostrar dados de teste
        st.subheader("📋 Dados de Teste")
        st.dataframe(df_teste, use_container_width=True)
        
        st.success("✅ Todos os testes passaram!")
        
    except Exception as e:
        st.error(f"❌ Erro no teste: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    testar_integracao() 