from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os


load_dotenv()

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings
import config 


llm = HuggingFaceEndpoint(
    repo_id=config.HF_REPO_ID,
    task=config.HF_TASK,
    max_new_tokens=512,
    temperature=0.1,
    top_p=0.9,
    do_sample=True,
    repetition_penalty=1.1,
    return_full_text=False,
    timeout=60,
)

chat_model = ChatHuggingFace(llm=llm)

if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment")