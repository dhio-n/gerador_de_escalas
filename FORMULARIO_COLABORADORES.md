# Formulário de Colaboradores - Interface Guiada

## 📋 Visão Geral

O **Formulário de Colaboradores** é uma nova funcionalidade do Sistema de Escalas que facilita o preenchimento da planilha de colaboradores através de uma interface visual e guiada, eliminando a necessidade de conhecimento técnico para editar planilhas manualmente.

## 🎯 Objetivos

- **Facilitar o preenchimento** da planilha de colaboradores para usuários iniciantes
- **Reduzir erros** através de validações em tempo real
- **Interface guiada** passo a passo com campos intuitivos
- **Integração completa** com o gerador de escalas existente

## 🚀 Como Usar

### 1. Acessando o Formulário

1. Abra o aplicativo Streamlit (`app2.py`)
2. Clique na aba **"👥 Formulário de Colaboradores"**
3. O formulário está organizado em 3 abas internas:
   - **➕ Adicionar Colaborador**
   - **📋 Lista de Colaboradores**
   - **📥 Exportar**

### 2. Adicionando Colaboradores

#### Campos Obrigatórios:
- **Nome Completo**: Nome completo do colaborador
- **Cargo/Função**: Cargo ou função do colaborador
- **Tipo de Escala**: Dropdown com todos os tipos disponíveis
- **Turno**: Dropdown com opções (Manhã, Tarde, Noite, Dia)

#### Campos Opcionais:
- **Atestados**: Seletor múltiplo de datas
- **Período de Férias**: Data de início e fim
- **Escalas Manuais**: Datas específicas para forçar escala
- **Último Plantão**: Para plantonistas
- **Último Domingo de Folga**: Para escalas 6x1

### 3. Funcionalidades Especiais

#### 🔄 Duplicar Último Colaborador
- Botão para copiar dados do último colaborador adicionado
- Facilita o preenchimento de times com jornadas semelhantes

#### 📋 Preview da Escala
- Visualização rápida dos colaboradores adicionados
- Estatísticas em tempo real

#### 📊 Estatísticas Detalhadas
- Gráficos de distribuição por tipo de escala e turno
- Resumo estatístico completo

### 4. Exportação

#### 📥 Exportar para Excel
- Gera automaticamente a planilha no formato correto
- Ajusta automaticamente a largura das colunas
- Nome do arquivo inclui timestamp

## 🔗 Integração com o Gerador de Escalas

### Usando Colaboradores do Formulário no Gerador:

1. **Adicione colaboradores** no formulário
2. **Clique em "📋 Usar Colaboradores no Gerador"**
3. **Vá para a aba "🚀 Gerador de Escalas"**
4. **Clique em "📋 Usar Colaboradores do Formulário"**
5. **Faça upload da planilha de feriados**
6. **Gere a escala normalmente**

### Vantagens da Integração:

- ✅ **Sem necessidade de salvar arquivos** intermediários
- ✅ **Validação em tempo real** dos dados
- ✅ **Interface mais amigável** para usuários iniciantes
- ✅ **Mantém compatibilidade** com upload de arquivos

## 📋 Tipos de Escala Suportados

### Escalas 44H:
- **M44**: 44H - Manhã (Segunda a sexta, 8h/dia)
- **T44**: 44H - Tarde (Segunda a sexta, 8h/dia)
- **N44**: 44H - Noite (Segunda a sexta, 8h/dia)

### Escalas 40H:
- **M40**: 40H - Manhã (Segunda a sexta, 8h/dia)
- **T40**: 40H - Tarde (Segunda a sexta, 8h/dia)
- **N40**: 40H - Noite (Segunda a sexta, 8h/dia)

### Escalas 6X1:
- **M6X1**: 6x1 - Manhã (6 dias trabalho, 1 dia folga)
- **T6X1**: 6x1 - Tarde (6 dias trabalho, 1 dia folga)
- **N6X1**: 6x1 - Noite (6 dias trabalho, 1 dia folga)

### Plantões:
- **P_D**: Plantão Par - Dia (dias pares do mês)
- **P_N**: Plantão Par - Noite (dias pares do mês)
- **I_D**: Plantão Ímpar - Dia (dias ímpares do mês)
- **I_N**: Plantão Ímpar - Noite (dias ímpares do mês)

## ✅ Validações Implementadas

### Campos Obrigatórios:
- Nome não pode estar vazio
- Cargo não pode estar vazio

### Regras de Negócio:
- Data de início das férias deve ser anterior à data de fim
- Data de início das férias não pode ser no passado
- Nomes duplicados não são permitidos

### Validações Específicas:
- **Plantonistas**: Sugestão de informar último plantão
- **Escalas 6x1**: Sugestão de informar último domingo de folga

## 🎨 Interface e UX

### Design Responsivo:
- Layout adaptável para diferentes tamanhos de tela
- Colunas organizadas logicamente
- Cores e ícones intuitivos

### Feedback Visual:
- ✅ Mensagens de sucesso
- ❌ Mensagens de erro
- ⚠️ Avisos e dicas
- 📊 Estatísticas em tempo real

### Navegação Intuitiva:
- Abas organizadas por funcionalidade
- Botões com ícones descritivos
- Help text em todos os campos

## 🔧 Arquivos do Sistema

### `colaborador_form.py`
- Classe principal `FormularioColaboradores`
- Lógica de validação e formatação
- Geração de Excel
- Gerenciamento de session state

### `app2.py`
- Integração com o gerador de escalas
- Abas do Streamlit
- Fluxo de dados entre formulário e gerador

## 🚀 Próximas Melhorias

### Funcionalidades Planejadas:
- [ ] **Importação de planilhas** para o formulário
- [ ] **Edição de colaboradores** existentes
- [ ] **Templates pré-definidos** para tipos de empresa
- [ ] **Validação avançada** de regras CLT
- [ ] **Backup automático** dos dados
- [ ] **Histórico de alterações**

### Melhorias de UX:
- [ ] **Drag & drop** para reordenar colaboradores
- [ ] **Busca e filtros** na lista
- [ ] **Atalhos de teclado**
- [ ] **Modo escuro**
- [ ] **Responsividade mobile**

## 📞 Suporte

Para dúvidas ou sugestões sobre o Formulário de Colaboradores:

1. **Verifique esta documentação**
2. **Teste com dados de exemplo**
3. **Reporte bugs** com detalhes do erro
4. **Sugira melhorias** através do sistema de issues

---

**Desenvolvido para otimizar processos de RH e garantir conformidade legal com a CLT brasileira.** 