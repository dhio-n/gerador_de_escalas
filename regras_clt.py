"""
Módulo de Regras CLT
===================

Contém as regras de jornada de trabalho conforme a CLT brasileira
para cada tipo de escala implementado no sistema.
"""

from datetime import date, timedelta, datetime
from typing import List, Dict, Any, Tuple
import calendar

class RegrasCLT:
    """Classe que implementa as regras da CLT para diferentes tipos de escala."""
    
    def __init__(self):
        """Inicializa as regras CLT."""
        self.tipos_escala = {
            # Escalas 44H
            'M44': self._regra_44h_manha,
            'T44': self._regra_44h_tarde,
            'N44': self._regra_44h_noite,
            # Escalas 40H
            'M40': self._regra_40h_manha,
            'T40': self._regra_40h_tarde,
            'N40': self._regra_40h_noite,
            # Escalas 6X1
            'M6X1': self._regra_6x1_manha,
            'T6X1': self._regra_6x1_tarde,
            'N6X1': self._regra_6x1_noite,
            # Plantões
            'P_D': self._regra_plantao_par_dia,
            'P_N': self._regra_plantao_par_noite,
            'I_D': self._regra_plantao_impar_dia,
            'I_N': self._regra_plantao_impar_noite
        }
    
    def gerar_escala_base(self, tipo_escala: str, data_inicio: date, data_fim: date, 
                         feriados: List[date], ultimo_plantao_mes_anterior: date = None,
                         ultimo_domingo_folga: date = None) -> Dict[date, str]:
        """
        Gera a escala base para um tipo específico.
        
        Args:
            tipo_escala: Tipo de escala (M44, T44, N44, etc.)
            data_inicio: Data de início do período
            data_fim: Data de fim do período
            feriados: Lista de feriados do período
            ultimo_plantao_mes_anterior: Último plantão do mês anterior (para plantões)
            ultimo_domingo_folga: Último domingo de folga (para escalas 6x1)
            
        Returns:
            Dict com data como chave e status como valor
        """
        if tipo_escala not in self.tipos_escala:
            raise ValueError(f"Tipo de escala '{tipo_escala}' não suportado")
        
        if tipo_escala.startswith('P_') or tipo_escala.startswith('I_'):
            return self.tipos_escala[tipo_escala](data_inicio, data_fim, feriados, ultimo_plantao_mes_anterior)
        elif tipo_escala.startswith('M6X1') or tipo_escala.startswith('T6X1') or tipo_escala.startswith('N6X1'):
            return self.tipos_escala[tipo_escala](data_inicio, data_fim, feriados, ultimo_domingo_folga)
        else:
            return self.tipos_escala[tipo_escala](data_inicio, data_fim, feriados)
    
    def _regra_44h_manha(self, data_inicio: date, data_fim: date, feriados: List[date]) -> Dict[date, str]:
        """
        Regra para escala 44H - Manhã: Segunda a sexta, 8h/dia, turno manhã.
        Não trabalha em feriados nem fins de semana.
        """
        escala = {}
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            # Verificar se é fim de semana
            if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
                escala[data_atual] = "FOLGA"
            # Verificar se é feriado
            elif data_atual in feriados:
                escala[data_atual] = "FERIADO"
            # Dias úteis (segunda a sexta)
            else:
                escala[data_atual] = "TRABALHO_MANHA"
            
            data_atual += timedelta(days=1)
        
        return escala
    
    def _regra_44h_tarde(self, data_inicio: date, data_fim: date, feriados: List[date]) -> Dict[date, str]:
        """
        Regra para escala 44H - Tarde: Segunda a sexta, 8h/dia, turno tarde.
        Não trabalha em feriados nem fins de semana.
        """
        escala = {}
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            # Verificar se é fim de semana
            if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
                escala[data_atual] = "FOLGA"
            # Verificar se é feriado
            elif data_atual in feriados:
                escala[data_atual] = "FERIADO"
            # Dias úteis (segunda a sexta)
            else:
                escala[data_atual] = "TRABALHO_TARDE"
            
            data_atual += timedelta(days=1)
        
        return escala
    
    def _regra_44h_noite(self, data_inicio: date, data_fim: date, feriados: List[date]) -> Dict[date, str]:
        """
        Regra para escala 44H - Noite: Segunda a sexta, 8h/dia, turno noite.
        Não trabalha em feriados nem fins de semana.
        """
        escala = {}
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            # Verificar se é fim de semana
            if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
                escala[data_atual] = "FOLGA"
            # Verificar se é feriado
            elif data_atual in feriados:
                escala[data_atual] = "FERIADO"
            # Dias úteis (segunda a sexta)
            else:
                escala[data_atual] = "TRABALHO_NOITE"
            
            data_atual += timedelta(days=1)
        
        return escala
    
    def _regra_40h_manha(self, data_inicio: date, data_fim: date, feriados: List[date]) -> Dict[date, str]:
        """
        Regra para escala 40H - Manhã: Segunda a sexta, 8h/dia, turno manhã.
        Não trabalha em feriados nem fins de semana.
        """
        escala = {}
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            # Verificar se é fim de semana
            if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
                escala[data_atual] = "FOLGA"
            # Verificar se é feriado
            elif data_atual in feriados:
                escala[data_atual] = "FERIADO"
            # Dias úteis (segunda a sexta)
            else:
                escala[data_atual] = "TRABALHO_MANHA"
            
            data_atual += timedelta(days=1)
        
        return escala
    
    def _regra_40h_tarde(self, data_inicio: date, data_fim: date, feriados: List[date]) -> Dict[date, str]:
        """
        Regra para escala 40H - Tarde: Segunda a sexta, 8h/dia, turno tarde.
        Não trabalha em feriados nem fins de semana.
        """
        escala = {}
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            # Verificar se é fim de semana
            if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
                escala[data_atual] = "FOLGA"
            # Verificar se é feriado
            elif data_atual in feriados:
                escala[data_atual] = "FERIADO"
            # Dias úteis (segunda a sexta)
            else:
                escala[data_atual] = "TRABALHO_TARDE"
            
            data_atual += timedelta(days=1)
        
        return escala
    
    def _regra_40h_noite(self, data_inicio: date, data_fim: date, feriados: List[date]) -> Dict[date, str]:
        """
        Regra para escala 40H - Noite: Segunda a sexta, 8h/dia, turno noite.
        Não trabalha em feriados nem fins de semana.
        """
        escala = {}
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            # Verificar se é fim de semana
            if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
                escala[data_atual] = "FOLGA"
            # Verificar se é feriado
            elif data_atual in feriados:
                escala[data_atual] = "FERIADO"
            # Dias úteis (segunda a sexta)
            else:
                escala[data_atual] = "TRABALHO_NOITE"
            
            data_atual += timedelta(days=1)
        
        return escala
    
    def _regra_6x1_manha(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_domingo_folga: date = None) -> Tuple[Dict[date, str], Dict[str, Any]]:
        """
        Regra para escala 6X1 - Manhã: Trabalha 6 dias e folga 1, turno manhã.
        Deve folgar pelo menos um domingo a cada 7 semanas.
        """
        escala = {}
        data_atual = data_inicio
        dias_trabalhados = 0
        domingos_folgados = 0
        semanas_sem_domingo = 0
        ultimo_domingo_folga_local = ultimo_domingo_folga
        
        # Calcular semanas sem domingo baseado no último domingo informado
        if ultimo_domingo_folga:
            # Calcular quantas semanas se passaram desde o último domingo
            dias_desde_ultimo_domingo = (data_inicio - ultimo_domingo_folga).days
            semanas_sem_domingo = max(0, dias_desde_ultimo_domingo // 7)
        
        info_controle = {
            'ultimo_domingo_folga': ultimo_domingo_folga,
            'domingos_folgados': 0,
            'semanas_sem_domingo': semanas_sem_domingo
        }
        
        while data_atual <= data_fim:
            # Verificar se é domingo
            if data_atual.weekday() == 6:  # Domingo
                # Regra: 1 domingo de folga a cada 7 semanas, no mínimo
                if semanas_sem_domingo >= 6:  # Força folga no domingo
                    escala[data_atual] = "FOLGA"
                    domingos_folgados += 1
                    ultimo_domingo_folga_local = data_atual
                    semanas_sem_domingo = 0
                else:
                    # Verificar se já trabalhou 6 dias seguidos
                    if dias_trabalhados >= 6:
                        escala[data_atual] = "FOLGA"
                        domingos_folgados += 1
                        ultimo_domingo_folga_local = data_atual
                        dias_trabalhados = 0
                        semanas_sem_domingo = 0
                    else:
                        escala[data_atual] = "TRABALHO_MANHA"
                        dias_trabalhados += 1
                        semanas_sem_domingo += 1
            else:
                # Regra 6x1: 6 dias trabalho, 1 dia folga
                if dias_trabalhados < 6:
                    escala[data_atual] = "TRABALHO_MANHA"
                    dias_trabalhados += 1
                else:
                    escala[data_atual] = "FOLGA"
                    dias_trabalhados = 0
            
            data_atual += timedelta(days=1)
        
        info_controle['ultimo_domingo_folga'] = ultimo_domingo_folga_local
        info_controle['domingos_folgados'] = domingos_folgados
        info_controle['semanas_sem_domingo'] = semanas_sem_domingo
        
        return escala, info_controle
    
    def _regra_6x1_tarde(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_domingo_folga: date = None) -> Tuple[Dict[date, str], Dict[str, Any]]:
        """
        Regra para escala 6X1 - Tarde: Trabalha 6 dias e folga 1, turno tarde.
        Deve folgar pelo menos um domingo a cada 7 semanas.
        """
        escala = {}
        data_atual = data_inicio
        dias_trabalhados = 0
        domingos_folgados = 0
        semanas_sem_domingo = 0
        ultimo_domingo_folga_local = ultimo_domingo_folga
        
        # Calcular semanas sem domingo baseado no último domingo informado
        if ultimo_domingo_folga:
            # Calcular quantas semanas se passaram desde o último domingo
            dias_desde_ultimo_domingo = (data_inicio - ultimo_domingo_folga).days
            semanas_sem_domingo = max(0, dias_desde_ultimo_domingo // 7)
        
        info_controle = {
            'ultimo_domingo_folga': ultimo_domingo_folga,
            'domingos_folgados': 0,
            'semanas_sem_domingo': semanas_sem_domingo
        }
        
        while data_atual <= data_fim:
            # Verificar se é domingo
            if data_atual.weekday() == 6:  # Domingo
                # Regra: 1 domingo de folga a cada 7 semanas, no mínimo
                if semanas_sem_domingo >= 6:  # Força folga no domingo
                    escala[data_atual] = "FOLGA"
                    domingos_folgados += 1
                    ultimo_domingo_folga_local = data_atual
                    semanas_sem_domingo = 0
                else:
                    # Verificar se já trabalhou 6 dias seguidos
                    if dias_trabalhados >= 6:
                        escala[data_atual] = "FOLGA"
                        domingos_folgados += 1
                        ultimo_domingo_folga_local = data_atual
                        dias_trabalhados = 0
                        semanas_sem_domingo = 0
                    else:
                        escala[data_atual] = "TRABALHO_TARDE"
                        dias_trabalhados += 1
                        semanas_sem_domingo += 1
            else:
                # Regra 6x1: 6 dias trabalho, 1 dia folga
                if dias_trabalhados < 6:
                    escala[data_atual] = "TRABALHO_TARDE"
                    dias_trabalhados += 1
                else:
                    escala[data_atual] = "FOLGA"
                    dias_trabalhados = 0
            
            data_atual += timedelta(days=1)
        
        info_controle['ultimo_domingo_folga'] = ultimo_domingo_folga_local
        info_controle['domingos_folgados'] = domingos_folgados
        info_controle['semanas_sem_domingo'] = semanas_sem_domingo
        
        return escala, info_controle
    
    def _regra_6x1_noite(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_domingo_folga: date = None) -> Tuple[Dict[date, str], Dict[str, Any]]:
        """
        Regra para escala 6X1 - Noite: Trabalha 6 dias e folga 1, turno noite.
        Deve folgar pelo menos um domingo a cada 7 semanas.
        """
        escala = {}
        data_atual = data_inicio
        dias_trabalhados = 0
        domingos_folgados = 0
        semanas_sem_domingo = 0
        ultimo_domingo_folga_local = ultimo_domingo_folga
        
        # Calcular semanas sem domingo baseado no último domingo informado
        if ultimo_domingo_folga:
            # Calcular quantas semanas se passaram desde o último domingo
            dias_desde_ultimo_domingo = (data_inicio - ultimo_domingo_folga).days
            semanas_sem_domingo = max(0, dias_desde_ultimo_domingo // 7)
        
        info_controle = {
            'ultimo_domingo_folga': ultimo_domingo_folga,
            'domingos_folgados': 0,
            'semanas_sem_domingo': semanas_sem_domingo
        }
        
        while data_atual <= data_fim:
            # Verificar se é domingo
            if data_atual.weekday() == 6:  # Domingo
                # Regra: 1 domingo de folga a cada 7 semanas, no mínimo
                if semanas_sem_domingo >= 6:  # Força folga no domingo
                    escala[data_atual] = "FOLGA"
                    domingos_folgados += 1
                    ultimo_domingo_folga_local = data_atual
                    semanas_sem_domingo = 0
                else:
                    # Verificar se já trabalhou 6 dias seguidos
                    if dias_trabalhados >= 6:
                        escala[data_atual] = "FOLGA"
                        domingos_folgados += 1
                        ultimo_domingo_folga_local = data_atual
                        dias_trabalhados = 0
                        semanas_sem_domingo = 0
                    else:
                        escala[data_atual] = "TRABALHO_NOITE"
                        dias_trabalhados += 1
                        semanas_sem_domingo += 1
            else:
                # Regra 6x1: 6 dias trabalho, 1 dia folga
                if dias_trabalhados < 6:
                    escala[data_atual] = "TRABALHO_NOITE"
                    dias_trabalhados += 1
                else:
                    escala[data_atual] = "FOLGA"
                    dias_trabalhados = 0
            
            data_atual += timedelta(days=1)
        
        info_controle['ultimo_domingo_folga'] = ultimo_domingo_folga_local
        info_controle['domingos_folgados'] = domingos_folgados
        info_controle['semanas_sem_domingo'] = semanas_sem_domingo
        
        return escala, info_controle
    
    def _regra_plantao_par_dia(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_plantao_mes_anterior: date = None, status_ultimo_dia_anterior: str = None) -> Dict[date, str]:
        escala = {}
        data_atual = data_inicio
        while data_atual <= data_fim:
            if data_atual.day % 2 == 0:
                escala[data_atual] = "TRABALHO_DIA"
            else:
                escala[data_atual] = "FOLGA"
            data_atual += timedelta(days=1)
        return escala

    def _regra_plantao_par_noite(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_plantao_mes_anterior: date = None, status_ultimo_dia_anterior: str = None) -> Dict[date, str]:
        escala = {}
        data_atual = data_inicio
        while data_atual <= data_fim:
            if data_atual.day % 2 == 0:
                escala[data_atual] = "TRABALHO_NOITE"
            else:
                escala[data_atual] = "FOLGA"
            data_atual += timedelta(days=1)
        return escala

    def _regra_plantao_impar_dia(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_plantao_mes_anterior: date = None, status_ultimo_dia_anterior: str = None) -> Dict[date, str]:
        escala = {}
        data_atual = data_inicio
        while data_atual <= data_fim:
            if data_atual.day % 2 == 1:
                escala[data_atual] = "TRABALHO_DIA"
            else:
                escala[data_atual] = "FOLGA"
            data_atual += timedelta(days=1)
        return escala

    def _regra_plantao_impar_noite(self, data_inicio: date, data_fim: date, feriados: List[date], ultimo_plantao_mes_anterior: date = None, status_ultimo_dia_anterior: str = None) -> Dict[date, str]:
        escala = {}
        data_atual = data_inicio
        while data_atual <= data_fim:
            if data_atual.day % 2 == 1:
                escala[data_atual] = "TRABALHO_NOITE"
            else:
                escala[data_atual] = "FOLGA"
            data_atual += timedelta(days=1)
        return escala
    
    def determinar_tipo_plantao_automatico(self, ultimo_plantao_mes_anterior: date, tipo_anterior: str) -> str:
        """
        Determina automaticamente o tipo de plantão baseado no último plantão do mês anterior e tipo anterior.
        
        REGRA CORRETA: A escala só muda quando o mês de referência (último mês trabalhado) tem 31 dias.
        Se o mês de referência tem 31 dias, inverte a paridade (P_ ↔ I_), mantendo o turno (_D ou _N).
        Se o mês de referência tem 30, 28 ou 29 dias, mantém o mesmo tipo.
        
        Args:
            ultimo_plantao_mes_anterior: Data do último plantão do mês anterior
            tipo_anterior: Tipo anterior completo (ex: 'P_D', 'I_N')
            
        Returns:
            String com o tipo de plantão (P_D, P_N, I_D, I_N)
        """
        if not ultimo_plantao_mes_anterior or not tipo_anterior:
            # Se não há informação, assume plantão par dia
            return "P_D"
        
        # Determinar o mês de referência (mês do último plantão)
        mes_referencia = ultimo_plantao_mes_anterior.replace(day=1)
        ultimo_dia_mes_referencia = (mes_referencia + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        dias_mes_referencia = ultimo_dia_mes_referencia.day
        
        paridade, turno = tipo_anterior.split('_')
        
        # CORREÇÃO: Verificar se o mês de referência tem 31 dias
        if dias_mes_referencia == 31:
            # Inverter paridade
            nova_paridade = 'I' if paridade == 'P' else 'P'
            return f"{nova_paridade}_{turno}"
        else:
            # Mantém o mesmo tipo
            return tipo_anterior
    
    def aplicar_excecoes(self, escala_base: Dict[date, str], 
                        atestados: str, ferias: str, escalas_manuais: str) -> Dict[date, str]:
        """
        Aplica as exceções (atestados, férias, escalas manuais) sobre a escala base.
        
        Args:
            escala_base: Escala base gerada pelas regras
            atestados: String com datas de atestados (separadas por vírgula)
            ferias: String com período de férias (formato: DD/MM/YYYY-DD/MM/YYYY)
            escalas_manuais: String com datas de escalas manuais (separadas por vírgula)
            
        Returns:
            Dict com escala final após aplicação das exceções
        """
        escala_final = escala_base.copy()
        
        # Aplicar atestados
        if atestados and atestados.strip():
            datas_atestados = self._parse_datas(atestados)
            for data_atestado in datas_atestados:
                if data_atestado in escala_final:
                    escala_final[data_atestado] = "ATESTADO"
        
        # Aplicar férias
        if ferias and ferias.strip():
            periodo_ferias = self._parse_periodo_ferias(ferias)
            for data_ferias in periodo_ferias:
                if data_ferias in escala_final:
                    escala_final[data_ferias] = "FÉRIAS"
        
        # Aplicar escalas manuais
        if escalas_manuais and escalas_manuais.strip():
            datas_manuais = self._parse_datas(escalas_manuais)
            for data_manual in datas_manuais:
                if data_manual in escala_final:
                    escala_final[data_manual] = "ESCALA MANUAL"
        
        return escala_final
    
    def _parse_datas(self, datas_str: str) -> List[date]:
        """
        Converte string de datas em lista de objetos date.
        
        Args:
            datas_str: String com datas separadas por vírgula (formato: DD/MM/YYYY)
            
        Returns:
            Lista de objetos date
        """
        datas = []
        if not datas_str.strip():
            return datas
        
        for data_str in datas_str.split(','):
            data_str = data_str.strip()
            if data_str:
                try:
                    # Tentar diferentes formatos
                    for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                        try:
                            data = datetime.strptime(data_str, formato).date()
                            datas.append(data)
                            break
                        except ValueError:
                            continue
                except:
                    continue
        
        return datas
    
    def _parse_periodo_ferias(self, periodo_str: str) -> List[date]:
        """
        Converte string de período de férias em lista de datas.
        
        Args:
            periodo_str: String com período (formato: DD/MM/YYYY-DD/MM/YYYY)
            
        Returns:
            Lista de objetos date do período
        """
        datas = []
        if not periodo_str.strip():
            return datas
        
        try:
            # Separar início e fim
            if '-' in periodo_str:
                inicio_str, fim_str = periodo_str.split('-', 1)
                inicio_str = inicio_str.strip()
                fim_str = fim_str.strip()
                
                # Converter datas
                data_inicio = None
                data_fim = None
                
                for formato in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                    try:
                        data_inicio = datetime.strptime(inicio_str, formato).date()
                        data_fim = datetime.strptime(fim_str, formato).date()
                        break
                    except ValueError:
                        continue
                
                if data_inicio and data_fim:
                    # Gerar todas as datas do período
                    data_atual = data_inicio
                    while data_atual <= data_fim:
                        datas.append(data_atual)
                        data_atual += timedelta(days=1)
        
        except:
            pass
        
        return datas
    
    def validar_escala(self, escala: Dict[date, str], tipo_escala: str) -> Dict[str, Any]:
        """
        Valida se a escala gerada está em conformidade com a CLT.
        
        Args:
            escala: Dicionário com a escala gerada
            tipo_escala: Tipo de escala aplicada
            
        Returns:
            Dict com resultados da validação
        """
        resultados = {
            'valida': True,
            'erros': [],
            'avisos': [],
            'estatisticas': {}
        }
        
        # Contar tipos de dias
        contadores = {}
        for status in escala.values():
            contadores[status] = contadores.get(status, 0) + 1
        
        resultados['estatisticas'] = contadores
        
        # Validações específicas por tipo de escala
        if tipo_escala == '44H':
            # Verificar se não trabalha aos fins de semana
            for data, status in escala.items():
                if data.weekday() >= 5 and status == 'TRABALHO':
                    resultados['erros'].append(f"Escala 44H não pode trabalhar em {data.strftime('%d/%m/%Y')} (fim de semana)")
                    resultados['valida'] = False
        
        elif tipo_escala == '12X36':
            # Verificar proporção trabalho/folga
            if 'TRABALHO' in contadores and 'FOLGA' in contadores:
                proporcao = contadores['TRABALHO'] / contadores['FOLGA']
                if proporcao < 0.2 or proporcao > 0.4:  # Esperado ~0.25 (12/48)
                    resultados['avisos'].append(f"Proporção trabalho/folga pode estar incorreta: {proporcao:.2f}")
        
        elif tipo_escala == '6X1':
            # Verificar se há pelo menos um domingo livre a cada 7 semanas
            domingos_trabalho = 0
            domingos_folga = 0
            for data, status in escala.items():
                if data.weekday() == 6:  # Domingo
                    if status == 'TRABALHO':
                        domingos_trabalho += 1
                    else:
                        domingos_folga += 1
            
            if domingos_trabalho > domingos_folga:
                resultados['avisos'].append("Muitos domingos de trabalho na escala 6X1")
        
        return resultados 