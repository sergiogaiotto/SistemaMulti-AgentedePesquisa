# 🔬 Sistema Multi-Agente de Pesquisa Avançada

Um sistema de pesquisa inteligente que utiliza **LangGraph** para coordenar múltiplos agentes especializados, implementando uma arquitetura orquestrador-trabalhador para pesquisas complexas e abrangentes.

## 🌟 Características Principais

- **🎯 Lead Researcher**: Agente coordenador que analisa consultas e orquestra todo o processo
- **🔍 Search Subagents**: Agentes especializados que executam pesquisas em paralelo
- **📚 Citation Agent**: Adiciona citações automáticas aos relatórios finais
- **🧠 Memory System**: Mantém contexto e persiste informações durante a pesquisa
- **⚡ Pesquisa Dinâmica**: Adapta estratégias baseando-se nos resultados encontrados
- **📊 Relatórios Detalhados**: Gera relatórios formatados com citações e bibliografia

## 📋 Pré-requisitos

- **Python 3.8+**
- **Windows 10/11** (testado)
- **OpenAI API Key** (obrigatório)
- **Tavily API Key** (opcional, melhora qualidade)

## 🚀 Instalação Rápida

### 1. Clone/Download do projeto

```bash
# Crie o diretório do projeto
mkdir multi_agent_research
cd multi_agent_research
```

### 2. Instale as dependências

```bash
# Instale Python 3.8+ se não tiver
# Baixe de: https://www.python.org/downloads/

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite .env com suas chaves de API
notepad .env
```

**Conteúdo do arquivo .env:**
```env
# OpenAI API Key (obrigatório)
OPENAI_API_KEY=sk-sua_chave_aqui

# Tavily API Key (opcional)
TAVILY_API_KEY=tvly-sua_chave_aqui

# Configurações opcionais
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.1
MAX_SEARCH_RESULTS=10
MAX_SUBAGENTS=3
```

### 4. Execute o sistema

```bash
python main.py
```

## 🎯 Como Usar

### Modo Interativo

```bash
python main.py
# Escolha opção 1 no menu
```

Digite suas pesquisas em linguagem natural:

- `"List the top 10 AI companies in Silicon Valley with their funding information"`
- `"Find startups working on quantum computing in 2025"`
- `"Compare electric vehicle manufacturers and their market share"`

### Modo Programático

```python
from graph.research_workflow import research_workflow

# Executa pesquisa
result = research_workflow.run_research("your query here")

if result["success"]:
    print(result["final_report"])
    print(f"Fontes: {len(result['sources'])}")
else:
    print(f"Erro: {result['error']}")
```

### Exemplos Práticos

```bash
# Execute exemplos pré-configurados
python example_usage.py
```

## 📁 Estrutura do Projeto

```
multi_agent_research/
├── 📄 main.py                    # Ponto de entrada principal
├── 📄 config.py                  # Configurações do sistema
├── 📄 example_usage.py           # Exemplos de uso
├── 📄 requirements.txt           # Dependências Python
├── 📄 .env.example              # Template de configuração
├── 📄 README.md                 # Esta documentação
│
├── 📁 agents/                   # Agentes do sistema
│   ├── lead_researcher.py       # Agente coordenador
│   ├── search_subagent.py       # Agentes de pesquisa
│   └── citation_agent.py        # Processador de citações
│
├── 📁 tools/                    # Ferramentas especializadas
│   ├── web_search.py           # Pesquisa web
│   └── citation_tools.py       # Processamento de citações
│
├── 📁 memory/                   # Sistema de memória
│   └── research_memory.py      # Persistência de contexto
│
├── 📁 utils/                    # Utilitários
│   └── helpers.py              # Funções auxiliares
│
└── 📁 graph/                    # Workflow LangGraph
    └── research_workflow.py    # Orquestração principal
```

## ⚙️ Configuração Avançada

### Chaves de API

#### OpenAI (Obrigatório)
1. Visite: https://platform.openai.com/api-keys
2. Crie uma nova chave
3. Adicione no arquivo `.env`: `OPENAI_API_KEY=sk-...`

#### Tavily (Opcional)
1. Visite: https://tavily.com
2. Registre-se e obtenha API key
3. Adicione no arquivo `.env`: `TAVILY_API_KEY=tvly-...`

**Nota**: Sem Tavily, o sistema usa DuckDuckGo como fallback gratuito.

### Parâmetros de Configuração

