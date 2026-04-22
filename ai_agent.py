import os
from dotenv import load_dotenv

load_dotenv() 
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY= os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

openai_llm= ChatOpenAI(model="gpt-4o-mini")
groq_llm= ChatGroq(model="llama-3.3-70b-versatile")

from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
system_prompt='act as chatbot who is smart and friendly'

def get_response(llm_id,query,allow_search,system_prompt,provider):
    if provider == "Groq" :
        llm=ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm=ChatOpenAI(model=llm_id) 

    Tool=[TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_agent(
        model=llm,
        tools=Tool,
        system_prompt=system_prompt
    )

    state={"messages":query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]