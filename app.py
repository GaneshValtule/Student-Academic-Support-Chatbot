import streamlit as st
from bot import load_student_data, process_student_data, qa_chain
import traceback

st.set_page_config(page_title="🎓 Student Academic Assistant", layout="wide")
st.title("🎓 Student Academic Assistant")

# Session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "qa_chain" not in st.session_state:
    try:
        df = load_student_data()
        retriever = process_student_data(df)  # ensure this returns a retriever
        st.session_state.qa_chain = qa_chain(retriever, df)
        st.session_state.df = df
    except Exception:
        st.error("❌ Error initializing bot.")
        st.text(traceback.format_exc())

# Refresh
if st.button("🔄 Refresh / Restart Conversation"):
    st.session_state.conversation = []

# Display conversation
st.markdown("### 💬 Conversation")
chat_container = st.container()
with chat_container:
    for entry in st.session_state.conversation:
        st.markdown(
            f"<div style='padding:10px; margin-bottom:10px; border-radius:10px; background-color:#f0f2f6; color:black;'><b>🧑 You:</b> {entry['question']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='padding:10px; margin-bottom:15px; border-radius:10px; background-color:#e8f5e9; color:black;'><b>🤖 Bot:</b> {entry['answer']}</div>",
            unsafe_allow_html=True,
        )

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask a question:", key="input_1", placeholder="Type your query here...")
    submitted = st.form_submit_button("Send 🚀")

if submitted and user_input:
    try:
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.qa_chain.invoke({"question": user_input})

        response_text = (
            response.content
            if hasattr(response, "content")
            else response["text"]
            if isinstance(response, dict) and "text" in response
            else str(response)
        )

        st.session_state.conversation.append({
            "question": user_input,
            "answer": response_text
        })

        st.rerun()

    except Exception:
        st.error("⚠️ An error occurred while processing your question.")
        st.text(traceback.format_exc())