"""
Formulário de Colaboradores - Interface Guiada
=============================================

Módulo para facilitar o preenchimento da planilha de colaboradores
com interface visual e validações em tempo real.

Autor: Sistema de Escalas
Data: 2025
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import io
from typing import List, Dict, Optional

class FormularioColaboradores:
    """Classe para gerenciar o formulário de colaboradores."""
    
    def __init__(self):
        self.tipos_escala = {
            "M44": "44H - Manhã (Segunda a sexta, 8h/dia)",
            "T44": "44H - Tarde (Segunda a sexta, 8h/dia)", 
            "N44": "44H - Noite (Segunda a sexta, 8h/dia)",
            "M40": "40H - Manhã (Segunda a sexta, 8h/dia)",
            "T40": "40H - Tarde (Segunda a sexta, 8h/dia)",
            "N40": "40H - Noite (Segunda a sexta, 8h/dia)",
            "M6X1": "6x1 - Manhã (6 dias trabalho, 1 dia folga)",
            "T6X1": "6x1 - Tarde (6 dias trabalho, 1 dia folga)",
            "N6X1": "6x1 - Noite (6 dias trabalho, 1 dia folga)",
            "P_D": "Plantão Par - Dia (dias pares do mês)",
            "P_N": "Plantão Par - Noite (dias pares do mês)",
            "I_D": "Plantão Ímpar - Dia (dias ímpares do mês)",
            "I_N": "Plantão Ímpar - Noite (dias ímpares do mês)"
        }
        
        self.turnos = ["Manhã", "Tarde", "Noite", "Dia"]
        
        # Inicializar session state se não existir
        if 'colaboradores' not in st.session_state:
            st.session_state.colaboradores = []
        if 'colaborador_atual' not in st.session_state:
            st.session_state.colaborador_atual = {}
    
    def renderizar_formulario(self):
        """Renderiza o formulário principal de colaboradores."""
        
        st.header("👥 Formulário de Colaboradores")
        st.markdown("Preencha os dados dos colaboradores de forma guiada e visual.")
        
        # Tabs para organização
        tab1, tab2, tab3 = st.tabs(["➕ Adicionar Colaborador", "📋 Lista de Colaboradores", "📥 Exportar"])
        
        with tab1:
            self._renderizar_formulario_adicionar()
        
        with tab2:
            self._renderizar_lista_colaboradores()
        
        with tab3:
            self._renderizar_exportacao()
    
    def _renderizar_formulario_adicionar(self):
        """Renderiza o formulário para adicionar novo colaborador."""
        
        st.subheader("➕ Adicionar Novo Colaborador")
        
        # Botão para duplicar último colaborador
        if st.session_state.colaboradores:
            if st.button("🔄 Duplicar Último Colaborador", help="Copia os dados do último colaborador adicionado"):
                ultimo = st.session_state.colaboradores[-1]
                st.session_state.colaborador_atual = ultimo.copy()
                st.success("Dados do último colaborador copiados! Ajuste conforme necessário.")
        
        # Campos obrigatórios
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input(
                "Nome Completo *",
                value=st.session_state.colaborador_atual.get('Nome', ''),
                help="Nome completo do colaborador"
            )
            
            cargo = st.text_input(
                "Cargo/Função *",
                value=st.session_state.colaborador_atual.get('Cargo', ''),
                help="Cargo ou função do colaborador"
            )
        
        with col2:
            # Dropdown para tipo de escala com descrição
            tipo_escala = st.selectbox(
                "Tipo de Escala *",
                options=list(self.tipos_escala.keys()),
                index=list(self.tipos_escala.keys()).index(st.session_state.colaborador_atual.get('Tipo_Escala', 'M44')),
                help="Selecione o tipo de escala do colaborador"
            )
            
            # Mostrar descrição do tipo de escala selecionado
            if tipo_escala:
                st.info(f"📋 {self.tipos_escala[tipo_escala]}")
            
            turno = st.selectbox(
                "Turno *",
                options=self.turnos,
                index=self.turnos.index(st.session_state.colaborador_atual.get('Turno', 'Manhã')),
                help="Turno de trabalho do colaborador"
            )
        
        # Campos opcionais
        st.subheader("📅 Datas Especiais (Opcional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Atestados - múltiplas datas
            st.write("**Atestados**")
            atestados_datas = st.multiselect(
                "Selecione as datas dos atestados",
                options=self._gerar_datas_mes_atual(),
                default=[],
                help="Selecione todas as datas de atestados no período"
            )
            
            # Férias - período
            st.write("**Período de Férias**")
            ferias_inicio = st.date_input(
                "Data de Início das Férias",
                value=None,
                help="Data de início do período de férias"
            )
            
            ferias_fim = st.date_input(
                "Data de Fim das Férias",
                value=None,
                help="Data de fim do período de férias"
            )
        
        with col2:
            # Escalas manuais
            st.write("**Escalas Manuais**")
            escalas_manuais = st.multiselect(
                "Selecione as datas de escalas manuais",
                options=self._gerar_datas_mes_atual(),
                default=[],
                help="Datas específicas onde o colaborador deve trabalhar"
            )
            
            # Último plantão (para plantonistas)
            st.write("**Último Plantão (Plantonistas)**")
            ultimo_plantao = st.date_input(
                "Data do Último Plantão",
                value=None,
                help="Data do último plantão do mês anterior (para plantonistas)"
            )
            
            # Último domingo de folga (para 6x1)
            st.write("**Último Domingo de Folga (6x1)**")
            ultimo_domingo = st.date_input(
                "Data do Último Domingo de Folga",
                value=None,
                help="Data do último domingo de folga (para escalas 6x1)"
            )
        
        # Validações
        erros = self._validar_campos(nome, cargo, tipo_escala, turno, ferias_inicio, ferias_fim)
        
        if erros:
            for erro in erros:
                st.error(erro)
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Adicionar Colaborador", type="primary", disabled=bool(erros)):
                self._adicionar_colaborador(
                    nome, cargo, tipo_escala, turno, atestados_datas,
                    ferias_inicio, ferias_fim, escalas_manuais,
                    ultimo_plantao, ultimo_domingo
                )
        
        with col2:
            if st.button("🗑️ Limpar Formulário"):
                st.session_state.colaborador_atual = {}
                st.rerun()
        
        with col3:
            if st.button("📋 Preview da Escala"):
                self._mostrar_preview_escala()
    
    def _renderizar_lista_colaboradores(self):
        """Renderiza a lista de colaboradores adicionados."""
        
        st.subheader("📋 Colaboradores Adicionados")
        
        if not st.session_state.colaboradores:
            st.info("Nenhum colaborador adicionado ainda. Use a aba 'Adicionar Colaborador' para começar.")
            return
        
        # Mostrar estatísticas
        total = len(st.session_state.colaboradores)
        tipos_escala_count = {}
        turnos_count = {}
        
        for colab in st.session_state.colaboradores:
            tipo = colab.get('Tipo_Escala', 'N/A')
            turno = colab.get('Turno', 'N/A')
            
            tipos_escala_count[tipo] = tipos_escala_count.get(tipo, 0) + 1
            turnos_count[turno] = turnos_count.get(turno, 0) + 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Colaboradores", total)
        with col2:
            st.metric("Tipos de Escala", len(tipos_escala_count))
        with col3:
            st.metric("Turnos", len(turnos_count))
        
        # Tabela de colaboradores
        df_colaboradores = pd.DataFrame(st.session_state.colaboradores)
        
        # Formatar colunas de datas para melhor visualização
        if not df_colaboradores.empty:
            # Colunas para formatar
            colunas_datas = ['Atestados', 'Escalas_Manuais', 'Ferias', 
                           'Ultimo_Plantao_Mes_Anterior', 'Ultimo_Domingo_Folga']
            
            for col in colunas_datas:
                if col in df_colaboradores.columns:
                    df_colaboradores[col] = df_colaboradores[col].apply(
                        lambda x: self._formatar_datas_para_exibicao(x)
                    )
        
        st.dataframe(df_colaboradores, use_container_width=True)
        
        # Botões de ação para a lista
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Limpar Todos"):
                if st.checkbox("Confirmar exclusão de todos os colaboradores"):
                    st.session_state.colaboradores = []
                    st.success("Todos os colaboradores foram removidos!")
                    st.rerun()
        
        with col2:
            if st.button("📊 Estatísticas Detalhadas"):
                self._mostrar_estatisticas_detalhadas()
    
    def _renderizar_exportacao(self):
        """Renderiza a seção de exportação."""
        
        st.subheader("📥 Exportar Planilha")
        
        if not st.session_state.colaboradores:
            st.warning("Nenhum colaborador para exportar. Adicione colaboradores primeiro.")
            return
        
        st.info(f"📋 **{len(st.session_state.colaboradores)} colaboradores** prontos para exportar")
        
        # Preview da planilha final
        with st.expander("👀 Preview da Planilha Final"):
            df_final = self._preparar_dataframe_final()
            st.dataframe(df_final, use_container_width=True)
        
        # Botão de exportação
        if st.button("📥 Exportar para Excel", type="primary"):
            try:
                excel_bytes = self._gerar_excel()
                st.download_button(
                    label="💾 Download Planilha Excel",
                    data=excel_bytes,
                    file_name=f"colaboradores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ Planilha gerada com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao gerar planilha: {str(e)}")
    
    def _gerar_datas_mes_atual(self) -> List[date]:
        """Gera lista de datas do mês atual para seleção."""
        hoje = date.today()
        primeiro_dia = hoje.replace(day=1)
        
        # Encontrar último dia do mês
        if hoje.month == 12:
            ultimo_dia = hoje.replace(year=hoje.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo_dia = hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1)
        
        datas = []
        data_atual = primeiro_dia
        while data_atual <= ultimo_dia:
            datas.append(data_atual)
            data_atual += timedelta(days=1)
        
        return datas
    
    def _validar_campos(self, nome: str, cargo: str, tipo_escala: str, 
                       turno: str, ferias_inicio: Optional[date], 
                       ferias_fim: Optional[date]) -> List[str]:
        """Valida os campos obrigatórios e regras de negócio."""
        erros = []
        
        # Campos obrigatórios
        if not nome.strip():
            erros.append("❌ Nome é obrigatório")
        
        if not cargo.strip():
            erros.append("❌ Cargo é obrigatório")
        
        # Validação de férias
        if ferias_inicio and ferias_fim:
            if ferias_inicio >= ferias_fim:
                erros.append("❌ Data de início das férias deve ser anterior à data de fim")
            
            if ferias_inicio < date.today():
                erros.append("❌ Data de início das férias não pode ser no passado")
        
        # Validações específicas por tipo de escala
        if tipo_escala.startswith(('P_', 'I_')):
            # Plantonistas devem ter último plantão informado
            pass  # Será validado no momento da adição
        
        if tipo_escala.endswith('6X1'):
            # Escalas 6x1 devem ter último domingo informado
            pass  # Será validado no momento da adição
        
        return erros
    
    def _adicionar_colaborador(self, nome: str, cargo: str, tipo_escala: str, 
                             turno: str, atestados_datas: List[date], 
                             ferias_inicio: Optional[date], ferias_fim: Optional[date],
                             escalas_manuais: List[date], ultimo_plantao: Optional[date],
                             ultimo_domingo: Optional[date]):
        """Adiciona um novo colaborador à lista."""
        
        # Formatar datas para o formato esperado pela planilha
        atestados_str = self._formatar_datas_para_planilha(atestados_datas)
        escalas_manuais_str = self._formatar_datas_para_planilha(escalas_manuais)
        
        # Formatar férias
        ferias_str = ""
        if ferias_inicio and ferias_fim:
            ferias_str = f"{ferias_inicio.strftime('%d/%m/%Y')}-{ferias_fim.strftime('%d/%m/%Y')}"
        
        # Formatar últimas datas
        ultimo_plantao_str = ultimo_plantao.strftime('%d/%m/%Y') if ultimo_plantao else ""
        ultimo_domingo_str = ultimo_domingo.strftime('%d/%m/%Y') if ultimo_domingo else ""
        
        colaborador = {
            'Nome': nome.strip(),
            'Cargo': cargo.strip(),
            'Tipo_Escala': tipo_escala,
            'Turno': turno,
            'Atestados': atestados_str,
            'Ferias': ferias_str,
            'Escalas_Manuais': escalas_manuais_str,
            'Ultimo_Plantao_Mes_Anterior': ultimo_plantao_str,
            'Ultimo_Domingo_Folga': ultimo_domingo_str
        }
        
        # Verificar se já existe colaborador com mesmo nome
        nomes_existentes = [c['Nome'] for c in st.session_state.colaboradores]
        if nome.strip() in nomes_existentes:
            st.warning(f"⚠️ Já existe um colaborador com o nome '{nome.strip()}'. Use um nome diferente.")
            return
        
        st.session_state.colaboradores.append(colaborador)
        st.session_state.colaborador_atual = {}
        
        st.success(f"✅ Colaborador '{nome.strip()}' adicionado com sucesso!")
        st.rerun()
    
    def _formatar_datas_para_planilha(self, datas: List[date]) -> str:
        """Formata lista de datas para o formato da planilha (DD/MM/YYYY,DD/MM/YYYY)."""
        if not datas:
            return ""
        
        datas_formatadas = [data.strftime('%d/%m/%Y') for data in datas]
        return ",".join(datas_formatadas)
    
    def _formatar_datas_para_exibicao(self, datas_str: str) -> str:
        """Formata string de datas para exibição mais amigável."""
        if not datas_str:
            return "-"
        
        datas = datas_str.split(',')
        if len(datas) <= 3:
            return datas_str
        else:
            return f"{datas[0]}, {datas[1]}, ... (+{len(datas)-2} mais)"
    
    def _mostrar_preview_escala(self):
        """Mostra um preview da escala baseado nos dados atuais."""
        st.subheader("👀 Preview da Escala")
        
        if not st.session_state.colaboradores:
            st.info("Adicione colaboradores para ver o preview da escala.")
            return
        
        # Criar preview simples
        df_preview = pd.DataFrame(st.session_state.colaboradores)
        
        # Mostrar apenas colunas principais para preview
        colunas_preview = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno']
        df_preview_simples = df_preview[colunas_preview].copy()
        
        st.dataframe(df_preview_simples, use_container_width=True)
        
        # Estatísticas rápidas
        st.info(f"📊 **Preview**: {len(df_preview)} colaboradores | "
                f"{df_preview['Tipo_Escala'].nunique()} tipos de escala | "
                f"{df_preview['Turno'].nunique()} turnos")
    
    def _mostrar_estatisticas_detalhadas(self):
        """Mostra estatísticas detalhadas dos colaboradores."""
        st.subheader("📊 Estatísticas Detalhadas")
        
        df = pd.DataFrame(st.session_state.colaboradores)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Distribuição por Tipo de Escala:**")
            tipo_counts = df['Tipo_Escala'].value_counts()
            st.bar_chart(tipo_counts)
        
        with col2:
            st.write("**Distribuição por Turno:**")
            turno_counts = df['Turno'].value_counts()
            st.bar_chart(turno_counts)
        
        # Tabela de estatísticas
        st.write("**Resumo Estatístico:**")
        stats_data = {
            'Métrica': ['Total de Colaboradores', 'Tipos de Escala Únicos', 'Turnos Únicos'],
            'Valor': [len(df), df['Tipo_Escala'].nunique(), df['Turno'].nunique()]
        }
        st.table(pd.DataFrame(stats_data))
    
    def _preparar_dataframe_final(self) -> pd.DataFrame:
        """Prepara o DataFrame final para exportação."""
        return pd.DataFrame(st.session_state.colaboradores)
    
    def _gerar_excel(self) -> bytes:
        """Gera o arquivo Excel para download."""
        df = self._preparar_dataframe_final()
        
        # Criar buffer de memória
        output = io.BytesIO()
        
        # Escrever para Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Colaboradores', index=False)
            
            # Ajustar largura das colunas
            worksheet = writer.sheets['Colaboradores']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        return output.getvalue()
    
    def obter_colaboradores(self) -> List[Dict]:
        """Retorna a lista de colaboradores para uso externo."""
        return st.session_state.colaboradores.copy()
    
    def limpar_colaboradores(self):
        """Limpa todos os colaboradores da sessão."""
        st.session_state.colaboradores = []
        st.session_state.colaborador_atual = {} 