from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from state import ChatState
from llm import chat_model
from prompts import CHAT_PROMPT


def chatbot_node(state: ChatState):
    question = state["question"]
    messages = state["messages"]  # existing history from checkpointer

    chain = CHAT_PROMPT | chat_model

    response = chain.invoke({
        "question": question,
        "chat_history": messages
    })

    content = response.content if hasattr(response, "content") else str(response)

    # Only return the NEW messages to be appended.
    # The add_messages reducer will append these to the existing checkpoint state.
    # Returning the full history would cause it to be doubled each turn.
    new_messages = [
        HumanMessage(content=question),
        AIMessage(content=content),
    ]

    return {
        "question": question,
        "answer": content,
        "messages": new_messages,
    }