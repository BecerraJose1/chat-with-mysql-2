# Import necessary libraries
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import streamlit as st
import pandas as pd

# Load datasets for projects and common device errors
def load_datasets():
    # Load your prepared datasets here
    projects_df = pd.read_json("src/dataset.json")  # Update with your dataset path
    errors_df = pd.read_json("src/dataset.json")  # Update with your dataset path
    return projects_df, errors_df

# Initialize chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm the Device Assistant. What seems to be the problem with your device?")
    ]

# Load environment variables from a .env file
load_dotenv()

# Set the page configuration for Streamlit
st.set_page_config(page_title="Chat with Device Assistant", page_icon=":speech_balloon:")

# Display the title of the chat application
st.title("Chat with Device Assistant")

# Load datasets
projects_df, errors_df = load_datasets()

# Function to determine project based on customer address
def get_project(address):
    project_info = projects_df[projects_df['address'] == address]
    if not project_info.empty:
        return project_info.iloc[0]  # Return the first matching project
    return None

# Function to get error resolution based on the error type
def get_resolution(error_type):
    resolution_info = errors_df[errors_df['error'] == error_type]
    if not resolution_info.empty:
        return resolution_info.iloc[0]['resolution'], resolution_info.iloc[0]['action']
    return None, None

# Function to generate responses using OpenAI
def generate_response(prompt):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    response = llm([HumanMessage(content=prompt)])
    return response.content

# Display the chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

# Get user input for a new chat message
user_query = st.chat_input("Type your address...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    project_info = get_project(user_query)

    if project_info is not None:
        response = f"We found the project associated with your address: {project_info['project_name']}."
        st.session_state.chat_history.append(AIMessage(content=response))
        with st.chat_message("AI"):
            st.markdown(response)
        
        # Ask for the error type next
        error_query = st.chat_input("What error are you experiencing?")
        if error_query is not None and error_query.strip() != "":
            st.session_state.chat_history.append(HumanMessage(content=error_query))
            
            resolution, action = get_resolution(error_query)
            if resolution and action:
                response = f"To resolve the issue, please try the following action: {action}."
            else:
                # Generate a response using OpenAI if the error is not found
                prompt = f"I couldn't find a solution for the error: '{error_query}'. Can you provide a detailed description or suggest troubleshooting steps?"
                response = generate_response(prompt)
                
            st.session_state.chat_history.append(AIMessage(content=response))
            with st.chat_message("AI"):
                st.markdown(response)
    else:
        response = "I'm sorry, I couldn't find a project associated with that address. Please check and try again."
        st.session_state.chat_history.append(AIMessage(content=response))
        with st.chat_message("AI"):
            st.markdown(response)
