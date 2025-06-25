# ⚡ Guia de Início Rápido

## 🚀 Setup em 3 Minutos

### 1. Pré-requisitos
```bash
# Verifique se tem Python 3.8+
python --version
```

### 2. Instalação Automática (Windows)
```bash
# Execute o instalador automático
install.bat
```

### 3. Configuração Manual (se preferir)
```bash
# Instale dependências
pip install -r requirements.txt

# Configure ambiente
copy .env.example .env
notepad .env  # Adicione sua OPENAI_API_KEY
```

### 4. Teste Rápido
```bash
python main.py
# Escolha opção 3: Testar Configurações
```

## 🎯 Primeiro Uso

### Interface Interativa
```bash
python main.py
# Escolha opção 1: Modo Interativo

# Digite algo como:
"List top 5 AI startups in 2025 with funding info"
```

### Uso Programático
```python
from graph.research_workflow import research_workflow

result = research_workflow.run_research("your query")
print(result["final_report"])
```

## 📋 Queries de Exemplo

### ✅ Funcionam Bem
- `"Top 10 AI companies in Silicon Valley with their latest products"`
- `"Electric vehicle startups founded in 2024"`
- `"Companies working on quantum computing with their funding status"`
- `"Renewable energy companies and their recent partnerships"`

### ❌ Evite (muito vagas)
- `"AI"`
- `"Companies"`
- `"Technology"`

## 🔧 Configurações Importantes

### .env Básico
```env
OPENAI_API_KEY=sk-sua_chave_aqui
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.1
MAX_SEARCH_RESULTS=10
MAX_SUBAGENTS=3
```

### Para Pesquisas Rápidas
```env
MAX_SEARCH_RESULTS=5
MAX_SUBAGENTS=2
```

### Para Pesquisas Detalhadas
```env
MAX_SEARCH_RESULTS=15
MAX_SUBAGENTS=3
TAVILY_API_KEY=tvly-sua_chave  # Opcional, melhora qualidade
```

## 🏃‍♂️ Execução Rápida

### Demonstração Instantânea
```bash
python main.py
# Opção 2: Modo Demonstração
# Vê 3 exemplos funcionando automaticamente
```

### Teste Específico
```bash
python example_usage.py
# Executa 5 exemplos diferentes programaticamente
```

## 🐛 Resolução Rápida de Problemas

### Erro: "OPENAI_API_KEY é obrigatório"
1. Abra o arquivo `.env`
2. Adicione: `OPENAI_API_KEY=sk-sua_chave_real`
3. Salve e teste novamente

### Erro: "No module named..."
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Pesquisas muito lentas
1. Reduza `MAX_SEARCH_RESULTS=5`
2. Configure Tavily API para melhor qualidade
3. Use queries mais específicas

### Encoding no Windows
```bash
# Execute no prompt com UTF-8
chcp 65001
python main.py
```

## 🎪 Recursos Avançados

### Salvar Relatórios
- Sistema pergunta automaticamente se quer salvar
- Ou use: `save_research_to_file(result)`

### Múltiplas Pesquisas
```python
queries = ["query1", "query2", "query3"]
for query in queries:
    result = research_workflow.run_research(query)
    # processa resultado...
```

### Configurações Dinâmicas
```python
from config import Config
Config.MAX_SUBAGENTS = 2  # Temporariamente
# ... executa pesquisa
Config.MAX_SUBAGENTS = 3  # Restaura
```

## 📊 O que Esperar

### Pesquisa Típica (3-5 minutos)
```
🎯 Planejando pesquisa...        [5s]
🤖 Executando subagentes...      [120s]
🔍 Avaliando progresso...        [10s]
🧠 Sintetizando resultados...    [30s]
📚 Adicionando citações...       [15s]
📝 Finalizando relatório...      [5s]
✅ Concluído!
```

### Resultado Final
- Relatório formatado em Markdown
- Citações inline [1], [2], [3]
- Bibliografia completa
- Metadados da pesquisa

## 🎯 Próximos Passos

1. **Experimente**: Use o modo demonstração
2. **Customize**: Ajuste configurações no `.env`
3. **Integre**: Use programaticamente em seus projetos
4. **Expanda**: Adicione novos agentes ou ferramentas

---

**💡 Dica**: Para melhor experiência, configure a Tavily API key - melhora significativamente a qualidade dos resultados!

🆘 **Problemas?** Execute `python main.py` → Opção 3: Testar Configurações