"""
Gerador de Escalas de Trabalho
==============================

Módulo principal para geração de escalas de trabalho automatizadas
respeitando as regras da CLT brasileira.
"""

import pandas as pd
from datetime import date, timedelta, datetime
from typing import Dict, List, Any
import streamlit as st

from regras_clt import RegrasCLT

class GeradorEscala:
    """Classe principal para geração de escalas de trabalho."""
    
    def __init__(self, data_inicio: date, data_fim: date, feriados: pd.DataFrame):
        """
        Inicializa o gerador de escalas.
        
        Args:
            data_inicio: Data de início do período
            data_fim: Data de fim do período
            feriados: DataFrame com os feriados do período
        """
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.feriados = self._processar_feriados(feriados)
        self.regras_clt = RegrasCLT()
        
        # Cores para visualização
        self.cores = {
            'TRABALHO_MANHA': '🟢',
            'TRABALHO_TARDE': '🟢',
            'TRABALHO_NOITE': '🟢',
            'TRABALHO_DIA': '🟢',
            'FOLGA': '🔵',
            'FERIADO': '⚫',
            'ESCALA MANUAL': '🟣',
            'ATESTADO': '🟠',
            'FÉRIAS': '🟡'
        }
    
    def _processar_feriados(self, df_feriados: pd.DataFrame) -> List[date]:
        """
        Processa o DataFrame de feriados para extrair as datas.
        
        Args:
            df_feriados: DataFrame com colunas 'Data' e 'Descricao'
            
        Returns:
            Lista de objetos date dos feriados
        """
        feriados = []
        if df_feriados is not None and not df_feriados.empty:
            for _, row in df_feriados.iterrows():
                if pd.notna(row['Data']):
                    if isinstance(row['Data'], str):
                        # Converter string para date
                        try:
                            for formato in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                                try:
                                    data_feriado = pd.to_datetime(row['Data'], format=formato).date()
                                    feriados.append(data_feriado)
                                    break
                                except:
                                    continue
                        except:
                            continue
                    else:
                        # Já é um objeto date
                        feriados.append(row['Data'])
        
        return feriados
    
    def gerar_escala_completa(self, df_colaboradores: pd.DataFrame) -> pd.DataFrame:
        """
        Gera a escala completa para todos os colaboradores.
        
        Args:
            df_colaboradores: DataFrame com os dados dos colaboradores
            
        Returns:
            DataFrame com a escala completa
        """
        if df_colaboradores.empty:
            return pd.DataFrame()
        
        escalas = []
        dados_completos = []  # Para relatórios específicos
        
        for _, colaborador in df_colaboradores.iterrows():
            escala_colaborador = self._gerar_escala_colaborador(colaborador)
            if not escala_colaborador.empty:
                escalas.append(escala_colaborador)
                
                # Manter dados completos para relatórios específicos
                dados_completos.extend(escala_colaborador.to_dict('records'))
        
        if not escalas:
            return pd.DataFrame()
        
        # Concatenar todas as escalas
        escala_completa = pd.concat(escalas, ignore_index=True)
        
        # Armazenar dados completos para uso nos relatórios
        self._dados_completos = pd.DataFrame(dados_completos)
        
        # Para a escala completa, retornar apenas as colunas básicas
        colunas_escala_completa = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno', 'Data', 'Status', 'Status_Colorido']
        
        return escala_completa[colunas_escala_completa]
    
    def _gerar_escala_colaborador(self, colaborador: pd.Series) -> pd.DataFrame:
        """
        Gera a escala para um colaborador específico.
        
        Args:
            colaborador: Série pandas com os dados do colaborador
            
        Returns:
            DataFrame com a escala do colaborador
        """
        nome = colaborador['Nome']
        tipo_escala = colaborador['Tipo_Escala']
        turno = colaborador['Turno']
        atestados = colaborador.get('Atestados', '')
        ferias = colaborador.get('Ferias', '')
        escalas_manuais = colaborador.get('Escalas_Manuais', '')
        ultimo_plantao_mes_anterior = colaborador.get('Ultimo_Plantao_Mes_Anterior', '')
        ultimo_domingo_folga = colaborador.get('Ultimo_Domingo_Folga', '')
        
        # Processar último plantão do mês anterior
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
        
        # Processar último domingo de folga
        ultimo_domingo = None
        if ultimo_domingo_folga and str(ultimo_domingo_folga).strip():
            valor = str(ultimo_domingo_folga).strip()
            convertido = False
            for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S']:
                try:
                    ultimo_domingo = datetime.strptime(valor, formato).date()
                    convertido = True
                    break
                except ValueError:
                    continue
            if not convertido:
                try:
                    # Tentar converter se vier como datetime do pandas
                    if hasattr(ultimo_domingo_folga, 'date'):
                        ultimo_domingo = ultimo_domingo_folga.date()
                        convertido = True
                except Exception:
                    pass
            if not convertido:
                if tipo_escala.startswith('M6X1') or tipo_escala.startswith('T6X1') or tipo_escala.startswith('N6X1'):
                    st.warning(f"Não foi possível converter o campo 'Ultimo_Domingo_Folga' para o colaborador: {nome}. Valor recebido: '{valor}'")
        
        # Para plantões, determinar automaticamente o tipo baseado no último plantão
        if tipo_escala.startswith('P_') or tipo_escala.startswith('I_'):
            tipo_escala_original = tipo_escala
            
            # Determinar o tipo inicial considerando a regra de alternância
            tipo_atual = self._determinar_tipo_plantao_inicial(tipo_escala, self.data_inicio, ultimo_plantao)
            
            # Se houve mudança no tipo inicial, mostrar aviso
            if tipo_atual != tipo_escala_original:
                st.info(f"🔄 Colaborador {nome}: Tipo de plantão ajustado de {tipo_escala_original} para {tipo_atual} devido à regra de alternância (mês anterior com 31 dias).")
            
            data_atual = self.data_inicio
            data_fim = self.data_fim
            escalas_mes = []
            ultimo_plantao = None
            avisos_mudanca = []
            tipos_utilizados = [tipo_atual]  # Lista para rastrear todos os tipos utilizados
            
            while data_atual <= data_fim:
                # Determinar o último dia do mês atual
                ultimo_dia_mes = (data_atual.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                fim_periodo = min(ultimo_dia_mes, data_fim)
                
                # Gerar escala para o mês atual
                escala_mes = self.regras_clt.gerar_escala_base(
                    tipo_atual, data_atual, fim_periodo, self.feriados, ultimo_plantao
                )
                
                # Adicionar tipo vigente em cada dia
                for data in escala_mes:
                    escala_mes[data] = (escala_mes[data], tipo_atual)
                escalas_mes.append(escala_mes)
                
                # Preparar para o próximo mês
                ultimo_plantao = fim_periodo
                
                # Avançar para o próximo mês
                data_atual = fim_periodo + timedelta(days=1)
                
                if data_atual <= data_fim:
                    # REGRA DE ALTERNÂNCIA: Trocar a paridade apenas se o mês terminar em 31
                    if ultimo_dia_mes.day == 31:
                        tipo_novo = self.regras_clt.determinar_tipo_plantao_automatico(ultimo_plantao, tipo_atual)
                        if tipo_novo != tipo_atual:
                            avisos_mudanca.append((fim_periodo, tipo_atual, tipo_novo))
                            tipos_utilizados.append(tipo_novo)  # Adicionar novo tipo à lista
                        tipo_atual = tipo_novo
                    # Para meses com 28, 29 ou 30 dias, a paridade é mantida e tipo_atual não muda.
            
            # Concatenar todas as escalas dos meses
            escala_base = {}
            for escala_mes in escalas_mes:
                escala_base.update(escala_mes)
            info_controle = {}
            
            # Mostrar avisos de mudança de tipo durante o período
            for data_mudanca, tipo_ant, tipo_novo in avisos_mudanca:
                st.warning(f"Colaborador {nome}: Tipo de plantão alterado automaticamente de {tipo_ant} para {tipo_novo} a partir de {data_mudanca + timedelta(days=1):%d/%m/%Y}.")
            
            # Criar tipo concatenado se houve mudanças
            if len(tipos_utilizados) > 1:
                tipo_escala_final = " - ".join(tipos_utilizados)
            else:
                tipo_escala_final = tipos_utilizados[0]
            
            # Atualizar tipo_escala para o tipo concatenado
            tipo_escala = tipo_escala_final
        # Gerar escala base para outros tipos
        elif tipo_escala.startswith('M6X1') or tipo_escala.startswith('T6X1') or tipo_escala.startswith('N6X1'):
            resultado = self.regras_clt.gerar_escala_base(
                tipo_escala, self.data_inicio, self.data_fim, self.feriados, 
                ultimo_plantao, ultimo_domingo
            )
            if isinstance(resultado, tuple):
                escala_base, info_controle = resultado
            else:
                escala_base = resultado
                info_controle = {}
        else:
            escala_base = self.regras_clt.gerar_escala_base(
                tipo_escala, self.data_inicio, self.data_fim, self.feriados, ultimo_plantao
            )
            info_controle = {}
        
        # Aplicar exceções
        escala_final = self.regras_clt.aplicar_excecoes(
            escala_base, atestados, ferias, escalas_manuais
        )
        
        # Converter para DataFrame
        dados_escala = []
        for data, status in escala_final.items():
            if isinstance(status, tuple):
                status_real, tipo_vigente = status
            else:
                status_real = status
                tipo_vigente = tipo_escala
            dados_escala.append({
                'Nome': nome,
                'Cargo': colaborador['Cargo'],
                'Tipo_Escala': tipo_escala,  # Usar o tipo concatenado para todos os dias
                'Turno': turno,
                'Data': data,
                'Status': status_real,
                'Status_Colorido': f"{self.cores.get(status_real, '⚪')} {status_real}",
                'Ultimo_Domingo_Folga': info_controle.get('ultimo_domingo_folga', ''),
                'Domingos_Folgados': info_controle.get('domingos_folgados', 0),
                'Semanas_Sem_Domingo': info_controle.get('semanas_sem_domingo', 0)
            })
        
        df_escala = pd.DataFrame(dados_escala)
        
        # Para a escala completa, retornar apenas as colunas básicas
        # As colunas de controle 6x1 serão usadas apenas nos relatórios específicos
        colunas_escala_completa = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno', 'Data', 'Status', 'Status_Colorido']
        
        # Retornar dados completos para uso interno
        return df_escala
    
    def validar_escalas(self, df_colaboradores: pd.DataFrame) -> Dict[str, Any]:
        """
        Valida todas as escalas geradas.
        
        Args:
            df_colaboradores: DataFrame com os dados dos colaboradores
            
        Returns:
            Dict com resultados da validação
        """
        resultados = {
            'valido': True,
            'erros': [],
            'avisos': [],
            'estatisticas': {}
        }
        
        for _, colaborador in df_colaboradores.iterrows():
            nome = colaborador['Nome']
            tipo_escala = colaborador['Tipo_Escala']
            
            # Gerar escala para validação
            escala_base = self.regras_clt.gerar_escala_base(
                tipo_escala, self.data_inicio, self.data_fim, self.feriados
            )
            
            # Validar escala
            validacao = self.regras_clt.validar_escala(escala_base, tipo_escala)
            
            if not validacao['valida']:
                resultados['valido'] = False
                for erro in validacao['erros']:
                    resultados['erros'].append(f"{nome}: {erro}")
            
            for aviso in validacao['avisos']:
                resultados['avisos'].append(f"{nome}: {aviso}")
        
        return resultados
    
    def gerar_resumo_estatisticas(self, escala_completa: pd.DataFrame) -> pd.DataFrame:
        """
        Gera resumo estatístico da escala completa.
        
        Args:
            escala_completa: DataFrame com a escala completa
            
        Returns:
            DataFrame com estatísticas por colaborador
        """
        if escala_completa.empty:
            return pd.DataFrame()
        
        # Agrupar por colaborador e status
        estatisticas = escala_completa.groupby(['Nome', 'Status']).size().unstack(fill_value=0)
        
        # Adicionar totais
        estatisticas['Total_Dias'] = estatisticas.sum(axis=1)
        
        # Calcular percentuais
        for col in estatisticas.columns:
            if col != 'Total_Dias':
                estatisticas[f'{col}_%'] = (estatisticas[col] / estatisticas['Total_Dias'] * 100).round(1)
        
        return estatisticas
    
    def filtrar_escala(self, escala_completa: pd.DataFrame, 
                      filtros: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Filtra a escala completa com base nos critérios fornecidos.
        
        Args:
            escala_completa: DataFrame com a escala completa
            filtros: Dict com filtros a aplicar
            
        Returns:
            DataFrame filtrado
        """
        if filtros is None:
            return escala_completa
        
        df_filtrado = escala_completa.copy()
        
        # Filtro por nome
        if 'nome' in filtros and filtros['nome']:
            df_filtrado = df_filtrado[df_filtrado['Nome'].str.contains(filtros['nome'], case=False)]
        
        # Filtro por turno
        if 'turno' in filtros and filtros['turno']:
            df_filtrado = df_filtrado[df_filtrado['Turno'] == filtros['turno']]
        
        # Filtro por tipo de escala
        if 'tipo_escala' in filtros and filtros['tipo_escala']:
            df_filtrado = df_filtrado[df_filtrado['Tipo_Escala'] == filtros['tipo_escala']]
        
        # Filtro por status
        if 'status' in filtros and filtros['status']:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtros['status']]
        
        # Filtro por período
        if 'data_inicio' in filtros and filtros['data_inicio']:
            df_filtrado = df_filtrado[df_filtrado['Data'] >= filtros['data_inicio']]
        
        if 'data_fim' in filtros and filtros['data_fim']:
            df_filtrado = df_filtrado[df_filtrado['Data'] <= filtros['data_fim']]
        
        return df_filtrado
    
    def exportar_escala_formatada(self, escala_completa: pd.DataFrame) -> pd.DataFrame:
        """
        Formata a escala para exportação, organizando por colaborador e data.
        
        Args:
            escala_completa: DataFrame com a escala completa
            
        Returns:
            DataFrame formatado para exportação
        """
        if escala_completa.empty:
            return pd.DataFrame()
        
        # Pivotar a tabela para ter colaboradores como linhas e datas como colunas
        escala_pivot = escala_completa.pivot_table(
            index=['Nome', 'Cargo', 'Tipo_Escala', 'Turno'],
            columns='Data',
            values='Status_Colorido',
            aggfunc='first'
        ).reset_index()
        
        # Reorganizar colunas
        colunas_info = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno']
        colunas_datas = [col for col in escala_pivot.columns if col not in colunas_info]
        colunas_datas.sort()  # Ordenar datas
        
        escala_formatada = escala_pivot[colunas_info + colunas_datas]
        
        return escala_formatada
    
    def gerar_relatorio_6x1(self, escala_completa: pd.DataFrame) -> pd.DataFrame:
        """
        Gera relatório específico para colaboradores com escala 6x1.
        
        Args:
            escala_completa: DataFrame com a escala completa
            
        Returns:
            DataFrame com informações de controle 6x1
        """
        if not hasattr(self, '_dados_completos') or self._dados_completos.empty:
            return pd.DataFrame()
        
        # Usar dados completos que contêm as colunas de controle 6x1
        escala_6x1 = self._dados_completos[self._dados_completos['Tipo_Escala'].str.contains('6X1')]
        
        if escala_6x1.empty:
            return pd.DataFrame()
        
        # Agrupar por colaborador e pegar informações de controle
        relatorio = escala_6x1.groupby(['Nome', 'Cargo', 'Tipo_Escala', 'Turno']).agg({
            'Ultimo_Domingo_Folga': 'first',
            'Domingos_Folgados': 'max',
            'Semanas_Sem_Domingo': 'max'
        }).reset_index()
        
        # Processar e formatar as datas
        relatorio['Ultimo_Domingo_Folga_Formatado'] = relatorio['Ultimo_Domingo_Folga'].apply(
            lambda x: self._formatar_data(x) if x else 'Não informado'
        )
        
        # Calcular próximo domingo de folga
        relatorio['Proximo_Domingo_Folga'] = relatorio['Ultimo_Domingo_Folga'].apply(
            lambda x: self._calcular_proximo_domingo_folga(x) if x else 'Não calculável'
        )
        
        # Adicionar informações de controle
        relatorio['Status_Controle'] = relatorio['Semanas_Sem_Domingo'].apply(
            lambda x: '⚠️ ATENÇÃO' if x >= 6 else '✅ OK'
        )
        
        # Reorganizar colunas (incluindo a coluna original)
        colunas_ordenadas = [
            'Nome', 'Cargo', 'Tipo_Escala', 'Turno', 
            'Ultimo_Domingo_Folga', 'Ultimo_Domingo_Folga_Formatado', 'Proximo_Domingo_Folga',
            'Domingos_Folgados', 'Semanas_Sem_Domingo', 'Status_Controle'
        ]
        
        return relatorio[colunas_ordenadas]
    
    def _formatar_data(self, data) -> str:
        """
        Formata uma data para exibição.
        
        Args:
            data: Data a ser formatada
            
        Returns:
            String formatada da data
        """
        if not data:
            return 'Não informado'
        
        try:
            if isinstance(data, str):
                # Tentar diferentes formatos
                for formato in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        data_obj = datetime.strptime(data, formato).date()
                        return data_obj.strftime('%d/%m/%Y')
                    except ValueError:
                        continue
            elif hasattr(data, 'strftime'):
                return data.strftime('%d/%m/%Y')
            else:
                return str(data)
        except:
            return str(data) if data else 'Não informado'
    
    def _calcular_proximo_domingo_folga(self, ultimo_domingo: str) -> str:
        """
        Calcula o próximo domingo de folga baseado no último.
        
        Args:
            ultimo_domingo: Data do último domingo de folga
            
        Returns:
            String com a data do próximo domingo de folga
        """
        if not ultimo_domingo:
            return ''
        
        try:
            if isinstance(ultimo_domingo, str):
                for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                    try:
                        data = datetime.strptime(ultimo_domingo, formato).date()
                        break
                    except ValueError:
                        continue
            else:
                data = ultimo_domingo
            
            # Próximo domingo de folga (7 semanas depois)
            proximo_domingo = data + timedelta(weeks=7)
            return proximo_domingo.strftime('%d/%m/%Y')
        except:
            return ''
    
    def gerar_relatorio_plantoes(self, escala_completa: pd.DataFrame) -> pd.DataFrame:
        """
        Gera relatório específico para plantonistas.
        
        Args:
            escala_completa: DataFrame com a escala completa
            
        Returns:
            DataFrame com informações de controle dos plantões
        """
        if escala_completa.empty:
            return pd.DataFrame()
        
        # Filtrar apenas plantonistas
        plantoes = escala_completa[escala_completa['Tipo_Escala'].str.contains('P_|I_')]
        
        if plantoes.empty:
            return pd.DataFrame()
        
        # Calcular dias de trabalho e folga por colaborador
        relatorio_dados = []
        
        for (nome, cargo, tipo_escala, turno), grupo in plantoes.groupby(['Nome', 'Cargo', 'Tipo_Escala', 'Turno']):
            # Contar dias de trabalho (TRABALHO_DIA ou TRABALHO_NOITE)
            dias_trabalho = len(grupo[grupo['Status'].isin(['TRABALHO_DIA', 'TRABALHO_NOITE'])])
            
            # Contar dias de folga
            dias_folga = len(grupo[grupo['Status'] == 'FOLGA'])
            
            # Calcular total de dias no período
            total_dias = (self.data_fim - self.data_inicio).days + 1
            
            # Calcular último plantão do mês
            ultimo_plantao_mes = self._calcular_ultimo_plantao_mes(tipo_escala, self.data_fim)
            
            relatorio_dados.append({
                'Nome': nome,
                'Cargo': cargo,
                'Tipo_Escala': tipo_escala,
                'Turno': turno,
                'Dias_Trabalho': dias_trabalho,
                'Dias_Folga': dias_folga,
                'Total_Dias': total_dias,
                'Ultimo_Plantao_Mes': ultimo_plantao_mes
            })
        
        return pd.DataFrame(relatorio_dados)
    
    def _calcular_ultimo_plantao_mes(self, tipo_escala: str, data_fim: date) -> str:
        """
        Calcula o último plantão do mês baseado no tipo de escala.
        
        Args:
            tipo_escala: Tipo de escala do plantão
            data_fim: Data de fim do período
            
        Returns:
            String com a data do último plantão
        """
        try:
            # Encontrar o último dia do mês que corresponde ao tipo de plantão
            ultimo_dia = data_fim.replace(day=1) + timedelta(days=32)
            ultimo_dia = ultimo_dia.replace(day=1) - timedelta(days=1)
            
            if tipo_escala.startswith('P_'):  # Plantão par
                # Encontrar o último dia par do mês
                while ultimo_dia.day % 2 != 0:
                    ultimo_dia -= timedelta(days=1)
            else:  # Plantão ímpar
                # Encontrar o último dia ímpar do mês
                while ultimo_dia.day % 2 != 1:
                    ultimo_dia -= timedelta(days=1)
            
            return ultimo_dia.strftime('%d/%m/%Y')
        except:
            return ''
    
    def _verificar_mes_anterior_31_dias(self, data_inicio: date) -> bool:
        """
        Verifica se o mês anterior à data de início tem 31 dias.
        
        Args:
            data_inicio: Data de início da escala
            
        Returns:
            True se o mês anterior tem 31 dias, False caso contrário
        """
        # Calcular o último dia do mês anterior
        primeiro_dia_mes_atual = data_inicio.replace(day=1)
        ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
        
        # Verificar se o mês anterior tem 31 dias
        return ultimo_dia_mes_anterior.day == 31
    
    def _determinar_tipo_plantao_inicial(self, tipo_escala: str, data_inicio: date, ultimo_plantao_mes_anterior: date = None) -> str:
        """
        Determina o tipo de plantão inicial considerando a regra de alternância.
        
        REGRA: Se o mês anterior tiver 31 dias, inverte a paridade (P_ ↔ I_).
        Se o mês anterior tiver 30, 28 ou 29 dias, mantém o mesmo tipo.
        
        Args:
            tipo_escala: Tipo de escala original (P_D, P_N, I_D, I_N)
            data_inicio: Data de início da escala
            ultimo_plantao_mes_anterior: Último plantão do mês anterior (opcional)
            
        Returns:
            Tipo de plantão ajustado conforme a regra de alternância
        """
        if not tipo_escala.startswith('P_') and not tipo_escala.startswith('I_'):
            return tipo_escala
        
        # Se não há informação do último plantão, verificar apenas o mês anterior
        if not ultimo_plantao_mes_anterior:
            # Verificar se o mês anterior tem 31 dias
            if self._verificar_mes_anterior_31_dias(data_inicio):
                # Inverter paridade
                paridade, turno = tipo_escala.split('_')
                nova_paridade = 'I' if paridade == 'P' else 'P'
                return f"{nova_paridade}_{turno}"
            else:
                # Mantém o mesmo tipo
                return tipo_escala
        
        # Se há informação do último plantão, usar a função existente
        return self.regras_clt.determinar_tipo_plantao_automatico(ultimo_plantao_mes_anterior, tipo_escala) 