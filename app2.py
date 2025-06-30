"""
Sistema de Geração de Escalas de Trabalho
=========================================

Aplicativo Streamlit para gerar escalas de trabalho automatizadas
respeitando as leis da CLT brasileira.

Autor: Sistema de Escalas
Data: 2025
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import sys

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos do projeto
try:
    from .excel_utils import ler_planilha_colaboradores, ler_planilha_feriados, criar_template_colaboradores
    from .escala_generator import GeradorEscala
    from .pdf_exporter import PDFExporter
    from .colaborador_form import FormularioColaboradores
except ImportError as e:
    # Tentar import absoluto como fallback
    try:
        from excel_utils import ler_planilha_colaboradores, ler_planilha_feriados, criar_template_colaboradores
        from escala_generator import GeradorEscala
        from pdf_exporter import PDFExporter
        from colaborador_form import FormularioColaboradores
    except ImportError as e2:
        st.error(f"Erro ao importar módulos: {str(e2)}")
        st.error("Verifique se todos os arquivos estão presentes no diretório app/")
        st.stop()

def main():
    """Função principal da aplicação Streamlit."""
    
    # Configuração da página
    st.set_page_config(
        page_title="Sistema de Escalas - CLT",
        page_icon="📅",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("📅 Sistema de Geração de Escalas de Trabalho")
    st.markdown("---")
    
    # Criar abas principais
    tab_gerador, tab_formulario = st.tabs(["🚀 Gerador de Escalas", "👥 Formulário de Colaboradores"])
    
    with tab_gerador:
        renderizar_gerador_escalas()
    
    with tab_formulario:
        # Instanciar e renderizar o formulário de colaboradores
        formulario = FormularioColaboradores()
        formulario.renderizar_formulario()
        
        # Botão para usar colaboradores do formulário no gerador
        if st.session_state.get('colaboradores', []):
            st.markdown("---")
            st.subheader("🔄 Integração com Gerador de Escalas")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Usar Colaboradores no Gerador", type="primary"):
                    # Salvar colaboradores do formulário para uso no gerador
                    st.session_state.colaboradores_formulario = formulario.obter_colaboradores()
                    st.success(f"✅ {len(st.session_state.colaboradores_formulario)} colaboradores prontos para uso no gerador!")
                    st.info("💡 Agora vá para a aba 'Gerador de Escalas' e clique em 'Usar Colaboradores do Formulário'")
            
            with col2:
                # Botão para download dos colaboradores
                if st.button("📥 Download Colaboradores XLSX", type="secondary"):
                    try:
                        excel_bytes = formulario._gerar_excel()
                        st.download_button(
                            label="💾 Download Planilha Excel",
                            data=excel_bytes,
                            file_name=f"colaboradores_formulario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        st.success("✅ Planilha pronta para download!")
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar planilha: {str(e)}")
            
            with col3:
                st.info(f"📊 **Status**: {len(st.session_state.get('colaboradores', []))} colaboradores no formulário")

def renderizar_gerador_escalas():
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Período contábil
        st.subheader("📆 Período Contábil")
        data_inicio = st.date_input(
            "Data de Início",
            value=date.today().replace(day=1),
            format="DD/MM/YYYY"
        )
        
        data_fim = st.date_input(
            "Data de Fim",
            value=date.today().replace(day=28),
            format="DD/MM/YYYY"
        )
        
        # Validação do período
        if data_inicio >= data_fim:
            st.error("A data de início deve ser anterior à data de fim!")
            return
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Upload de Dados")
        
        # Upload da planilha de colaboradores
        st.subheader("👥 Colaboradores")
        
        # Opção para usar colaboradores do formulário
        if st.session_state.get('colaboradores_formulario'):
            st.success(f"✅ {len(st.session_state.colaboradores_formulario)} colaboradores disponíveis do formulário!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 Usar Colaboradores do Formulário", type="primary"):
                    # Converter colaboradores do formulário para DataFrame
                    df_colaboradores_form = pd.DataFrame(st.session_state.colaboradores_formulario)
                    st.session_state.df_colaboradores_formulario = df_colaboradores_form
                    st.success("✅ Colaboradores do formulário carregados com sucesso!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Limpar Colaboradores do Formulário"):
                    st.session_state.colaboradores_formulario = None
                    st.session_state.df_colaboradores_formulario = None
                    st.success("✅ Colaboradores do formulário removidos!")
                    st.rerun()
        else:
            st.info("💡 **Dica**: Adicione colaboradores no formulário da aba 'Formulário de Colaboradores' para usar aqui!")
        
        # Botão para download do template
        template_bytes = criar_template_colaboradores()
        st.download_button(
            label="📥 Download Template Colaboradores",
            data=template_bytes,
            file_name="template_colaboradores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Baixe o template para preencher com os dados dos colaboradores"
        )
        
        arquivo_colaboradores = st.file_uploader(
            "Selecione a planilha de colaboradores (.xlsx)",
            type=['xlsx'],
            help="Planilha deve conter as colunas: Nome, Cargo, Tipo_Escala, Turno, Atestados, Ferias, Escalas_Manuais, Ultimo_Plantao_Mes_Anterior, Ultimo_Domingo_Folga"
        )
        
        # Informações sobre os dados
        with st.expander("📋 Informações sobre os dados"):
            st.markdown("""
            **Colunas obrigatórias:**
            - **Nome**: Nome completo do colaborador
            - **Cargo**: Cargo/função do colaborador
            - **Tipo_Escala**: Código da escala (M44, T44, N44, etc.)
            - **Turno**: Turno de trabalho (Manhã, Tarde, Noite, Dia)
            
            **Colunas opcionais:**
            - **Atestados**: Datas de atestados (separadas por vírgula)
            - **Ferias**: Período de férias (DD/MM/YYYY-DD/MM/YYYY)
            - **Escalas_Manuais**: Datas de escalas manuais (separadas por vírgula)
            - **Ultimo_Plantao_Mes_Anterior**: Último plantão do mês anterior (DD/MM/YYYY) - para plantões
            - **Ultimo_Domingo_Folga**: Último domingo de folga (DD/MM/YYYY) - para escalas 6x1
            
            **Observações importantes:**
            - Para plantões (P_D, P_N, I_D, I_N): O sistema determina automaticamente se deve ser par ou ímpar baseado no último plantão
            - Para escalas 6x1: O sistema calcula corretamente as semanas sem domingo baseado no último domingo informado
            """)
        
        # Upload da planilha de feriados
        st.subheader("🎉 Feriados")
        arquivo_feriados = st.file_uploader(
            "Selecione a planilha de feriados (.xlsx)",
            type=['xlsx'],
            help="Planilha deve conter as colunas: Data, Descricao"
        )
    
    with col2:
        with st.expander("Mostrar tipos de escala e legendas"):
            st.header("🎨 Legenda")
            st.markdown("""
            **Cores da Escala:**
            - 🟢 **Verde**: Trabalho regular
            - 🔵 **Azul**: Folga
            - ⚫ **Cinza**: Feriado
            - 🟣 **Roxo**: Escala manual
            - 🟠 **Laranja**: Atestado
            - 🟡 **Amarelo**: Férias
            """)
            st.subheader("📋 Tipos de Escala")
            st.markdown("""
            **Escalas 44H:**
            - **M44**: 44H - Manhã (Segunda a sexta, 8h/dia)
            - **T44**: 44H - Tarde (Segunda a sexta, 8h/dia)
            - **N44**: 44H - Noite (Segunda a sexta, 8h/dia)
            
            **Escalas 40H:**
            - **M40**: 40H - Manhã (Segunda a sexta, 8h/dia)
            - **T40**: 40H - Tarde (Segunda a sexta, 8h/dia)
            - **N40**: 40H - Noite (Segunda a sexta, 8h/dia)
            
            **Escalas 6X1:**
            - **M6X1**: 6x1 - Manhã (6 dias trabalho, 1 dia folga)
            - **T6X1**: 6x1 - Tarde (6 dias trabalho, 1 dia folga)
            - **N6X1**: 6x1 - Noite (6 dias trabalho, 1 dia folga)
            
            **Plantões:**
            - **P_D**: Plantão Par - Dia (dias pares do mês)
            - **P_N**: Plantão Par - Noite (dias pares do mês)
            - **I_D**: Plantão Ímpar - Dia (dias ímpares do mês)
            - **I_N**: Plantão Ímpar - Noite (dias ímpares do mês)
            """)
    
    # Processamento dos dados
    colaboradores_disponiveis = arquivo_colaboradores or st.session_state.get('df_colaboradores_formulario') is not None
    feriados_disponiveis = arquivo_feriados
    
    # Indicador visual de origem dos dados
    if st.session_state.get('df_colaboradores_formulario') is not None:
        st.info("📋 **Usando colaboradores do formulário** - Faça upload da planilha de feriados para continuar")
    elif arquivo_colaboradores:
        st.info("📄 **Usando colaboradores do arquivo** - Faça upload da planilha de feriados para continuar")
    
    if colaboradores_disponiveis and feriados_disponiveis:
        st.markdown("---")
        st.header("🔄 Processando Dados")
        
        try:
            # Ler dados de colaboradores
            if st.session_state.get('df_colaboradores_formulario') is not None:
                df_colaboradores = st.session_state.df_colaboradores_formulario
                st.success(f"✅ {len(df_colaboradores)} colaboradores carregados do formulário")
                
                # Mostrar preview dos colaboradores carregados
                with st.expander("👀 Preview dos Colaboradores Carregados"):
                    st.dataframe(df_colaboradores[['Nome', 'Cargo', 'Tipo_Escala', 'Turno']], use_container_width=True)
            else:
                with st.spinner("Lendo planilha de colaboradores..."):
                    df_colaboradores = ler_planilha_colaboradores(arquivo_colaboradores)
                    st.success(f"✅ {len(df_colaboradores)} colaboradores carregados do arquivo")
            
            # Ler dados de feriados
            with st.spinner("Lendo planilha de feriados..."):
                df_feriados = ler_planilha_feriados(arquivo_feriados)
                st.success(f"✅ {len(df_feriados)} feriados carregados")
            
            # Gerar escala
            if st.button("🚀 Gerar Escala", type="primary"):
                with st.spinner("Gerando escala..."):
                    gerador = GeradorEscala(data_inicio, data_fim, df_feriados)
                    escala_completa = gerador.gerar_escala_completa(df_colaboradores)
                    
                    # Salvar escala no session_state para evitar perda
                    st.session_state.escala_completa = escala_completa
                    st.session_state.escala_formatada = gerador.exportar_escala_formatada(escala_completa)
                    st.session_state.gerador = gerador
                    
                    st.success("✅ Escala gerada com sucesso!")
            
            # Verificar se há escala salva no session_state
            if hasattr(st.session_state, 'escala_completa') and st.session_state.escala_completa is not None:
                escala_completa = st.session_state.escala_completa
                escala_formatada = st.session_state.escala_formatada
                gerador = st.session_state.gerador
                
                # Exibir resultados
                st.markdown("---")
                st.header("📋 Resultados")
                
                # Tabela interativa
                # Tabela formatada tipo planilha (linha = colaborador / coluna = data)
                st.subheader("📆 Escala Formatada por Datas")

                if not escala_formatada.empty:
                    # Legenda visual
                    st.caption("""
                    🟢 TRABALHO | 🔵 FOLGA | ⚫ FERIADO | 🟣 ESCALA MANUAL | 🟠 ATESTADO | 🟡 FÉRIAS
                    """)

                    st.dataframe(escala_formatada, use_container_width=True)
                else:
                    st.warning("⚠️ Não foi possível formatar a escala para visualização.")

                
                # Relatórios específicos
                col1, col2 = st.columns(2)
                
                with col1:
                    # Relatório 6x1
                    relatorio_6x1 = gerador.gerar_relatorio_6x1(escala_completa)
                    if not relatorio_6x1.empty:
                        st.subheader("📅 Controle Escalas 6x1")
                        
                        # Informações sobre o relatório
                        with st.expander("ℹ️ Informações sobre o Controle 6x1"):
                            st.markdown("""
                            **Este relatório mostra:**
                            - **Último Domingo Folga**: Data do último domingo de folga informado
                            - **Próximo Domingo Folga**: Data calculada do próximo domingo que deve folgar (7 semanas depois)
                            - **Domingos Folgados**: Quantidade de domingos de folga no período atual
                            - **Semanas Sem Domingo**: Quantidade de semanas sem folgar no domingo
                            - **Status**: ⚠️ ATENÇÃO (quando ≥ 6 semanas sem domingo) ou ✅ OK
                            """)
                        
                        # Exibir relatório
                        st.dataframe(relatorio_6x1, use_container_width=True)
                        
                        # Estatísticas do relatório
                        total_6x1 = len(relatorio_6x1)
                        com_atencao = len(relatorio_6x1[relatorio_6x1['Status_Controle'] == '⚠️ ATENÇÃO'])
                        
                        st.info(f"📊 **Resumo 6x1**: {total_6x1} colaboradores | {com_atencao} precisam de atenção")
                
                with col2:
                    # Relatório Plantões
                    relatorio_plantoes = gerador.gerar_relatorio_plantoes(escala_completa)
                    if not relatorio_plantoes.empty:
                        st.subheader("🏥 Controle Plantões")
                        
                        # Informações sobre o relatório
                        with st.expander("ℹ️ Informações sobre o Controle Plantões"):
                            st.markdown("""
                            **Este relatório mostra:**
                            - **Dias Trabalho**: Quantidade de dias trabalhados no período
                            - **Dias Folga**: Quantidade de dias de folga no período
                            - **Último Plantão Mês**: Data do último plantão do mês atual
                            """)
                        
                        # Exibir relatório
                        st.dataframe(relatorio_plantoes, use_container_width=True)
                        
                        # Estatísticas do relatório
                        total_plantoes = len(relatorio_plantoes)
                        st.info(f"📊 **Resumo Plantões**: {total_plantoes} plantonistas")
                
                # Botões de download
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Download Excel"):
                        try:
                            import io
                            output = io.BytesIO()
                            escala_formatada.to_excel(output, index=False, engine='openpyxl')
                            output.seek(0)
                            st.download_button(
                                label="💾 Baixar Escala Excel",
                                data=output,
                                file_name=f"escala_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        except Exception as e:
                            st.error(f"Erro ao gerar Excel: {e}")
                
                with col2:
                    if st.button("📄 Download PDF"):
                        try:
                            pdf_exporter = PDFExporter()
                            pdf_bytes = pdf_exporter.exportar_pdf(escala_formatada)
                            st.download_button(
                                label="💾 Baixar Escala PDF",
                                data=pdf_bytes,
                                file_name=f"escala_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.error(f"Erro ao gerar PDF: {e}")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar dados: {str(e)}")
            st.exception(e)
    
    elif colaboradores_disponiveis or feriados_disponiveis:
        st.warning("⚠️ Por favor, forneça tanto os dados de colaboradores quanto os feriados para continuar.")
        if not colaboradores_disponiveis:
            st.info("💡 **Dica**: Você pode adicionar colaboradores usando o formulário na aba 'Formulário de Colaboradores' ou fazer upload de uma planilha.")
        if not feriados_disponiveis:
            st.info("💡 **Dica**: Faça upload da planilha de feriados para continuar.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>Sistema de Geração de Escalas de Trabalho - Conforme CLT Brasileira</p>
        <p>Desenvolvido para otimizar processos de RH e garantir conformidade legal</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 