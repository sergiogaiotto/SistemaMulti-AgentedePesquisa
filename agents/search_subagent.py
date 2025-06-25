from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from config import Config
from tools.web_search import search_web, search_companies
from memory.research_memory import research_memory

class SearchSubagent:
    """Subagente especializado em pesquisas específicas"""
    
    def __init__(self, agent_id: str, task: str, focus: str):
        self.agent_id = agent_id
        self.task = task
        self.focus = focus
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
        self.search_iterations = 0
        self.max_iterations = 3
        
    def execute_search(self) -> Dict[str, Any]:
        """Executa a pesquisa especializada"""
        
        print(f"🔍 {self.agent_id} iniciando pesquisa: {self.task}")
        
        # 1. Planeja estratégia de pesquisa
        search_strategy = self._plan_search_strategy()
        
        # 2. Executa pesquisas iterativas
        all_results = []
        for query in search_strategy["queries"]:
            print(f"   🔎 Pesquisando: {query}")
            results = self._perform_search(query)
            all_results.extend(results)
            
            # Avalia se precisa continuar
            if self._evaluate_results(all_results):
                break
        
        # 3. Processa e filtra resultados
        processed_results = self._process_results(all_results)
        
        # 4. Gera resumo
        summary = self._generate_summary(processed_results)
        
        result = {
            "agent_id": self.agent_id,
            "task": self.task,
            "focus": self.focus,
            "search_strategy": search_strategy,
            "raw_results": all_results,
            "processed_results": processed_results,
            "summary": summary,
            "sources": processed_results,
            "status": "completed"
        }
        
        print(f"✅ {self.agent_id} concluído: {len(processed_results)} resultados")
        return result
    
    def _plan_search_strategy(self) -> Dict[str, Any]:
        """Planeja estratégia de pesquisa baseada na tarefa"""
        
        system_prompt = """Você é um especialista em estratégias de pesquisa web.
        
        Sua tarefa é criar uma estratégia de pesquisa otimizada para encontrar informações específicas.
        
        Dado uma tarefa e foco, crie 2-3 queries de pesquisa diferentes que abordem:
        1. Termos gerais amplos
        2. Termos específicos e técnicos
        3. Termos alternativos ou relacionados
        
        Responda em formato JSON:
        {
            "queries": ["query 1", "query 2", "query 3"],
            "strategy": "descrição da estratégia",
            "expected_sources": ["tipo de fonte 1", "tipo de fonte 2"]
        }
        """
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Tarefa: {self.task}\nFoco: {self.focus}")
            ]
            
            response = self.llm.invoke(messages)
            
            import json
            try:
                strategy = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback
                strategy = {
                    "queries": [self.task, f"{self.focus} {self.task}", f"{self.task} 2025"],
                    "strategy": "Pesquisa iterativa com termos variados",
                    "expected_sources": ["websites", "articles", "directories"]
                }
            
            return strategy
            
        except Exception as e:
            print(f"Erro no planejamento de pesquisa: {e}")
            return {
                "queries": [self.task],
                "strategy": "Pesquisa simples",
                "expected_sources": ["web"]
            }
    
    def _perform_search(self, query: str) -> List[Dict]:
        """Executa uma pesquisa específica"""
        
        try:
            # Escolhe ferramenta de pesquisa baseada no foco
            if "company" in self.focus.lower() or "companies" in query.lower():
                results = search_companies(query)
            else:
                results = search_web(query, num_results=Config.MAX_SEARCH_RESULTS)
            
            return results
            
        except Exception as e:
            print(f"Erro na pesquisa '{query}': {e}")
            return []
    
    def _evaluate_results(self, results: List[Dict]) -> bool:
        """Avalia se os resultados são suficientes"""
        
        if not results:
            return False
        
        # Verifica qualidade dos resultados
        quality_score = 0
        for result in results:
            content = result.get("content", "")
            if len(content) > 100:  # Conteúdo substancial
                quality_score += 1
            if result.get("score", 0) > 0.7:  # Alta relevância
                quality_score += 1
        
        # Para se tem resultados de qualidade suficiente
        return quality_score >= 5 or len(results) >= 10
    
    def _process_results(self, raw_results: List[Dict]) -> List[Dict]:
        """Processa e filtra resultados para melhor qualidade"""
        
        processed = []
        seen_urls = set()
        
        for result in raw_results:
            url = result.get("url", "")
            content = result.get("content", "")
            
            # Remove duplicatas
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # Filtra resultados com pouco conteúdo
            if len(content) < 50:
                continue
            
            # Adiciona metadados do processamento
            processed_result = {
                **result,
                "processed_by": self.agent_id,
                "relevance_score": self._calculate_relevance(result),
                "content_length": len(content)
            }
            
            processed.append(processed_result)
        
        # Ordena por relevância
        processed.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        # Retorna top 10 resultados
        return processed[:10]
    
    def _calculate_relevance(self, result: Dict) -> float:
        """Calcula score de relevância para um resultado"""
        
        content = result.get("content", "").lower()
        title = result.get("title", "").lower()
        
        # Palavras-chave da tarefa
        task_words = set(self.task.lower().split())
        focus_words = set(self.focus.lower().split())
        
        # Conta ocorrências
        content_words = set(content.split())
        title_words = set(title.split())
        
        task_matches = len(task_words.intersection(content_words.union(title_words)))
        focus_matches = len(focus_words.intersection(content_words.union(title_words)))
        
        # Score base do resultado
        base_score = result.get("score", 0.5)
        
        # Score combinado
        relevance = (task_matches * 0.4 + focus_matches * 0.3 + base_score * 0.3)
        
        return min(relevance, 1.0)
    
    def _generate_summary(self, results: List[Dict]) -> str:
        """Gera resumo dos resultados encontrados"""
        
        if not results:
            return f"Nenhum resultado encontrado para: {self.task}"
        
        # Prepara contexto para resumo
        context = f"Tarefa: {self.task}\nFoco: {self.focus}\n\nResultados encontrados:\n"
        
        for i, result in enumerate(results[:5], 1):  # Top 5 para resumo
            title = result.get("title", "Sem título")
            content = result.get("content", "")[:200] + "..."
            context += f"\n{i}. {title}\n   {content}\n"
        
        system_prompt = """Você é um especialista em análise de resultados de pesquisa.
        
        Sua tarefa é criar um resumo conciso dos resultados encontrados, destacando:
        1. Principais descobertas
        2. Informações mais relevantes
        3. Padrões ou tendências identificados
        4. Lacunas que podem precisar de mais pesquisa
        
        Mantenha o resumo focado e objetivo, com no máximo 300 palavras.
        """
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=context)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Erro na geração de resumo: {e}")
            return f"Encontrados {len(results)} resultados para: {self.task}"

