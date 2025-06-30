"""
Comparação entre app.py e app2.py
=================================

Script para identificar diferenças entre os dois aplicativos
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def comparar_apps():
    """Compara o comportamento do app.py vs app2.py."""
    
    st.title("🔍 Comparação app.py vs app2.py")
    
    # Dados de teste idênticos
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 28)
    
    colaboradores_teste = [
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
    
    feriados_teste = pd.DataFrame({
        'Data': [date(2025, 6, 19)],
        'Descricao': ['Corpus Christi']
    })
    
    st.subheader("📋 Dados de Teste")
    st.write(f"**Período:** {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
    
    df_colaboradores = pd.DataFrame(colaboradores_teste)
    st.dataframe(df_colaboradores, use_container_width=True)
    
    if st.button("🔍 Comparar Comportamento"):
        
        try:
            # Testar com escala_generator diretamente (como app.py faria)
            gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
            
            st.subheader("🧪 Teste Direto com escala_generator")
            
            # Testar cada colaborador individualmente
            for _, colaborador in df_colaboradores.iterrows():
                st.markdown("---")
                st.subheader(f"🔍 {colaborador['Nome']}")
                
                # Mostrar dados de entrada
                st.write(f"**Tipo Original:** {colaborador['Tipo_Escala']}")
                st.write(f"**Último Plantão:** {colaborador['Ultimo_Plantao_Mes_Anterior']}")
                
                # Processar último plantão manualmente (como o código faz)
                ultimo_plantao_mes_anterior = colaborador['Ultimo_Plantao_Mes_Anterior']
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
                
                # Testar função de determinação automática
                regras = RegrasCLT()
                tipo_novo = regras.determinar_tipo_plantao_automatico(ultimo_plantao, colaborador['Tipo_Escala'])
                st.write(f"**Tipo Calculado:** {tipo_novo}")
                
                # Gerar escala individual
                escala_colaborador = gerador._gerar_escala_colaborador(colaborador)
                
                # Verificar mudanças de tipo
                tipos_unicos = escala_colaborador['Tipo_Escala'].unique()
                if len(tipos_unicos) > 1:
                    st.warning(f"⚠️ **MUDANÇA DETECTADA:** {tipos_unicos}")
                    
                    # Mostrar quando ocorreu a mudança
                    for tipo in tipos_unicos:
                        if tipo != colaborador['Tipo_Escala']:
                            primeiro_dia_novo_tipo = escala_colaborador[escala_colaborador['Tipo_Escala'] == tipo]['Data'].min()
                            st.info(f"**Mudança para {tipo} a partir de:** {primeiro_dia_novo_tipo.strftime('%d/%m/%Y')}")
                else:
                    st.info(f"ℹ️ **Tipo mantido:** {tipos_unicos[0]}")
                
                # Mostrar primeiros 10 dias
                st.write("**Primeiros 10 dias:**")
                primeiros_dias = escala_colaborador.head(10)
                st.dataframe(primeiros_dias[['Data', 'Status', 'Tipo_Escala']], use_container_width=True)
            
            # Testar escala completa
            st.subheader("📊 Escala Completa")
            escala_completa = gerador.gerar_escala_completa(df_colaboradores)
            st.dataframe(escala_completa, use_container_width=True)
            
            st.success("✅ Teste concluído!")
            
        except Exception as e:
            st.error(f"❌ Erro no teste: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    comparar_apps() 