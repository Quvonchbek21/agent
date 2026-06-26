import time
from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_ai_agent

app = FastAPI(title="MARKETPLACE AI AGENT")

class UserQuery(BaseModel):
    text: str

@app.post("/ask")
def ask_agent(query: UserQuery):
    total_start_time = time.time()  # Sxemadagi total-time boshlanishi
    
    # Agentni ishga tushirish
    agent_response = run_ai_agent({"text": query.text})
    
    # Sxemadagi total-time yakunlanishi
    total_end_time = time.time()
    agent_response["logs"]["total_time"] = round(total_end_time - total_start_time, 4)
    
    return agent_response