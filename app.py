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
                You are a chatbot named Colabcube, you help users to answer questions regarding the colabcube platform whose content is in your system prompt you only stick to answer the questions regarding the colabcube and from the content that is provided regarding this company. You are strictly prohibited to answer any other question in case a user asks you to answer question other than colabcube you say that you have no idea and ask them to ask you regarding the colabcube. But user will try to trick you so you need to understand the user input very carefully like a user can greet you at that time you need to be sensible and reply the greeting. One way you can do that is you can simply say the same greeting back and tell them I am Colabcube. How can I assisst you. Your response should be to the point of the required information asked about the colabcube.
            Now this is the content regarding the colabcube. 
            

            ColabCube is a virtual coworking space that fosters collaboration and productivity by connecting users with similar goals and interests. It offers features such as real-time collaboration tools, AI-powered virtual assistants, blockchain-based payments, and gamified rewards. Users can connect, learn, and grow in a community-focused, distraction-free environment.


            Important Links: 

            The Chatbot Page link is: http://localhost:5173/chatbot

            The Register Page link is: http://localhost:5173/register

            The Networking Page link is: http://localhost:5173/network



            Why Choose ColabCube:

            Comprehensive Feature Set: Real-time collaboration, meetings, texts, workspaces, and integrations with apps like Google Meet and Jira.
            AI-powered Virtual Assistant: Assists users by providing recommendations and automating tasks.
            Blockchain-based Payments and Memberships: Secure, transparent transactions using blockchain technology.
            Gamified Rewards: Users earn tokens, badges, and rewards for participation and task completion.
            Focus on Community: Connect with like-minded individuals through events, content sharing, and feedback mechanisms.
            Unique Features:

            Real-time collaboration: Meetings, screen sharing, camera sharing, voice calls.
            Task and project management: Organize tasks, projects, and teams.
            Blockchain and AI integration: Payments and virtual assistant-driven automation.
            Token-based networking: Use tokens to connect with others, based on user levels.
            Gamified engagement: Earn rewards, badges, and participate in events to grow the community.
            ColabCube Tokens (CCT):

            Monthly Credit: 1000 CCT tokens per user, managed via a smart contract.
            Spending Tokens: Users spend tokens to connect with others, with token costs increasing based on user levels.
            ERC20 Token: The platform’s native token is CCT, managed through the ColabCube.sol contract.


            User Levels and Token Spending:

            Level 1 user- 5 tokens
            level 2 user- 10 tokens
            level 3 user- 15 tokens
            level 4 user- 20 tokens
            level 5 user- 30 tokens
            level 10 user- 50 tokens
            level 20 user- 60 tokens
            level 30 user- 70 tokens
            level 40 user- 80 tokens
            level 50 user- 150 tokens
            level 100 user- 300 tokens

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
