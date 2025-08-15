#step1 setup api keys groq and tavily
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key=os.environ.get("GROQ_API_KEY")
gemini_api_key=os.environ.get("GEMINI_API_KEY")
tavily_api_key=os.environ.get("TAVILY_API_KEY")
#step2 setup llm and tools

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI as  Gemini
from langchain_tavily import TavilySearch


#step3 setup ai agent with search tool functionality



system_prompt="act as an ai chatbot who is smart and friendly"

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage,AIMessage

def get_response(llm_id,provider,query,allow_search,system_prompt):

    if provider=="GROQ":
        llm=ChatGroq(model=f"{llm_id}",api_key=groq_api_key)
    elif provider=="GEMINI":
        llm=Gemini(model=f"{llm_id}",api_key=gemini_api_key)
    else:
        raise ValueError(f"unknown provider")
    # query="tell me about gen ai in a short paragraph"

    search_tool=[TavilySearch(max_results=2)] if allow_search else []
    
    agent=create_react_agent(
        model=llm,
        tools=search_tool,
        prompt=SystemMessage(system_prompt)
    )
    state={"messages":query}

    response=agent.invoke(state)
    messages=response.get('messages')
    ai_message=[message.content for message in messages if isinstance(message,AIMessage)]
    print(ai_message[-1])
    return ai_message[-1]