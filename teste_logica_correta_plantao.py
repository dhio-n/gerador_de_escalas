"""
Teste da Lógica Correta - Plantões
==================================

Script para testar a lógica correta de alternância de plantões
baseada no número de dias do mês de referência.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from escala_generator import GeradorEscala
from regras_clt import RegrasCLT

def testar_logica_correta():
    """Testa a lógica correta de plantões com diferentes cenários."""
    
    st.title("✅ Teste da Lógica Correta - Plantões")
    
    # Criar instância das regras
    regras = RegrasCLT()
    
    st.subheader("🔧 Teste da Função de Determinação Automática")
    
    # Cenários de teste
    cenarios = [
        {
            'nome': 'Maio 2025 (31 dias) - Plantão Par',
            'ultimo_plantao': '31/05/2025',
            'tipo_anterior': 'P_D',
            'esperado': 'I_D',
            'descricao': 'Maio tem 31 dias, P_D deve virar I_D'
        },
        {
            'nome': 'Maio 2025 (31 dias) - Plantão Ímpar',
            'ultimo_plantao': '30/05/2025',
            'tipo_anterior': 'I_N',
            'esperado': 'P_N',
            'descricao': 'Maio tem 31 dias, I_N deve virar P_N'
        },
        {
            'nome': 'Abril 2025 (30 dias) - Plantão Par',
            'ultimo_plantao': '30/04/2025',
            'tipo_anterior': 'P_D',
            'esperado': 'P_D',
            'descricao': 'Abril tem 30 dias, P_D deve permanecer P_D'
        },
        {
            'nome': 'Abril 2025 (30 dias) - Plantão Ímpar',
            'ultimo_plantao': '29/04/2025',
            'tipo_anterior': 'I_N',
            'esperado': 'I_N',
            'descricao': 'Abril tem 30 dias, I_N deve permanecer I_N'
        },
        {
            'nome': 'Fevereiro 2025 (28 dias) - Plantão Par',
            'ultimo_plantao': '28/02/2025',
            'tipo_anterior': 'P_D',
            'esperado': 'P_D',
            'descricao': 'Fevereiro tem 28 dias, P_D deve permanecer P_D'
        }
    ]
    
    # Executar testes
    resultados = []
    
    for cenario in cenarios:
        try:
            # Converter data
            ultimo_plantao_date = datetime.strptime(cenario['ultimo_plantao'], '%d/%m/%Y').date()
            
            # Testar função
            tipo_resultado = regras.determinar_tipo_plantao_automatico(ultimo_plantao_date, cenario['tipo_anterior'])
            
            # Verificar resultado
            sucesso = tipo_resultado == cenario['esperado']
            
            resultados.append({
                'Cenário': cenario['nome'],
                'Último Plantão': cenario['ultimo_plantao'],
                'Tipo Anterior': cenario['tipo_anterior'],
                'Resultado': tipo_resultado,
                'Esperado': cenario['esperado'],
                'Status': '✅ Correto' if sucesso else '❌ Incorreto',
                'Descrição': cenario['descricao']
            })
            
        except Exception as e:
            resultados.append({
                'Cenário': cenario['nome'],
                'Último Plantão': cenario['ultimo_plantao'],
                'Tipo Anterior': cenario['tipo_anterior'],
                'Resultado': f'ERRO: {str(e)}',
                'Esperado': cenario['esperado'],
                'Status': '❌ Erro',
                'Descrição': cenario['descricao']
            })
    
    # Mostrar resultados
    df_resultados = pd.DataFrame(resultados)
    st.dataframe(df_resultados, use_container_width=True)
    
    # Resumo
    corretos = len([r for r in resultados if r['Status'] == '✅ Correto'])
    total = len(resultados)
    
    st.subheader("📊 Resumo dos Testes")
    st.metric("Testes Corretos", f"{corretos}/{total}")
    
    if corretos == total:
        st.success("🎉 Todos os testes passaram! A lógica está correta.")
    else:
        st.error(f"⚠️ {total - corretos} teste(s) falharam. Verifique a implementação.")
    
    # Teste prático com escala
    st.subheader("🧪 Teste Prático - Geração de Escala")
    
    # Dados de teste para junho 2025
    data_inicio = date(2025, 6, 1)
    data_fim = date(2025, 6, 28)
    
    colaboradores_teste = [
        {
            'Nome': 'Plantonista Par (31/05)',
            'Cargo': 'Enfermeiro',
            'Tipo_Escala': 'P_D',
            'Turno': 'Dia',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '31/05/2025',  # Maio tem 31 dias - deve virar I_D
            'Ultimo_Domingo_Folga': ''
        },
        {
            'Nome': 'Plantonista Ímpar (30/05)',
            'Cargo': 'Técnico',
            'Tipo_Escala': 'I_N',
            'Turno': 'Noite',
            'Atestados': '',
            'Ferias': '',
            'Escalas_Manuais': '',
            'Ultimo_Plantao_Mes_Anterior': '30/05/2025',  # Maio tem 31 dias - deve virar P_N
            'Ultimo_Domingo_Folga': ''
        }
    ]
    
    feriados_teste = pd.DataFrame({
        'Data': [date(2025, 6, 19)],
        'Descricao': ['Corpus Christi']
    })
    
    if st.button("🧪 Gerar Escala de Teste"):
        try:
            gerador = GeradorEscala(data_inicio, data_fim, feriados_teste)
            df_colaboradores = pd.DataFrame(colaboradores_teste)
            escala_completa = gerador.gerar_escala_completa(df_colaboradores)
            
            st.success("✅ Escala gerada com sucesso!")
            
            # Analisar resultados
            for _, colaborador in df_colaboradores.iterrows():
                nome = colaborador['Nome']
                tipo_original = colaborador['Tipo_Escala']
                ultimo_plantao = colaborador['Ultimo_Plantao_Mes_Anterior']
                
                dados_colaborador = escala_completa[escala_completa['Nome'] == nome]
                
                if not dados_colaborador.empty:
                    st.markdown(f"---")
                    st.subheader(f"🔍 {nome}")
                    
                    tipos_unicos = dados_colaborador['Tipo_Escala'].unique()
                    
                    if len(tipos_unicos) > 1:
                        st.warning(f"⚠️ **ALTERNAÇÃO DETECTADA:** {tipo_original} → {tipos_unicos}")
                        
                        # Mostrar quando ocorreu a mudança
                        for tipo in tipos_unicos:
                            if tipo != tipo_original:
                                primeiro_dia_novo_tipo = dados_colaborador[dados_colaborador['Tipo_Escala'] == tipo]['Data'].min()
                                st.info(f"**Mudança para {tipo} a partir de:** {primeiro_dia_novo_tipo.strftime('%d/%m/%Y')}")
                    else:
                        st.info(f"ℹ️ **Tipo mantido:** {tipos_unicos[0]}")
                    
                    # Mostrar primeiros 10 dias
                    st.write("**Primeiros 10 dias:**")
                    primeiros_dias = dados_colaborador.head(10)
                    st.dataframe(primeiros_dias[['Data', 'Status', 'Tipo_Escala']], use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Erro ao gerar escala: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    testar_logica_correta() 