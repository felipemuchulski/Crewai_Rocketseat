#Instalação das libs
# pip install yfinance==0.2.41
# pip install crewai==0.28.8
# pip install "crewai[tools]"
# pip install --upgrade crewai
# pip install langchain==0.1.0
# pip install langchain-openai==0.1.7
# pip install -qU duckduckgo-search langchain-community==0.0.38
# pip install -U duckduckgo-search==5.3.0
# pip install streamlit
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])  # Added --upgrade

# ... (rest of your import statements)

# Upgrade langchain-community and langchain-core
# install("langchain-community>=0.2.10,<0.3.0")
# install("langchain-core>=0.2.27,<0.3.0")

# # Install other packages
# install("yfinance==0.2.41")
# install("crewai==0.28.8")
# install("crewai[tools]")
# install("langchain==0.1.0")           # This might be redundant after the upgrade
# install("langchain-openai==0.1.7")
# install("duckduckgo-search")
# install("streamlit") 
#Import das LIBS
import json
import os
from datetime import datetime

import yfinance as yf

from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults

import streamlit as st #Como construir uma aplicação web rapida e facil


# Criada função 
def fetch_stock_price(ticket):
    stock = yf.download(ticket, start="2023-08-08", end='2024-08-08')
    return stock

yahoo_finance_tool = Tool(
    name = "Yahoo Finance Tool",
    description = "Fetches stock prices for {ticket} from the last year using Yahoo Finance API.",
    func = lambda ticket: fetch_stock_price(ticket)
)
    

# Teste de execução
# response = yahoo_finance_tool.run("AAPL")
# print(response)


# Importar LLM
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
llm = ChatOpenAI(model='gpt-3.5-turbo')

# Create Agent AI
stockPriceAnalyst = Agent(
    role= "Senior stock price Analyst",
    goal="Find the {ticket} stock price and analyze trends.",
    backstory="""You're highly experienced in analyzing the price of a specific stock and making predictions about its future price.""",
    verbose=True,
    llm= llm,
    max_iter = 150,  # Aumentar o limite de iterações
    memory= True,
    tools= [yahoo_finance_tool],
    allow_delegation = False,
    max_execution_time = 300  # Definir um limite de tempo de 5 minutos
)



getStockPrice = Task(
    description = "Analyze the stock {ticket} price history and create a trend analysis of up, down, or sideways.",
    expected_output = """Specify the current trend of stock price - up, down, or sideways
     e.g., stock = 'AAPL, price UP'.""",
    agent = stockPriceAnalyst
)


# Important a tool search
search_tool = DuckDuckGoSearchResults(backend="news", num_results=10)


newsAnalyst = Agent(
    role= "Stock News Analyst",
    goal="""Create a short summary of the market news related to the stock {ticket} company. Specify the current trend - up, down, or sideways with the news context. For each requested stock asset, specify a number between 0 and 100, where 0 is extreme fear and 100 is extreme greed.""",
    backstory="""You're experienced in analyzing market trends and news and have tracked assets for more than 10 years. You're also a master-level analyst in traditional markets and have a deep understanding of human psychology. You understand news, their titles, and information, but you look at those with a healthy dose of skepticism. You also consider the source of the news articles.""",
    verbose=True,
    llm= llm,
    max_iter = 150,  # Aumentar o limite de iterações
    memory= True,
    tools= [search_tool],
    allow_delegation = False,
    max_execution_time = 300  # Definir um limite de tempo de 5 minutos
)


get_news = Task(
    description = f"""Take the stock and always include BTC in the analysis (if not requested).
    Use the search tool to search for each one individually.
    The current date is {datetime.now()}.
    Compose the results into a helpful report.""",
    expected_output = """A summary of the overall market and a one-sentence summary for each requested asset. Include a fear/greed score for each asset based on the news.
    Use the format:
        <STOCK ASSET>
        <SUMMARY BASED ON NEWS>
        <TREND PREDICTION>
        <FEAR/GREED SCORE>""",
    agent = newsAnalyst
)

stockAnalystWrite = Agent(
    role = "Senior Stock Analyst Writer",
    goal = """Analyze the price trends and news, and write an insightful, compelling, and informative 3-paragraph newsletter based on the stock report and price trend.""",
    backstory = """You're widely accepted as the best stock analyst in the market. You understand complex concepts and create compelling stories and narratives that resonate with wider audiences. You understand macro factors and combine multiple theories - e.g., cycle theory and fundamental analysis. You're able to hold multiple opinions when analyzing anything.""",
    verbose = True,
    llm = llm,
    max_iter = 150,  # Aumentar o limite de iterações
    memory= True,
    allow_delegation = True,
    max_execution_time = 600  # Definir um limite de tempo de 5 minutos
)

writeAnalyses = Task(
    description = """Use the stock price trend and the stock news report to create an analysis and write the newsletter about the {ticket} company that is brief and highlights the most important points. 
    Focus on the stock price trend, news, and fear/greed score. What are the near-future considerations?
    Include the previous analysis of stock trend and news summary.""",
    expected_output= """An eloquent 3-paragraph newsletter formatted as markdown in an easily readable manner. It should contain:
    - 3 bullets executive summary
    - Introduction - set the overall picture and spike up the interest
    - Main part - provides the meat of the analysis including the news summary and fear/greed scores
    - Summary - key facts and concrete future trend prediction - up, down, or sideways.""",
    agent = stockAnalystWrite,
    context = [getStockPrice, get_news]
)

crew = Crew(
    agents = [stockPriceAnalyst, newsAnalyst, stockAnalystWrite],
    tasks = [getStockPrice, get_news, writeAnalyses],
    verbose = True,
    process = Process.hierarchical,
    full_output = True,
    share_crew=False,
    manager_llm = llm,
    max_iter = 150,  # Aumentar o limite de iterações,
    max_execution_time = 600
)

# Executar 
#results = crew.kickoff(inputs={'ticket': 'AAPL'})

with st.sidebar:
    st.header('Enter the stock to Research')

    with st.form(key='research_form'):
        topic = st.text_input("Select the ticket")
        submit_button = st.form_submit_button(label= "Run Research")

if submit_button:
    if not topic:
        st.error("Please fill the ticket field")
    else: 
        results = crew.kickoff(inputs={'ticket': topic})
        for valor in results.tasks_output:
            combined_info = []
            descripition = valor.__dict__.get('description', '')
            summary = valor.__dict__.get('summary', '')
            raw = valor.__dict__.get('raw', '')

            #Markdown
            summary_markdown = st.markdown(str(summary))
            raw_markdown = st.markdown(str(raw))
            combined_info = f"{summary}\n{raw}"


            st.markdown(combined_info)

        st.subheader("Results of your research:")
        st.write(combined_info)