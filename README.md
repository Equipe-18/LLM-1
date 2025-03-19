# Analisador Inteligente de Editais

Uma aplicação Streamlit para análise automática de editais e chamadas públicas usando processamento de linguagem natural e inteligência artificial.

## Sobre o Projeto

Este projeto oferece uma interface web para analisar editais de fundos públicos, extraindo automaticamente informações relevantes como:

- Título e objetivo
- Linhas temáticas
- Valores e prazos
- Requisitos de elegibilidade
- Contrapartidas obrigatórias

A análise é feita usando técnicas de NLP com spaCy (para extração de entidades) e modelos de linguagem via Ollama (para análise semântica avançada).

## Requisitos

- Python 3.8+
- Streamlit
- spaCy com modelo português (`pt_core_news_lg`)
- Ollama instalado localmente
- Conexão com internet

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/analisador-editais.git
cd analisador-editais
```

### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Baixe o modelo do spaCy para português

```bash
python -m spacy download pt_core_news_lg
```

### 4.1 Caso não funcione

venv\Scripts\python.exe -m pip install spacy
venv\Scripts\python.exe -m spacy download pt_core_news_lg


### 5. Instale o Ollama

#### Windows:
1. Baixe o instalador do Ollama para Windows em [ollama.ai/download](https://ollama.ai/download)
2. Execute o instalador e siga as instruções
3. Após a instalação, o Ollama será executado como um serviço em segundo plano

#### macOS:
1. Baixe o aplicativo Ollama para macOS em [ollama.ai/download](https://ollama.ai/download)
2. Arraste o aplicativo para a pasta Aplicativos
3. Abra o Ollama para iniciar o serviço

#### Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 6. Baixe o modelo para o Ollama

```bash
ollama pull llama2
```

## Executando a Aplicação

Ative o ambiente virtual (caso ainda não esteja ativo):

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Inicie a aplicação:

```bash
streamlit run app.py
```

Seu navegador abrirá automaticamente com a aplicação rodando em `http://localhost:8501`

## Como Usar

1. Digite seu prompt de análise ou selecione um dos templates disponíveis
2. Inclua a URL do edital que deseja analisar
3. Clique em "Analisar"
4. Aguarde o processamento e visualize os resultados

## Solução de Problemas

- **Erro ao conectar com Ollama**: Verifique se o serviço Ollama está em execução (padrão: `http://localhost:11434`)
- **Timeout durante a análise**: Tente usar um modelo menor no Ollama ou reduza o tamanho do texto analisado
- **Erro no download do modelo spaCy**: Verifique sua conexão com a internet ou tente baixar um modelo menor (`pt_core_news_md` ou `pt_core_news_sm`)

## Arquivo requirements.txt

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```
streamlit>=1.26.0
spacy>=3.6.0
requests>=2.28.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.
