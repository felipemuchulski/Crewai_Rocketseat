## crewai-stock.py - Analisador de Ações com IA

Este código Python implementa um sistema de análise de ações com a ajuda de Inteligência Artificial, utilizando a biblioteca LangChain para gerenciar tarefas e a CrewAI para organizar agentes e suas interações. O projeto visa fornecer análises de ações e insights baseados em dados históricos de preços, notícias relevantes e análise de sentimento do mercado.

### O que o código faz?

O código cria um "time" de agentes de IA especializados em diferentes áreas da análise de ações:

* **Analista de Preços de Ações (stockPriceAnalyst):**  
    - Coleta dados históricos de preços de ações através do Yahoo Finance.
    - Analisa as tendências de preços (alta, baixa, lateral).
* **Analista de Notícias de Ações (newsAnalyst):**
    - Busca notícias relevantes sobre a empresa e o mercado.
    - Resume as notícias em um formato conciso.
    - Determina a tendência do mercado (alta, baixa, lateral) com base nas notícias.
    - Calcula um "índice de medo/ganância" (Fear/Greed Score) para avaliar o sentimento do mercado.
* **Escritor Sênior de Análise de Ações (stockAnalystWrite):**
    - Combina as informações de preços e notícias.
    - Gera um boletim informativo (newsletter) conciso e informativo sobre a ação.

O código também define tarefas para cada agente:

* **getStockPrice:** Busca dados de preços da ação e analisa a tendência.
* **get_news:** Busca e resume notícias sobre a ação e o mercado.
* **writeAnalyses:** Cria o boletim informativo com base nas análises de preço e notícias.

A CrewAI gerencia a execução das tarefas, coordenando os agentes para produzir uma análise abrangente da ação.

### Como usar o código:

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure a API Key do OpenAI:**
   - Crie uma conta no OpenAI (https://platform.openai.com/account/api-keys) e obtenha uma API Key.
   - Defina a API Key no arquivo `secrets.py`:
     ```python
     OPENAI_API_KEY = "sua_chave_api"
     ```

3. **Execute o código:**
   - Execute o arquivo `crewai-stock.py`.
   - O código abrirá uma interface web no navegador (Streamlit).
   - Insira o código da ação (ticker) no campo "Select the ticket" e clique em "Run Research".

4. **Visualize os resultados:**
   - O código exibirá os resultados da análise na interface web.

### Detalhes do Código

#### Imports:

* **subprocess:** Para executar comandos do sistema (pip).
* **sys:** Para acessar variáveis e funções do sistema.
* **json:** Para trabalhar com dados JSON.
* **os:** Para interagir com o sistema operacional.
* **datetime:** Para trabalhar com datas e horários.
* **yfinance:** Para baixar dados de preços de ações do Yahoo Finance.
* **crewai:** Para gerenciar agentes de IA.
* **langchain.tools:** Para definir ferramentas para os agentes.
* **langchain_openai:** Para interagir com a API do OpenAI.
* **langchain_community.tools:** Para usar ferramentas predefinidas da LangChain.
* **streamlit:** Para criar a interface web.

#### Funções:

* **install(package):** Instala um pacote Python com o pip.
* **fetch_stock_price(ticket):** Baixa dados de preços de ações do Yahoo Finance.

#### Agentes:

* **stockPriceAnalyst:** Analisa preços de ações.
* **newsAnalyst:** Analisa notícias sobre ações.
* **stockAnalystWrite:** Gera um boletim informativo com a análise da ação.

#### Tarefas:

* **getStockPrice:** Coleta dados de preços e analisa a tendência.
* **get_news:** Coleta e resume notícias sobre a ação.
* **writeAnalyses:** Gera o boletim informativo.

#### CrewAI:

* **crew:** Define a equipe de agentes e tarefas.

#### Streamlit:

* **st:** Define a interface web para interagir com o código.

### Próximos Passos:

* **Melhorar a análise de sentiment:** Implementar um modelo de linguagem mais avançado para analisar o sentiment das notícias.
* **Incorporar indicadores técnicos:** Adicionar análises de indicadores técnicos como médias móveis, MACD, etc.
* **Criar um dashboard:** Implementar um dashboard para visualizar os resultados da análise.
* **Automatizar a execução:** Integrar o código com um sistema de agendamento para executar a análise periodicamente.
