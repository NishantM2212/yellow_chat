import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Helper Functions
# ----------------------------

def get_chat_response(message, conversation_history, api_provider, model):
    """
    Get response from OpenAI API or Claude API
    """
    if api_provider == "gpt":
        try:
            messages = []
            # Convert conversation history to OpenAI format
            for msg in conversation_history.split("\n"):
                if msg.startswith("User:"):
                    messages.append({"role": "user", "content": msg[5:].strip()})
                elif msg.startswith("Assistant:"):
                    messages.append({"role": "assistant", "content": msg[10:].strip()})
            
            # Add the current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        # Simulate Claude response for demo
        return f"[CLAUDE-{model}] You said: {message}"

def generate_quick_replies(conversation_context):
    """
    Generate contextual quick replies based on the current conversation
    """
    if not conversation_context:
        # Initial quick replies for new chat
        return [
            "Tell me about YellowChat",
            "How can you help me?",
            "What can you do?"
        ]
    
    try:
        # Construct a prompt that generates contextual quick replies
        prompt = f"""Based on this conversation, generate 3 likely follow-up messages or questions the user might want to ask. 
        Make them specific to the context and natural to the flow of conversation.
        
        Conversation:
        {conversation_context}
        
        Generate 3 short, specific quick replies that would be natural for the user to say next.
        Consider:
        - Questions that would clarify or expand on the last response
        - Natural follow-up requests
        - Specific actions the user might want to take
        
        Format each reply to be concise (max 6-8 words) and conversational.
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that generates relevant, contextual quick reply suggestions for a chat interface."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        suggestions = response.choices[0].message.content.strip().split("\n")
        return [s.strip().strip('123.-*') for s in suggestions if s.strip()][:3]
        
    except Exception as e:
        return [
            "Could you explain that further?",
            "Tell me more",
            "What are my options?"
        ]

# ----------------------------
# Initialize Session State
# ----------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "quick_replies" not in st.session_state:
    st.session_state.quick_replies = generate_quick_replies("")
if "input_message" not in st.session_state:
    st.session_state.input_message = ""
if "api_provider" not in st.session_state:
    st.session_state.api_provider = "gpt"
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List to store multiple conversations

# ----------------------------
# Sidebar: Chat History & Settings
# ----------------------------

with st.sidebar:
    st.title("YellowChat")
    st.markdown("---")
    
    st.subheader("Settings")
    api_provider = st.selectbox(
        "Select AI Provider",
        options=["gpt", "claude"],
        index=0,
        help="Choose between OpenAI's GPT or Anthropic's Claude"
    )
    st.session_state.api_provider = api_provider

    model_options = {
        "gpt": ["gpt-3.5-turbo", "gpt-4"],
        "claude": ["claude-v1", "claude-plus"]
    }
    model = st.selectbox(
        "Select Model",
        options=model_options[api_provider],
        help="Choose the AI model to power your chat"
    )
    st.session_state.model = model
    
    st.markdown("---")
    st.subheader("Chat History")
    
    # Save current conversation if it's not empty
    if len(st.session_state.conversation) > 0:
        current_chat = {
            "messages": st.session_state.conversation,
            "timestamp": st.session_state.get("current_timestamp", "Untitled Chat")
        }
        if current_chat not in st.session_state.chat_history:
            st.session_state.chat_history.append(current_chat)
    
    # Display chat history
    for idx, chat in enumerate(st.session_state.chat_history):
        if st.button(f"Chat {idx + 1}: {chat['timestamp']}", key=f"history_{idx}", use_container_width=True):
            st.session_state.conversation = chat["messages"]
            st.session_state.quick_replies = generate_quick_replies("\n".join(
                [f"{msg['sender'].capitalize()}: {msg['text']}" for msg in chat["messages"]]
            ))
            st.rerun()
    
    if st.button("New Chat", use_container_width=True):
        st.session_state.conversation = []
        st.session_state.quick_replies = generate_quick_replies("")
        st.session_state.input_message = ""
        st.session_state.current_timestamp = "New Chat"
        st.rerun()

# ----------------------------
# Main Chat Area
# ----------------------------

st.markdown(
    """
    <style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e6f3ff;
        border-left: 5px solid #2b6cb0;
    }
    .assistant-message {
        background-color: #f0f0f0;
        border-left: 5px solid #718096;
    }
    .quick-reply-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .stButton > button {
        background-color: #2b6cb0;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #2c5282;
        transform: translateY(-1px);
    }
    .input-container {
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        border-radius: 0.5rem;
    }
    /* Hide 'Press Enter to apply' text */
    .st-emotion-cache-1gulkj5 {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Chat Container
chat_container = st.container()
with chat_container:
    for msg in st.session_state.conversation:
        if msg["sender"] == "user":
            st.markdown(
                f"""<div class='chat-message user-message'>
                    <div><b>You:</b></div>
                    <div>{msg['text']}</div>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""<div class='chat-message assistant-message'>
                    <div><b>Assistant:</b></div>
                    <div>{msg['text']}</div>
                </div>""",
                unsafe_allow_html=True
            )

# Quick Replies (shown before user input)
if st.session_state.quick_replies:
    quick_reply_cols = st.columns(3)
    for idx, reply in enumerate(st.session_state.quick_replies):
        if quick_reply_cols[idx].button(
            reply,
            key=f"quick_reply_{idx}",
            use_container_width=True
        ):
            # Process the quick reply as user input
            st.session_state.conversation.append({"sender": "user", "text": reply})
            conversation_context = "\n".join(
                [f"{msg['sender'].capitalize()}: {msg['text']}" for msg in st.session_state.conversation]
            )
            
            # Get bot response
            bot_response = get_chat_response(
                message=reply,
                conversation_history=conversation_context,
                api_provider=st.session_state.api_provider,
                model=st.session_state.model
            )
            st.session_state.conversation.append({"sender": "assistant", "text": bot_response})
            
            # Generate new quick replies based on the updated conversation
            st.session_state.quick_replies = generate_quick_replies(conversation_context)
            
            # Clear both the session state and input message
            st.session_state.input_message = ""
            st.rerun()

# Input Area with improved styling
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
cols = st.columns([5, 1])
with cols[0]:
    # Use an empty default value and get the current input from session state
    input_message = st.text_input(
        "Your message",
        value="",  # Set empty default value
        key=f"input_message_field_{st.session_state.get('input_counter', 0)}",  # Dynamic key to force refresh
        placeholder="Type your message here or select a suggestion above...",
        label_visibility="collapsed",
        on_change=lambda: handle_message(st.session_state[f"input_message_field_{st.session_state.get('input_counter', 0)}"]) if st.session_state[f"input_message_field_{st.session_state.get('input_counter', 0)}"].strip() else None
    )
with cols[1]:
    send_button = st.button("Send", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Initialize input counter if not exists
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

def handle_message(message):
    if message.strip():
        # Add user message to conversation
        st.session_state.conversation.append({"sender": "user", "text": message})
        
        # Build conversation context
        conversation_context = "\n".join(
            [f"{msg['sender'].capitalize()}: {msg['text']}" for msg in st.session_state.conversation]
        )
        
        # Get bot response
        bot_response = get_chat_response(
            message=message,
            conversation_history=conversation_context,
            api_provider=st.session_state.api_provider,
            model=st.session_state.model
        )
        st.session_state.conversation.append({"sender": "assistant", "text": bot_response})
        
        # Generate new quick replies
        st.session_state.quick_replies = generate_quick_replies(conversation_context)
        
        # Increment the counter to force a new text input widget
        st.session_state.input_counter += 1
        
        # Rerun the app
        st.rerun()

# Handle manual message input from send button
if send_button and input_message.strip():
    handle_message(input_message)
