import os
import requests
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import streamlit as st

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI API
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=openai_api_key)

# Sample dataset to map locations to projects and devices
data = {
    "Location A": {"project": "Project X", "devices": ["Apple TV", "Crestron"]},
    "Location B": {"project": "Project Y", "devices": ["Sonos", "Apple TV"]},
}

# Function to get project and devices based on location
def get_project_info(location):
    return data.get(location)

# Function to handle device commands
def send_device_command(device, action):
    api_endpoint = f"http://your-server/api/{device}/{action}"  # Modify as needed
    response = requests.post(api_endpoint)  # Ensure your server supports POST requests
    return response.text

# Initialize chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm the Smart Device Assistant. What's your name?"),
    ]

# Set the page configuration for Streamlit
st.set_page_config(page_title="Smart Device Assistant", page_icon=":speech_balloon:")

# Display the title of the chat application
st.title("Chat with the Smart Device Assistant")

# Display the chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

# Get user input for a new chat message
user_query = st.chat_input("Type your message here...")
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    # Initialize response variable
    response = ""

    # Check if user has provided their name and location
    user_name = None
    user_location = None

    # Extracting user information
    if "name" not in st.session_state:
        st.session_state["name"] = user_query  # First message is name
        user_name = user_query
        st.session_state.chat_history.append(AIMessage(content=f"Nice to meet you, {user_name}! Where are you located?"))
    elif "location" not in st.session_state:
        st.session_state["location"] = user_query  # Second message is location
        user_location = user_query
        project_info = get_project_info(user_location)

        if project_info:
            st.session_state.chat_history.append(AIMessage(content=f"You're part of {project_info['project']}. You have the following devices: {', '.join(project_info['devices'])}. How can I assist you today?"))
        else:
            st.session_state.chat_history.append(AIMessage(content="Sorry, I couldn't find your project information. Can you specify again?"))
    else:
        # Handle requests related to device control
        device_issue = user_query  # This could be more sophisticated with NLP
        device = "Apple TV"  # Example device
        action = "reboot"  # Example action based on user input (to be extracted from user_query)

        response = send_device_command(device, action)
        st.session_state.chat_history.append(AIMessage(content=response))

    # Display user input
    with st.chat_message("Human"):
        st.markdown(user_query)

    # Generate response from OpenAI (if needed)
    if "name" in st.session_state and "location" in st.session_state:
        response = llm.invoke({
            "question": user_query,
            "chat_history": st.session_state.chat_history,
        })
        st.session_state.chat_history.append(AIMessage(content=response))

    # Display AI response only if it's defined
    if response:
        with st.chat_message("AI"):
            st.markdown(response)

