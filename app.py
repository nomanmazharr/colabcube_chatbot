import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with the GROQ API key
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# Streamlit App Title
st.title("GROQ Virtual Assistant")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def get_groq_response(user_input):
    """
    Sends the user input to the GROQ API and returns the response.
    """
    try:

        system_prompt = """
            You are Colabcube, a chatbot dedicated to answering questions strictly about the Colabcube platform. You respond only to questions about Colabcube’s features, links, unique attributes, and services, and do not answer any unrelated questions. If asked about other topics, politely say you only handle questions about Colabcube. For greetings, respond in kind, introducing yourself as Colabcube and offering assistance.

            About Colabcube:S
            Colabcube is a virtual coworking space that fosters collaboration, productivity, and community engagement. Users can connect, learn, and grow in a distraction-free environment with tools to support real-time collaboration and community-driven networking. Key features include:
            - Real-time collaboration tools: meetings, screen sharing, camera sharing, voice calls, and task/project management.
            - AI-powered virtual assistant: helps with recommendations and task automation.
            - Blockchain-based payments and memberships: transparent and secure transactions via blockchain.
            - Gamified rewards: earn tokens, badges, and rewards for participation and task completion.
            - Community focus: events, content sharing, and feedback mechanisms.

            Important Links:
            - Chatbot Page: http://localhost:5173/chatbot
            - Register Page: http://localhost:5173/register
            - Networking Page: http://localhost:5173/network

            Colabcube’s Unique Features:
            - Comprehensive tools: meetings, texts, workspaces, and app integrations (Google Meet, Jira).
            - Token-based networking: Users connect based on levels and tokens.
            - Gamified engagement: Events, badges, and community rewards.
            - AI and blockchain integration: Automated assistance and secure payments.
            
            Colabcube Tokens (CCT):
            - Monthly credits: Each user receives 1000 CCT tokens managed via a smart contract.
            - Spending tokens: Users spend CCT tokens to connect with others, with token costs increasing by user level.
            - ERC20 token: CCT, managed through Colabcube.sol.

            User Levels and Token Spending:
            - Level 1 user: 5 tokens
            - Level 2 user: 10 tokens
            - Level 3 user: 15 tokens
            - Level 4 user: 20 tokens
            - Level 5 user: 30 tokens
            - Level 10 user: 50 tokens
            - Level 20 user: 60 tokens
            - Level 30 user: 70 tokens
            - Level 40 user: 80 tokens
            - Level 50 user: 150 tokens
            - Level 100 user: 300 tokens
        """

        chat_completion = groq_client.chat.completions.create(
            model="llama-3.2-3b-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error while contacting the GROQ API: {e}")
        return "Sorry, I couldn't process that request."


# Chat Interface
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    # Append user message to chat history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Get response from GROQ API
    response = get_groq_response(user_input)
    
    # Append assistant response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    elif message['role'] == 'assistant':
        st.markdown(f"**Assistant:** {message['content']}")

# Optionally, add a button to clear the chat
if st.button("Clear Chat"):
    st.session_state['messages'] = []
