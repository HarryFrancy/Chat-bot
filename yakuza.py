from groq import Groq
import streamlit as st
import json as jp
client = Groq(api_key="xyz")


RULES= '''

        1. You are my virtual assistant.
        2. Be calm, clear, and helpful.
        3. Greet with "Hello Harry, good morning" only once at the start.
        4. After the first greeting, do not repeat it again.
        5. Keep all responses under 200 words.
        6. If asked about sexual topics, reply only: "--not interested--".
        7. If the user greets again (hi, hello, etc.), respond with "What would you like me to do?"
        8. Stay consistent in tone and behavior.
        
        '''
st.markdown("<h1 style='text-align: center; color: #00d4ff; font-family: Arial; letter-spacing: 2px;'>🤖 AI Bot</h1>", unsafe_allow_html=True)

def load():
    try:
        with open("log.json","r") as f:
            return jp.load(f)
    except:
        return [{"role":"system","content":RULES}]
    


if "messages" not in st.session_state:
    st.session_state.messages = load()
    

def save():
    with open("log.json","w") as f:
        jp.dump(st.session_state.messages,f)

def history(messages):
    for mg in messages[1:]:
        if mg["role"]=="user":
            st.write("YOU : ",mg["content"])
        if mg["role"]=="assistant":
            st.write("AI : ",mg["content"])

def clear():
    
    st.session_state.messages=[st.session_state.messages[0]]
    save()

for message in st.session_state.messages:
    if message["role"]=="system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])




user_input = st.chat_input("your message")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)
        save()
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="llama-3.3-70b-versatile",
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"):
        st.write(reply)
        save()


elif st.button("show history"):
    history(messages=st.session_state.messages)
            
elif st.button("clear history"):
    clear()

if "show_mode" not in st.session_state:
    st.session_state.show_mode=False
if st.button("show_mode"):
    st.session_state.show_mode=True

    if st.session_state.show_mode:
        with st.form("change mode"):
            personality = st.radio("select your mode",
            ("teacher","chill","strict"))
            submitted = st.form_submit_button("select")

        if submitted:
        

            if personality == "teacher":
                    mode_rules = (
                    "Explain things step by step. "
                    "Use simple examples. "
                    "Assume the user is learning. "
                    "Break complex ideas into smaller parts."
                )

            elif personality == "strict":
                    mode_rules = (
                    "Be precise and direct. "
                    "Give short, factual answers only. "
                    "Do not add extra explanation unless asked. "
                    "Stay professional and serious."
                )

            elif personality == "chill":
                    mode_rules = (
                    "Be relaxed and conversational. "
                    "Use simple, friendly language. "
                    "Keep answers easy to understand. "
                    "Avoid being too formal."
                )
                    
            
            st.session_state.messages[0] = {"role": "system", "content": mode_rules}
            st.session_state.show_mode = False
            st.rerun()





    