# step1 setup pydantic schema

from pydantic import BaseModel
from typing import List

class RequestModel(BaseModel):
    model_name:str
    model_provider:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

# step2 setup ai agent frontend request
from fastapi import FastAPI
from ai_agent import get_response
app=FastAPI()

MODEL_LIST=["gemini-2.5-pro","gemini-2.5-flash","gemini-2.0-flash","llama-3.1-8b-instant","llama-3.3-70b-versatile","openai/gpt-oss-120b"]
@app.post("/chat")
def chat_endpoint(request:RequestModel):
    """
    api endpoint to interact with chatbot using langgraph and search tools.
    dynamically select model and perform.
    """

    if request.model_name not in MODEL_LIST:
        return {"error":"invalid model"}
    
    llm_id=request.model_name
    provider=request.model_provider
    query=request.messages
    allow_search=request.allow_search
    system_prompt=request.system_prompt

    response=get_response(llm_id,provider,query,allow_search,system_prompt)
    return response

# step3 run app
import uvicorn

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)