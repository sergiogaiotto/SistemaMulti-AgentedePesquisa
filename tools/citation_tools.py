import re
from typing import List, Dict, Tuple
from langchain_core.tools import tool

class CitationProcessor:
    """Processador de citações para relatórios de pesquisa"""
    
    def __init__(self):
        self.citation_counter = 1
        self.sources = {}
    
    def process_citations(self, text: str, sources: List[Dict]) -> str:
        """Adiciona citações ao texto baseado nas fontes fornecidas"""
        self.sources = {i+1: source for i, source in enumerate(sources)}
        self.citation_counter = 1
        
        # Processa o texto para adicionar citações
        cited_text = self._add_citations_to_text(text, sources)
        
        # Adiciona bibliografia no final
        bibliography = self._generate_bibliography()
        
        return f"{cited_text}\n\n{bibliography}"
    
    def _add_citations_to_text(self, text: str, sources: List[Dict]) -> str:
        """Adiciona citações inline no texto"""
        # Identifica declarações que precisam de citação
        sentences = re.split(r'(?<=[.!?])\s+', text)
        cited_sentences = []
        
        for sentence in sentences:
            if self._needs_citation(sentence):
                # Encontra a melhor fonte para esta sentença
                best_source_idx = self._find_best_source(sentence, sources)
                if best_source_idx:
                    sentence = f"{sentence} [{best_source_idx}]"
            
            cited_sentences.append(sentence)
        
        return ' '.join(cited_sentences)
    
    def _needs_citation(self, sentence: str) -> bool:
        """Determina se uma sentença precisa de citação"""
        # Palavras-chave que indicam necessidade de citação
        citation_keywords = [
            "according to", "research shows", "studies indicate", 
            "data reveals", "reports suggest", "analysis shows",
            "founded in", "headquarters", "revenue", "employees",
            "specializes in", "offers", "provides", "develops"
        ]
        
        sentence_lower = sentence.lower()
        return any(keyword in sentence_lower for keyword in citation_keywords)
    
    def _find_best_source(self, sentence: str, sources: List[Dict]) -> int:
        """Encontra a melhor fonte para uma sentença específica"""
        best_score = 0
        best_idx = None
        
        for i, source in enumerate(sources, 1):
            score = self._calculate_relevance_score(sentence, source)
            if score > best_score:
                best_score = score
                best_idx = i
        
        return best_idx if best_score > 0.3 else None
    
    def _calculate_relevance_score(self, sentence: str, source: Dict) -> float:
        """Calcula score de relevância entre sentença e fonte"""
        sentence_words = set(sentence.lower().split())
        source_content = source.get("content", "").lower()
        source_title = source.get("title", "").lower()
        
        # Conta palavras em comum
        source_words = set((source_content + " " + source_title).split())
        common_words = sentence_words.intersection(source_words)
        
        if not sentence_words:
            return 0
        
        return len(common_words) / len(sentence_words)
    
    def _generate_bibliography(self) -> str:
        """Gera bibliografia formatada"""
        if not self.sources:
            return ""
        
        bibliography = "## References\n\n"
        for idx, source in self.sources.items():
            title = source.get("title", "Untitled")
            url = source.get("url", "")
            
            bibliography += f"[{idx}] {title}"
            if url:
                bibliography += f" - {url}"
            bibliography += "\n"
        
        return bibliography

# Instância global do processador
citation_processor = CitationProcessor()

@tool
def add_citations_to_report(report_text: str, sources: List[Dict]) -> str:
    """
    Adiciona citações a um relatório de pesquisa.
    
    Args:
        report_text: Texto do relatório
        sources: Lista de fontes com title, url, content
        
    Returns:
        Relatório com citações inline e bibliografia
    """
    return citation_processor.process_citations(report_text, sources)

@tool
def extract_key_facts(text: str) -> List[str]:
    """
    Extrai fatos-chave de um texto que precisam de citação.
    
    Args:
        text: Texto para analisar
        
    Returns:
        Lista de fatos-chave identificados
    """
    # Patterns para identificar fatos importantes
    fact_patterns = [
        r'founded in \d{4}',
        r'headquarters in [A-Z][a-z]+',
        r'revenue of \$[\d,]+',
        r'\d+[\+]? employees',
        r'raised \$[\d,]+ in funding',
        r'valued at \$[\d,]+',
    ]

    facts = []
    for pattern in fact_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        facts.extend(matches)
    
    return facts

@tool
def format_company_info(company_data: Dict) -> str:
    """
    Formata informações de uma empresa de forma estruturada.
    
    Args:
        company_data: Dicionário com dados da empresa
        
    Returns:
        Texto formatado com informações da empresa
    """
    formatted = []
    
    name = company_data.get("name", "Unknown Company")
    formatted.append(f"**{name}**")
    
    if "website" in company_data:
        formatted.append(f"Website: {company_data['website']}")
    
    if "description" in company_data:
        formatted.append(f"Description: {company_data['description']}")
    
    if "industry" in company_data:
        formatted.append(f"Industry: {company_data['industry']}")
    
    if "founded" in company_data:
        formatted.append(f"Founded: {company_data['founded']}")
    
    if "location" in company_data:
        formatted.append(f"Location: {company_data['location']}")
    
    return "\n".join(formatted)