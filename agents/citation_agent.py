from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from config import Config
from tools.citation_tools import add_citations_to_report, extract_key_facts, format_company_info

class CitationAgent:
    """Agente especializado em adicionar citações aos relatórios"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=0.1,  # Temperatura baixa para precisão
            api_key=Config.OPENAI_API_KEY
        )
    
    def process_research_report(self, report: str, sources: List[Dict]) -> str:
        """Processa relatório de pesquisa adicionando citações apropriadas"""
        
        print("📚 CitationAgent processando relatório...")
        
        # 1. Identifica locais que precisam de citação
        citation_locations = self._identify_citation_locations(report)
        
        # 2. Mapeia fontes para declarações específicas
        source_mappings = self._map_sources_to_statements(report, sources, citation_locations)
        
        # 3. Adiciona citações inline
        cited_report = self._add_inline_citations(report, source_mappings)
        
        # 4. Gera bibliografia
        bibliography = self._generate_bibliography(sources)
        
        # 5. Combina relatório final
        final_report = f"{cited_report}\n\n{bibliography}"
        
        print(f"✅ CitationAgent concluído: {len(sources)} fontes citadas")
        return final_report
    
    def _identify_citation_locations(self, text: str) -> List[Dict]:
        """Identifica locais no texto que precisam de citação"""
        
        system_prompt = """Você é um especialista em citações acadêmicas e jornalísticas.
        
        Sua tarefa é identificar declarações no texto que precisam de citação para verificação.
        
        Identifique:
        1. Fatos específicos (datas, números, estatísticas)
        2. Declarações sobre empresas (fundação, localização, produtos)
        3. Citações diretas ou indiretas
        4. Informações que não são conhecimento geral
        
        Para cada declaração, forneça:
        - Texto exato da declaração
        - Tipo de informação (fact, company_info, quote, statistic)
        - Nível de prioridade (high, medium, low)
        
        Responda em formato JSON:
        {
            "citation_needs": [
                {
                    "text": "declaração exata",
                    "type": "fact|company_info|quote|statistic",
                    "priority": "high|medium|low",
                    "context": "contexto adicional"
                }
            ]
        }
        """
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Texto para análise:\n\n{text}")
            ]
            
            response = self.llm.invoke(messages)
            
            import json
            try:
                result = json.loads(response.content)
                return result.get("citation_needs", [])
            except json.JSONDecodeError:
                # Fallback: identifica declarações básicas
                return self._basic_citation_identification(text)
                
        except Exception as e:
            print(f"Erro na identificação de citações: {e}")
            return self._basic_citation_identification(text)
    
    def _basic_citation_identification(self, text: str) -> List[Dict]:
        """Identificação básica de locais para citação (fallback)"""
        
        import re
        citation_needs = []
        
        # Padrões que geralmente precisam de citação
        patterns = [
            (r'founded in \d{4}', 'company_info', 'high'),
            (r'\$[\d,]+(?:\.\d{2})? (?:million|billion)', 'statistic', 'high'),
            (r'\d+[\+]? employees', 'company_info', 'medium'),
            (r'headquarters in [A-Z][a-z]+(?:, [A-Z][a-z]+)?', 'company_info', 'medium'),
            (r'according to [^.]+', 'quote', 'high'),
            (r'research shows [^.]+', 'fact', 'high'),
        ]
        
        for pattern, type_info, priority in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                citation_needs.append({
                    "text": match.group(),
                    "type": type_info,
                    "priority": priority,
                    "context": "auto-detected"
                })
        
        return citation_needs
    
    def _map_sources_to_statements(self, text: str, sources: List[Dict], citation_locations: List[Dict]) -> Dict[str, int]:
        """Mapeia cada declaração para a melhor fonte disponível"""
        
        source_mappings = {}
        
        for location in citation_locations:
            statement = location["text"]
            best_source_idx = self._find_best_source_for_statement(statement, sources)
            
            if best_source_idx is not None:
                source_mappings[statement] = best_source_idx + 1  # Citations são 1-indexed
        
        return source_mappings
    
    def _find_best_source_for_statement(self, statement: str, sources: List[Dict]) -> int:
        """Encontra a melhor fonte para uma declaração específica"""
        
        best_score = 0
        best_idx = None
        
        statement_words = set(statement.lower().split())
        
        for i, source in enumerate(sources):
            score = self._calculate_source_relevance(statement_words, source)
            
            if score > best_score:
                best_score = score
                best_idx = i
        
        # Só retorna se a relevância for significativa
        return best_idx if best_score > 0.3 else None
    
    def _calculate_source_relevance(self, statement_words: set, source: Dict) -> float:
        """Calcula relevância entre declaração e fonte"""
        
        source_content = source.get("content", "").lower()
        source_title = source.get("title", "").lower()
        
        source_words = set((source_content + " " + source_title).split())
        
        # Conta palavras em comum
        common_words = statement_words.intersection(source_words)
        
        if not statement_words:
            return 0.0
        
        # Score baseado em sobreposição de palavras
        overlap_score = len(common_words) / len(statement_words)
        
        # Bonus por qualidade da fonte
        quality_bonus = source.get("relevance_score", source.get("score", 0.5)) * 0.2
        
        return min(overlap_score + quality_bonus, 1.0)
    
    def _add_inline_citations(self, text: str, source_mappings: Dict[str, int]) -> str:
        """Adiciona citações inline ao texto"""
        
        cited_text = text
        
        # Ordena por tamanho decrescente para evitar conflitos de substituição
        sorted_statements = sorted(source_mappings.keys(), key=len, reverse=True)
        
        for statement in sorted_statements:
            citation_num = source_mappings[statement]
            
            # Adiciona citação no final da declaração
            citation_marker = f" [{citation_num}]"
            
            # Substitui apenas a primeira ocorrência
            cited_text = cited_text.replace(statement, statement + citation_marker, 1)
        
        return cited_text
    
    def _generate_bibliography(self, sources: List[Dict]) -> str:
        """Gera bibliografia formatada"""
        
        if not sources:
            return ""
        
        bibliography = "## References\n\n"
        
        for i, source in enumerate(sources, 1):
            title = source.get("title", "Untitled Source")
            url = source.get("url", "")
            
            # Formato: [1] Title - URL
            bibliography += f"[{i}] {title}"
            
            if url and url != "":
                bibliography += f" - {url}"
            
            bibliography += "\n"
        
        return bibliography
    
    def validate_citations(self, cited_report: str, sources: List[Dict]) -> Dict[str, Any]:
        """Valida se todas as citações estão corretas"""
        
        import re
        
        # Encontra todas as citações no texto
        citations = re.findall(r'\[(\d+)\]', cited_report)
        citation_numbers = [int(c) for c in citations]
        
        validation_result = {
            "total_citations": len(citation_numbers),
            "unique_citations": len(set(citation_numbers)),
            "max_citation": max(citation_numbers) if citation_numbers else 0,
            "total_sources": len(sources),
            "valid": True,
            "issues": []
        }
        
        # Verifica se todas as citações têm fontes correspondentes
        for num in set(citation_numbers):
            if num > len(sources):
                validation_result["valid"] = False
                validation_result["issues"].append(f"Citação [{num}] não tem fonte correspondente")
        
        # Verifica se há fontes não utilizadas
        used_sources = set(citation_numbers)
        total_sources = set(range(1, len(sources) + 1))
        unused_sources = total_sources - used_sources
        
        if unused_sources:
            validation_result["issues"].append(f"Fontes não utilizadas: {list(unused_sources)}")
        
        return validation_result

# Instância global do agente
citation_agent = CitationAgent()

@tool
def process_documents_for_citations(report: str, sources: List[Dict]) -> str:
    """
    Processa relatório de pesquisa adicionando citações apropriadas.
    
    Args:
        report: Texto do relatório
        sources: Lista de fontes utilizadas
        
    Returns:
        Relatório com citações inline e bibliografia
    """
    return citation_agent.process_research_report(report, sources)

@tool
def validate_report_citations(cited_report: str, sources: List[Dict]) -> Dict:
    """
    Valida se todas as citações no relatório estão corretas.
    
    Args:
        cited_report: Relatório com citações
        sources: Lista de fontes
        
    Returns:
        Resultado da validação
    """
    return citation_agent.validate_citations(cited_report, sources)

@tool
def format_source_bibliography(sources: List[Dict]) -> str:
    """
    Gera bibliografia formatada a partir das fontes.
    
    Args:
        sources: Lista de fontes
        
    Returns:
        Bibliografia formatada
    """
    return citation_agent._generate_bibliography(sources)