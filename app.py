import streamlit as st
import spacy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import Dict, List, Optional
from datetime import datetime
import json

# Carrega o modelo do spaCy
nlp = spacy.load("pt_core_news_lg")

class EditalExtractor:
    """Classe base para extração de dados de editais"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
    def extrair_conteudo(self, url: str) -> Optional[Dict]:
        """Extrai conteúdo do site"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove elementos irrelevantes
            for tag in ['script', 'style', 'nav', 'footer']:
                for element in soup.find_all(tag):
                    element.decompose()
                    
            return {
                'html': str(soup),
                'text': soup.get_text(separator='\n', strip=True),
                'url': url
            }
        except Exception as e:
            st.error(f"Erro ao extrair conteúdo: {str(e)}")
            return None

class ProcessadorNLP:
    """Classe para processamento de linguagem natural"""
    
    def __init__(self):
        self.nlp = nlp
        
    def processar_texto(self, texto: str) -> Dict:
        """Processa o texto usando spaCy"""
        doc = self.nlp(texto[:1000000])  # Limita tamanho para performance
        
        return {
            'entidades': self._extrair_entidades(doc),
            'frases_chave': self._extrair_frases_chave(doc),
            'categorias': self._categorizar_texto(doc)
        }
    
    def _extrair_entidades(self, doc) -> Dict:
        """Extrai entidades nomeadas relevantes"""
        entidades = {
            'datas': [],
            'valores': [],
            'organizacoes': [],
            'temas': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                entidades['datas'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entidades['valores'].append(ent.text)
            elif ent.label_ == 'ORG':
                entidades['organizacoes'].append(ent.text)
            
        return entidades
    
    def _extrair_frases_chave(self, doc) -> List[str]:
        """Extrai frases importantes usando análise sintática"""
        frases_chave = []
        
        for sent in doc.sents:
            # Identifica frases com palavras-chave relevantes
            if any(palavra in sent.text.lower() for palavra in [
                'objetivo', 'prazo', 'recurso', 'financiamento', 'contrapartida',
                'elegível', 'requisito', 'valor'
            ]):
                frases_chave.append(sent.text.strip())
                
        return frases_chave
    
    def _categorizar_texto(self, doc) -> List[str]:
        """Categoriza o texto em áreas temáticas"""
        categorias = set()
        
        # Lista de palavras-chave por categoria
        areas_tematicas = {
            'Tecnologia': ['tecnologia', 'inovação', 'digital', 'software'],
            'Saúde': ['saúde', 'médico', 'hospital', 'clínico'],
            'Educação': ['educação', 'ensino', 'escola', 'acadêmico'],
            'Meio Ambiente': ['sustentável', 'ambiental', 'ecológico'],
            'Infraestrutura': ['infraestrutura', 'construção', 'obra'],
        }
        
        texto = doc.text.lower()
        for area, palavras in areas_tematicas.items():
            if any(palavra in texto for palavra in palavras):
                categorias.add(area)
                
        return list(categorias)

class ProcessadorOllama:
    """Classe para processamento com Ollama"""
    
    def __init__(self, modelo="llama2"):
        self.modelo = modelo
        self.url_base = "http://localhost:11434/api/generate"
    
    def analisar_edital(self, dados: Dict) -> Optional[str]:
        """Analisa dados do edital usando Ollama"""
        prompt = self._construir_prompt(dados)
        
        try:
            response = requests.post(
                self.url_base,
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "temperature": 0.1,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response")
                
        except Exception as e:
            st.error(f"Erro no processamento Ollama: {str(e)}")
            return None
    
    def _construir_prompt(self, dados: Dict) -> str:
        """Constrói prompt especializado usando o prompt do usuário"""
        prompt_usuario = dados.get('prompt_analise', '')
        
        return f"""
        Com base no seguinte prompt do usuário:
        {prompt_usuario}
        
        Analise o seguinte conteúdo e forneça uma resposta estruturada que atenda especificamente à solicitação do usuário.
        Se alguma informação solicitada não for encontrada, indique explicitamente como "Não encontrado".
        
        Conteúdo para análise:
        {dados['text'][:2000]}  # Limita o tamanho para evitar timeout
        
        Entidades relevantes identificadas:
        {json.dumps(dados['entidades'], indent=2, ensure_ascii=False)}
        
        Categorias identificadas:
        {json.dumps(dados['categorias'], indent=2, ensure_ascii=False)}
        """

def main():
    st.set_page_config(page_title="Extrator de Editais", page_icon="📄", layout="wide")
    st.title("Analisador Inteligente de Editais")

    # Template de prompt padrão
    default_prompt = """Extraia e categorize informações sobre chamadas públicas, incluindo:
    - Título
    - Objetivo
    - Linha temática
    - Tipo de recurso financeiro
    - Contrapartida obrigatória
    - Prazos
    
    URL para análise: """

    # Interface do usuário com prompt
    prompt = st.text_area(
        "Digite seu prompt de análise:",
        value=default_prompt,
        height=200
    )

    # Botões para templates de prompt
    st.markdown("### Templates de Prompt")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Análise Básica"):
            st.session_state.prompt = default_prompt
            
    with col2:
        if st.button("🎯 Análise de Elegibilidade"):
            st.session_state.prompt = """Analise este edital e determine:
            - Quem pode participar
            - Requisitos principais
            - Restrições importantes
            - Contrapartida necessária
            
            URL para análise: """
            
    with col3:
        if st.button("📊 Análise Financeira"):
            st.session_state.prompt = """Analise os aspectos financeiros:
            - Valor total disponível
            - Tipos de recursos
            - Contrapartidas
            - Itens financiáveis
            
            URL para análise: """

    if st.button("Analisar"):
        # Extrai URL do prompt
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', prompt)
        
        if not urls:
            st.error("Nenhuma URL encontrada no prompt. Por favor, inclua uma URL válida.")
            return

        url = urls[0]  # Usa a primeira URL encontrada
        
        with st.spinner("Processando..."):
            # Extração
            extractor = EditalExtractor()
            conteudo = extractor.extrair_conteudo(url)
            
            if conteudo:
                # Adiciona o prompt original aos dados
                conteudo['prompt_usuario'] = prompt
                
                # Processamento NLP
                processador_nlp = ProcessadorNLP()
                analise_nlp = processador_nlp.processar_texto(conteudo['text'])
                
                # Processamento Ollama com prompt personalizado
                processador_ollama = ProcessadorOllama()
                dados_combinados = {
                    **conteudo,
                    **analise_nlp,
                    'prompt_analise': prompt  # Inclui o prompt na análise
                }
                analise_ollama = processador_ollama.analisar_edital(dados_combinados)
                
                # Exibição dos resultados
                st.markdown("### Resultados da Análise")
                
                # Dividir a tela em duas colunas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Análise Técnica (spaCy)")
                    st.write("**Entidades Identificadas:**")
                    st.json(analise_nlp['entidades'])
                    
                    st.write("**Categorias:**")
                    st.write(analise_nlp['categorias'])
                    
                    st.write("**Trechos Relevantes:**")
                    for frase in analise_nlp['frases_chave']:
                        st.markdown(f"- {frase}")
                
                with col2:
                    st.markdown("#### Resposta ao Prompt")
                    if analise_ollama:
                        st.markdown(analise_ollama)
                    else:
                        st.error("Não foi possível gerar a análise.")

if __name__ == "__main__":
    main()