# Factory function para criar subagentes
def create_subagent(agent_id: str, task: str, focus: str) -> SearchSubagent:
    """Cria uma nova instância de SearchSubagent"""
    return SearchSubagent(agent_id, task, focus)

@tool
def run_subagent(agent_id: str, task: str, focus: str = "general") -> Dict:
    """
    Executa um subagente de pesquisa.
    
    Args:
        agent_id: ID único do agente
        task: Tarefa específica de pesquisa
        focus: Foco ou especialização da pesquisa
        
    Returns:
        Resultado completo da pesquisa do subagente
    """
    subagent = create_subagent(agent_id, task, focus)
    result = subagent.execute_search()
    
    # Salva resultado na memória
    research_memory.add_subagent_result(agent_id, result)
    research_memory.add_sources(result.get("sources", []))
    
    return result

@tool
def create_specialized_subagent(task: str, focus: str, search_terms: List[str]) -> Dict:
    """
    Cria e executa subagente com termos de pesquisa específicos.
    
    Args:
        task: Tarefa do subagente
        focus: Área de foco
        search_terms: Lista de termos específicos para pesquisar
        
    Returns:
        Resultado da pesquisa especializada
    """
    agent_id = f"specialized_{hash(task) % 1000}"
    subagent = create_subagent(agent_id, task, focus)
    
    # Override da estratégia com termos específicos
    subagent._plan_search_strategy = lambda: {
        "queries": search_terms,
        "strategy": "Pesquisa com termos específicos fornecidos",
        "expected_sources": ["specialized sources"]
    }
    
    return subagent.execute_search()