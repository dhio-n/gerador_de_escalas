"""
Teste de Debug - Lógica de Plantões
===================================

Script para testar e debugar a lógica de plantões que não está funcionando no app2.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_plantao():
    """Testa a lógica de plantões com dados específicos."""
    
    st.title("🧪 Debug - Lógica de Plantões")
    
    # Dados de teste - período de junho 2025
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 28)
    
    # Dados de colaboradores de teste
    colaboradores_teste = [
        {
            'Nome': 'Plantonista Par Dia',
            'Cargo': 'Enfermeiro',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',  # Dia 30 (par)
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
            'Ultimo_Plantao_Mes_Anterior': '29/05/2025',  # Dia 29 (ímpar)
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
    if st.button("🧪 Testar Lógica de Plantões"):
        
        try:
            # Criar gerador
            gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
            
            # Testar cada colaborador individualmente
            for _, colaborador in df_colaboradores.iterrows():
                st.markdown("---")
                st.subheader(f"🔍 Testando: {colaborador['Nome']}")
                
                # Mostrar dados do colaborador
                st.write(f"**Tipo Original:** {colaborador['Tipo_Escala']}")
                st.write(f"**Último Plantão:** {colaborador['Ultimo_Plantao_Mes_Anterior']}")
                
                # Gerar escala individual
                escala_colaborador = gerador._gerar_escala_colaborador(colaborador)
                
                # Mostrar resultados
                st.write("**Escala Gerada:**")
                st.dataframe(escala_colaborador, use_container_width=True)
                
                # Verificar mudanças de tipo
                tipos_unicos = escala_colaborador['Tipo_Escala'].unique()
                if len(tipos_unicos) > 1:
                    st.warning(f"⚠️ **MUDANÇA DETECTADA:** {tipos_unicos}")
                else:
                    st.info(f"ℹ️ **Tipo mantido:** {tipos_unicos[0]}")
                
                # Mostrar dias de trabalho
                dias_trabalho = escala_colaborador[escala_colaborador['Status'] == 'TRABALHO']
                st.write(f"**Dias de Trabalho:** {len(dias_trabalho)}")
                
                # Mostrar primeiros 10 dias para verificação
                st.write("**Primeiros 10 dias:**")
                primeiros_dias = escala_colaborador.head(10)
                st.dataframe(primeiros_dias[['Data', 'Status', 'Tipo_Escala']], use_container_width=True)
            
            # Testar função específica de determinação automática
            st.markdown("---")
            st.subheader("🔧 Teste da Função de Determinação Automática")
            
            regras = RegrasCLT()
            
            # Teste 1: Plantão par com último plantão em dia par
            ultimo_plantao_par = datetime.strptime('30/05/2025', '%d/%m/%Y').date()
            tipo_novo_par = regras.determinar_tipo_plantao_automatico(ultimo_plantao_par, 'P_D')
            st.write(f"**Teste 1:** P_D com último plantão 30/05/2025 → {tipo_novo_par}")
            
            # Teste 2: Plantão ímpar com último plantão em dia ímpar
            ultimo_plantao_impar = datetime.strptime('29/05/2025', '%d/%m/%Y').date()
            tipo_novo_impar = regras.determinar_tipo_plantao_automatico(ultimo_plantao_impar, 'I_N')
            st.write(f"**Teste 2:** I_N com último plantão 29/05/2025 → {tipo_novo_impar}")
            
            # Verificar se maio tem 31 dias
            mes_maio = date(2025, 5, 31)
            st.write(f"**Maio 2025 tem 31 dias:** {mes_maio.day == 31}")
            
            st.success("✅ Teste concluído!")
            
        except Exception as e:
            st.error(f"❌ Erro no teste: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    testar_plantao() 