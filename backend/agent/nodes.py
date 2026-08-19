import os 
from typing import Dict, Any 

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


from .state import AgentState
from .tools import tavily_search , fetch_page


load_dotenv()

gemini =ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api=getenv.os("GEMINI_API_KEY")
)