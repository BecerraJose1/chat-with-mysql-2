from dotenv import load_dotenv
import streamlit as st


load_dotenv()

st.set_page_config(page_title="Chat with Hootsi",page_icon=" :speech_balloon:" )

st.title("Chat with Hootsi")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a chat application using MySQL for Hootsi.")

    st.text_input("Host", value="localhost")
    st.text_input("Port", value="3306")
    st.text_input("User", value="root")
    st.text_input("Password", type="password", value="example")
    st.text_input("Database", value="DB")

    st.button("Connect")