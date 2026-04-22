from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()

chat_model = ChatGroq(model_name="llama-3.3-70b-versatile",max_tokens=10000,temperature=0.7)

import os

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found in environment")