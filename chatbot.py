import os
import streamlit as st # type: ignore
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# Initialize Chat Model
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    openai_api_base=os.environ["OPENAI_API_BASE"],
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

# Streamlit UI
st.set_page_config(page_title="AI Chatbot 💬", page_icon="🤖", layout="centered")
st.title("🤖 AI Chatbot with OpenRouter")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Write something to ask...")
if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response
    with st.spinner("Thinking..."):
        response = llm.invoke([HumanMessage(content=user_input)])
        reply = response.content

    # Display AI reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
