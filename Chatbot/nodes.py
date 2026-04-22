from langchain_core.messages import HumanMessage, AIMessage
from state import ChatState
from llm import chat_model
from prompts import CHAT_PROMPT


def chatbot_node(state: ChatState):
    question = state["question"]
    messages = state["messages"]

    chain = CHAT_PROMPT | chat_model

    response = chain.invoke({
        "question": question,
        "chat_history": messages
    })

    content = response.content if hasattr(response, "content") else str(response)

    updated_messages = messages + [
        HumanMessage(content=question),
        AIMessage(content=content)
    ]

    return {
        "question": question,
        "answer": content,
        "messages": updated_messages
    }