```env
# Modelo OpenAI a usar
MODEL_NAME=gpt-4-turbo-preview  # ou gpt-3.5-turbo

# Criatividade das respostas (0.0-1.0)
TEMPERATURE=0.1

# Número máximo de resultados por pesquisa
MAX_SEARCH_RESULTS=10

# Número máximo de subagentes
MAX_SUBAGENTS=3

# Limite de tokens na memória
MEMORY_LIMIT_TOKENS=200000
```

## 🔧 Solução de Problemas

### ❌ Erro: "cannot import name 'EXCLUDED_METADATA_KEYS'"
**Este é o erro mais comum!** Indica incompatibilidade de versões do LangGraph.

**Solução Rápida:**
```bash
# Execute o script de correção
fix_installation.bat

# OU manualmente:
pip uninstall langgraph langchain langchain-openai langchain-community -y
pip install langchain==0.2.16 langchain-openai==0.1.25 langchain-community==0.2.16 langgraph==0.1.19
```

**Teste após correção:**
```bash
python test_system.py
```

### Erro: "OPENAI_API_KEY é obrigatório"
- Verifique se o arquivo `.env` existe
- Confirme se a chave está correta
- Use `python -c "from config import Config; Config.validate()"`

### Erro: "No module named..."
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Pesquisas lentas ou sem resultados
- Configure uma Tavily API key para melhor qualidade
- Verifique sua conexão com internet
- Reduza `MAX_SEARCH_RESULTS` para pesquisas mais rápidas

### Erro de encoding no Windows
```bash
# Execute no prompt de comando com UTF-8
chcp 65001
python main.py
```

### ⚡ Correção Automática Completa
Se nada funcionar, execute em ordem:
```bash
1. fix_installation.bat     # Corrige dependências
2. python test_system.py    # Verifica sistema
3. python main.py          # Executa sistema
```

## 📊 Exemplo de Saída

```
🎯 Planejando pesquisa para: Top 5 AI companies in 2025
✅ Plano criado com 3 tarefas

🤖 Executando subagentes (iteração 1)
   🔍 Executando subagent_1: Research leading AI companies
   🔍 Executando subagent_2: Find company details and metrics
   🔍 Executando subagent_3: Analyze market positions

🔍 Avaliando progresso da pesquisa...
📊 Progresso: 3 resultados, 27 fontes

🧠 Sintetizando resultados da pesquisa...
✅ Síntese concluída

📚 Adicionando citações ao relatório...
✅ Citações adicionadas: 23 fontes

📝 Finalizando relatório...
✅ Relatório finalizado!

==================================================
✅ Pesquisa concluída com sucesso!

⏱️  Relatório de Timing:
----------------------------------------
execução_workflow: 45.2 segundos
fim_workflow: 45.2 segundos
----------------------------------------
Total: 45.2 segundos
```

## 🎮 Modo Demonstração

Execute pesquisas de exemplo para ver o sistema em ação:

```bash
python main.py
# Escolha opção 2: Modo Demonstração
```

## 💡 Dicas de Uso

### Queries Eficazes
- **Específicas**: "AI companies in healthcare with FDA approvals"
- **Estruturadas**: "List companies with: name, website, product, funding"
- **Contextuais**: "Startups founded in 2024 working on climate tech"

### Tipos de Pesquisa Suportados
- 🏢 **Empresas e Startups**: Informações detalhadas de organizações
- 📈 **Análise de Mercado**: Tendências e comparações setoriais  
- 🔬 **Pesquisa Técnica**: Desenvolvimentos em tecnologia
- 📊 **Relatórios Comparativos**: Análises lado a lado

### Otimização de Performance
- Use queries específicas para resultados mais rápidos
- Configure `MAX_SUBAGENTS=2` para pesquisas simples
- Configure `MAX_SUBAGENTS=3` para pesquisas complexas

## 🤝 Contribuindo

Este é um projeto base que pode ser estendido. Sugestões de melhorias:

1. **Novos Agentes**: Agentes especializados em setores específicos
2. **Mais Fontes**: Integração com APIs especializadas
3. **Interface Web**: Frontend React/Streamlit
4. **Cache**: Sistema de cache para pesquisas repetidas
5. **Analytics**: Métricas detalhadas de performance

## 📄 Licença

Este projeto é disponibilizado como código educacional e de demonstração. Use sob sua própria responsabilidade e respeite os termos de serviço das APIs utilizadas.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique a seção "Solução de Problemas"
2. Execute o teste de configuração: opção 3 no menu
3. Verifique os logs de erro para detalhes específicos

---

**🔬 Sistema Multi-Agente de Pesquisa Avançada** - Powered by LangGraph & OpenAI
