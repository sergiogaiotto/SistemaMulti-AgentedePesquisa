import requests
from typing import List, Dict, Optional
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from config import Config
import json

class WebSearchTool:
    """Ferramenta de pesquisa web com fallback para múltiplas APIs"""
    
    def __init__(self):
        self.tavily_search = None
        if Config.TAVILY_API_KEY:
            self.tavily_search = TavilySearchResults(
                max_results=Config.MAX_SEARCH_RESULTS,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True
            )
    
    def search_web(self, query: str, num_results: int = None) -> List[Dict]:
        """Executa pesquisa web com fallback para múltiplas fontes"""
        if num_results is None:
            num_results = Config.MAX_SEARCH_RESULTS
            
        try:
            # Tenta usar Tavily primeiro (melhor qualidade)
            if self.tavily_search:
                results = self.tavily_search.run(query)
                return self._format_tavily_results(results)
            else:
                # Fallback para DuckDuckGo (gratuito)
                return self._search_duckduckgo(query, num_results)
                
        except Exception as e:
            print(f"Erro na pesquisa web: {e}")
            return self._search_duckduckgo(query, num_results)
    
    def _format_tavily_results(self, results: List[Dict]) -> List[Dict]:
        """Formata resultados do Tavily"""
        formatted = []
        for result in results:
            formatted.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0.0)
            })
        return formatted
    
    def _search_duckduckgo(self, query: str, num_results: int) -> List[Dict]:
        """Pesquisa usando DuckDuckGo (fallback gratuito)"""
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            search = DuckDuckGoSearchRun()
            result = search.run(query)
            
            # Parse do resultado do DuckDuckGo
            results = []
            if result:
                # Simula múltiplos resultados a partir do texto
                content_chunks = result.split('\n\n')[:num_results]
                for i, chunk in enumerate(content_chunks):
                    if chunk.strip():
                        results.append({
                            "title": f"Result {i+1}",
                            "url": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
                            "content": chunk.strip(),
                            "score": 1.0 - (i * 0.1)
                        })
            
            return results
            
        except Exception as e:
            print(f"Erro no DuckDuckGo: {e}")
            return [{"title": "Erro", "url": "", "content": f"Não foi possível pesquisar: {query}", "score": 0.0}]

# Instância global da ferramenta
web_search_tool = WebSearchTool()

@tool
def search_web(query: str, num_results: int = 5) -> List[Dict]:
    """
    Ferramenta para pesquisar informações na web.
    
    Args:
        query: Termo de pesquisa
        num_results: Número máximo de resultados (padrão: 5)
    
    Returns:
        Lista de dicionários com title, url, content e score
    """
    return web_search_tool.search_web(query, num_results)

@tool 
def search_companies(query: str, industry: str = "", year: str = "2025") -> List[Dict]:
    """
    Ferramenta especializada para pesquisar empresas.
    
    Args:
        query: Termo de pesquisa sobre empresas
        industry: Setor/indústria específica
        year: Ano de referência
        
    Returns:
        Lista de empresas encontradas
    """
    # Constrói query otimizada para empresas
    search_query = f"{query} companies {industry} {year} list"
    if "AI" in query or "artificial intelligence" in query.lower():
        search_query += " artificial intelligence startups"
    
    results = web_search_tool.search_web(search_query, Config.MAX_SEARCH_RESULTS)
    
    # Filtra e processa resultados para empresas
    company_results = []
    for result in results:
        content = result.get("content", "")
        if any(keyword in content.lower() for keyword in ["company", "startup", "corporation", "inc", "ltd", "llc"]):
            company_results.append(result)
    
    return company_results[:10]  # Limita a 10 empresas por pesquisa