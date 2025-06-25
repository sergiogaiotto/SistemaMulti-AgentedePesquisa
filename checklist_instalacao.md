# ✅ Checklist de Instalação - Sistema Multi-Agente

Use esta checklist para garantir que tudo está funcionando corretamente.

## 📋 Pré-Instalação

- [ ] **Python 3.8+** instalado
  - [ ] Execute: `python --version`
  - [ ] Deve mostrar versão 3.8 ou superior
  
- [ ] **Pip** funcionando
  - [ ] Execute: `pip --version`
  - [ ] Deve mostrar versão do pip

- [ ] **OpenAI API Key** disponível
  - [ ] Acesse: https://platform.openai.com/api-keys
  - [ ] Crie uma nova chave se necessário
  - [ ] Copie a chave (sk-...)

## 📁 Estrutura de Arquivos

Verifique se todos estes arquivos estão presentes:

### ✅ Arquivos Principais
- [ ] `main.py`
- [ ] `config.py`
- [ ] `requirements.txt`
- [ ] `.env.example`
- [ ] `README.md`
- [ ] `example_usage.py`
- [ ] `install.bat`

### ✅ Diretório agents/
- [ ] `agents/__init__.py`
- [ ] `agents/lead_researcher.py`
- [ ] `agents/search_subagent.py`
- [ ] `agents/citation_agent.py`

### ✅ Diretório tools/
- [ ] `tools/__init__.py`
- [ ] `tools/web_search.py`
- [ ] `tools/citation_tools.py`

### ✅ Diretório memory/
- [ ] `memory/__init__.py`
- [ ] `memory/research_memory.py`

### ✅ Diretório utils/
- [ ] `utils/__init__.py`
- [ ] `utils/helpers.py`

### ✅ Diretório graph/
- [ ] `graph/__init__.py`
- [ ] `graph/research_workflow.py`

## 🔧 Instalação

### 1. Dependências
- [ ] Execute: `pip install -r requirements.txt`
- [ ] Sem erros de instalação
- [ ] Todas as bibliotecas instaladas

### 2. Configuração
- [ ] Copie `.env.example` para `.env`
- [ ] Edite `.env` com sua OPENAI_API_KEY
- [ ] Arquivo `.env` existe e contém a chave

### 3. Teste de Importação
Execute cada comando e verifique que não há erros:

- [ ] `python -c "import langchain"`
- [ ] `python -c "import langgraph"`
- [ ] `python -c "import langchain_openai"`
- [ ] `python -c "from config import Config"`
- [ ] `python -c "from graph.research_workflow import research_workflow"`

## 🧪 Testes de Funcionalidade

### 1. Teste de Configuração
```bash
python -c "from config import Config; Config.validate()"
```
- [ ] Executa sem erro
- [ ] Mostra "✅ Configurações validadas com sucesso!"

### 2. Teste OpenAI
```bash
python -c "
from langchain_openai import ChatOpenAI
from config import Config
llm = ChatOpenAI(api_key=Config.OPENAI_API_KEY)
print('OpenAI funcionando!')
"
```
- [ ] Executa sem erro
- [ ] Mostra "OpenAI funcionando!"

### 3. Teste do Sistema Principal
```bash
python main.py
```
- [ ] Sistema inicia sem erros
- [ ] Menu principal aparece
- [ ] Opção 3 (Testar Configurações) funciona

### 4. Teste de Pesquisa Simples
```bash
python -c "
from graph.research_workflow import research_workflow
result = research_workflow.run_research('test query')
print('Teste concluído:', result.get('success'))
"
```
- [ ] Executa sem erro crítico
- [ ] Retorna resultado (mesmo que simples)

## 🚀 Teste Funcional Completo

### Pesquisa de Demonstração
1. [ ] Execute: `python main.py`
2. [ ] Escolha opção 1: "Modo Interativo"
3. [ ] Digite: `"Top 3 AI companies"`
4. [ ] Aguarde execução (1-3 minutos)
5. [ ] Recebe relatório formatado
6. [ ] Relatório contém informações relevantes
7. [ ] Citações estão presentes

## 🔍 Verificação de Qualidade

### Output Esperado
O sistema deve produzir:
- [ ] **Planejamento**: Análise da query
- [ ] **Execução**: Múltiplos subagentes trabalhando
- [ ] **Progresso**: Indicadores de andamento
- [ ] **Síntese**: Combinação de resultados
- [ ] **Citações**: Referências automáticas
- [ ] **Relatório**: Documento final formatado

### Indicadores de Sucesso
- [ ] Tempo de execução: 1-5 minutos
- [ ] Múltiplas fontes encontradas (5+)
- [ ] Relatório coerente e bem estruturado
- [ ] Citações numeradas corretamente
- [ ] Bibliografia no final

## 🐛 Resolução de Problemas

### Se algo falhou:

#### ❌ Erro de importação
1. [ ] Verifique instalação: `pip list | grep -E "(langchain|langgraph)"`
2. [ ] Reinstale: `pip install --upgrade -r requirements.txt`
3. [ ] Teste novamente

#### ❌ Erro de configuração
1. [ ] Verifique arquivo `.env`
2. [ ] Confirme OPENAI_API_KEY válida
3. [ ] Teste com: `python -c "from config import Config; Config.validate()"`

#### ❌ Pesquisa falha
1. [ ] Verifique conexão internet
2. [ ] Teste query mais simples
3. [ ] Configure Tavily API se disponível

#### ❌ Erro de encoding (Windows)
1. [ ] Execute: `chcp 65001`
2. [ ] Use PowerShell em vez de CMD
3. [ ] Ou execute via IDE (VSCode, PyCharm)

## ✅ Checklist Final

Se todos os itens estão marcados:

- [ ] ✅ Instalação completa
- [ ] ✅ Configuração válida  
- [ ] ✅ Testes básicos passaram
- [ ] ✅ Pesquisa funcional executou
- [ ] ✅ Resultados de qualidade

**🎉 Sistema pronto para uso!**

## 📞 Suporte

Se algum item falhou:

1. **Revise esta checklist** do início
2. **Execute**: `python main.py` → Opção 3
3. **Verifique logs** de erro para detalhes
4. **Teste configuração** passo a passo

---

**💡 Dica**: Mantenha esta checklist para futuras instalações ou troubleshooting!