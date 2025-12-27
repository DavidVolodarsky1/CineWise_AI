import streamlit as st
from app.agent import CineWiseAgent

st.set_page_config(page_title="CineWise AI", page_icon="🎬")

# CSS חזק יותר ליישור לימין (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    
    html, body, [data-testid="ststAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Assistant', sans-serif;
    }
    [data-testid="stChatMessage"] {
        flex-direction: row-reverse !important;
        text-align: right;
    }
    .stMarkdown {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = CineWiseAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# כותרת
st.title("🎬 CineWise AI")

# תצוגת הודעות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# צ'אט
if prompt := st.chat_input("שאל אותי משהו..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("מעבד נתונים...", expanded=False) as status:
            try:
                response = st.session_state.agent.chat(prompt)
                status.update(label="הושלם!", state="complete")
            except Exception as e:
                status.update(label="שגיאת Rate Limit", state="error")
                response = "מצטער, הגעתי למכסת ההודעות היומית שלי ב-Groq. נסה שוב בעוד שעה או החלף מודל."
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})