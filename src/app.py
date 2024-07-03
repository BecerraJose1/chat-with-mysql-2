from dotenv import load_dotenv  # Import dotenv for managing environment variables
from langchain_community.utilities import SQLDatabase  # Import SQLDatabase from langchain_community module
import streamlit as st  # Import Streamlit for building the web application

def init_database(user:str, password:str, host:str, port: str, database:str) -> SQLDatabase:
    """
    Initializes and returns an SQLDatabase object using the provided credentials.

    Args:
        user (str): Database username.
        password (str): Database password.
        host (str): Database host address.
        port (str): Database port number.
        database (str): Database name.

    Returns:
        SQLDatabase: Initialized SQLDatabase object connected to the specified database.
    """
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)  # Connects to the database using the URI and returns the SQLDatabase object

load_dotenv()  # Loads environment variables from a .env file if present

# Setting Streamlit page configuration
st.set_page_config(
    page_title="Chat with Hootsi",  # Title of the web page
    page_icon=":speech_balloon:",  # Icon shown on the browser tab
    layout="wide",  # Sets the layout of the app to wide
    initial_sidebar_state="expanded"  # Sets the initial state of the sidebar to expanded
)

st.title("Chat with Hootsi")  # Displays a title on the Streamlit app page

with st.sidebar:  # Defines content for the sidebar
    st.subheader("Settings")  # Subheader for the settings section
    st.write("This is a chat application using MySQL for Hootsi.")  # Description of the app

    # Input fields for database connection parameters
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type="password", value="example", key="Password")
    st.text_input("Database", value="DB", key="Database")

    # Button to initiate database connection
    if st.button("Connect"):
        with st.spinner("Connecting to the DB..."):  # Displays a spinner while connecting
            # Calls init_database function with user inputs and establishes connection
            db = init_database(
                st.session_state["User"],  # Retrieves user input from session state
                st.session_state["Password"],  # Retrieves password input from session state
                st.session_state["Host"],  # Retrieves host input from session state
                st.session_state["Port"],  # Retrieves port input from session state
                st.session_state["Database"]  # Retrieves database input from session state
            )
            st.session_state.db = db  # Stores the database connection object in session state
            st.success("Connected!")  # Displays success message once connected

st.chat_input("Type a message...")  # Displays an input box for typing messages in the main app section
