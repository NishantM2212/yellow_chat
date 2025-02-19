import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure Streamlit theme
st.set_page_config(
    page_title="MiaChat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --background-color: #1E1E1E;
        --secondary-bg: #2D2D2D;
        --text-color: #E0E0E0;
        --yellow-brand: #FFD700;
        --accent-color: #4A4A4A;
        --success-color: #4CAF50;
        --error-color: #FF5252;
    }

    /* Global styles */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        padding: 2rem;
    }

    .stApp {
        background-color: var(--background-color);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--secondary-bg);
    }

    .sidebar .sidebar-content {
        background-color: var(--secondary-bg);
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--yellow-brand) !important;
        font-weight: 600;
    }

    /* Text areas */
    .stTextArea textarea {
        background-color: var(--secondary-bg);
        color: var(--text-color);
        border: 1px solid var(--accent-color);
        border-radius: 5px;
    }

    .stTextArea textarea:focus {
        border-color: var(--yellow-brand);
        box-shadow: 0 0 0 1px var(--yellow-brand);
    }

    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background-color: #000000;
        border-left: 5px solid var(--yellow-brand);
        color: #000000;
    }

    .user-message {
        background-color: #FFFFFF;
        border-left: 5px solid var(--yellow-brand);
        color: #000000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .assistant-message {
        background-color: #F5F5F5;
        border-left: 5px solid #FFB700;
        color: #000000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Message headers */
    .chat-message b {
        color: #000000;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: block;
        font-weight: 600;
    }

    /* Message content */
    .chat-message div:last-child {
        margin-top: 0.5rem;
        line-height: 1.5;
        color: #000000;
    }

    /* Buttons */
    .stButton button {
        background-color: var(--yellow-brand);
        color: #000000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #FFE44D;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.2);
    }

    /* Quick replies */
    .quick-reply-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .quick-reply {
        background-color: var(--secondary-bg);
        color: var(--yellow-brand);
        border: 1px solid var(--yellow-brand);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .quick-reply:hover {
        background-color: var(--yellow-brand);
        color: var(--background-color);
    }

    /* Input container */
    .input-container {
        background-color: var(--secondary-bg);
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }

    /* Selectbox */
    .stSelectbox {
        background-color: var(--secondary-bg);
    }

    .stSelectbox > div > div {
        background-color: var(--secondary-bg);
        color: var(--text-color);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--secondary-bg);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-color);
    }

    .stTabs [aria-selected="true"] {
        color: var(--yellow-brand);
    }

    /* Status messages */
    .success-message {
        color: var(--success-color);
        background-color: rgba(76, 175, 80, 0.1);
        padding: 0.5rem;
        border-radius: 4px;
    }

    .error-message {
        color: var(--error-color);
        background-color: rgba(255, 82, 82, 0.1);
        padding: 0.5rem;
        border-radius: 4px;
    }

    /* Input area */
    .stTextInput input {
        color: #000000;
        background-color: #FFFFFF;
        border: 1px solid var(--yellow-brand);
    }

    .stTextInput input:focus {
        border-color: var(--yellow-brand);
        box-shadow: 0 0 0 1px var(--yellow-brand);
    }

    /* Title styling */
    .title {
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        color: var(--yellow-brand);
        text-align: center;
        margin-bottom: 2rem;
    }

    .mia-branding {
        font-size: 2.5rem;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Yellow.ai Platform Configuration
YELLOW_AI_CONFIG = {
    "channels": [
        "WhatsApp",
        "Facebook Messenger",
        "Instagram",
        "Web Chat",
        "IVR",
        "SMS"
    ],
    "features": {
        "customer_support": {
            "name": "Customer Support Automation",
            "description": "AI-driven customer support with intelligent routing"
        },
        "sales_automation": {
            "name": "Sales Automation",
            "description": "Lead generation and sales process automation"
        },
        "hr_automation": {
            "name": "HR Process Automation",
            "description": "Streamline HR workflows and employee engagement"
        },
        "demo_booking": {
            "name": "Demo Booking",
            "description": "Schedule product demonstrations and sales calls"
        }
    },
    "integrations": {
        "crm": ["Salesforce", "HubSpot"],
        "erp": ["SAP", "Oracle"],
        "ticketing": ["Zendesk", "Freshdesk"],
        "communication": ["Twilio", "MessageBird"]
    }
}

# System Prompt
YELLOW_AI_PROMPT = """You are MiaChat, an AI assistant specifically trained for Yellow.ai platform support.

Key Capabilities:
1. Provide comprehensive information about Yellow.ai's products and services
2. Guide users through Yellow.ai's features and capabilities:
   - Conversational AI Bots
   - Omnichannel Support
   - Orch LLM (Proprietary orchestration engine)
   - Customer Experience Automation
   - Live Agent Handoff
   - AI-Powered Analytics
   - Enterprise System Integrations
   - Generative AI Capabilities

3. Assist with demo booking and platform inquiries
4. Explain technical concepts in an accessible manner
5. Provide integration guidance
6. Share analytics and reporting capabilities

Guidelines:
- Maintain a professional and helpful tone
- Provide accurate platform information
- Guide users through demo booking process
- Explain technical features clearly
- Handle complex queries with detailed responses
- Facilitate smooth handoffs when needed

Remember: You are Mia, an expert in Yellow.ai's platform and should focus on helping users understand and utilize its capabilities effectively. Always introduce yourself as Mia and maintain a friendly, professional demeanor."""

# ----------------------------
# Helper Functions
# ----------------------------

def get_chat_response(message, conversation_history, api_provider, model):
    """
    Get response from OpenAI API or Claude API with Yellow.ai context
    """
    if api_provider == "gpt":
        try:
            messages = [{"role": "system", "content": YELLOW_AI_PROMPT}]
            
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
    Generate contextual quick replies based on Yellow.ai platform features in first person
    """
    if not conversation_context:
        # Initial quick replies for new chat in first person
        return [
            "Hi Mia, tell me about Yellow.ai",
            "I'd like to book a demo with you",
            "Can you show me the integration options?"
        ]
    
    try:
        # Construct a prompt that generates first-person quick replies for Yellow.ai
        prompt = f"""Based on this conversation about Yellow.ai platform, generate 3 likely follow-up questions or actions from the user's perspective in first person (using I, my, me).
        The assistant's name is Mia, so include personal addressing where appropriate.

        Focus on Yellow.ai's key features:
        - Conversational AI capabilities
        - Omnichannel support
        - Integration options
        - Demo booking
        - Platform features
        
        Current Conversation:
        {conversation_context}
        
        Generate 3 short, specific quick replies in first person that a user would naturally say. Examples:
        - "Mia, can you tell me more about..."
        - "I'd like your help with..."
        - "Could you explain to me..."
        - "Show me how to..."
        - "Help me understand..."
        
        Make responses conversational and personal, addressing Mia directly where appropriate.
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that generates first-person quick reply suggestions from the user's perspective, addressing the AI assistant named Mia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        suggestions = response.choices[0].message.content.strip().split("\n")
        return [s.strip().strip('123.-*') for s in suggestions if s.strip()][:3]
        
    except Exception as e:
        return [
            "Mia, tell me more about the features",
            "Help me set up integrations",
            "I'd like to schedule a demo"
        ]

def handle_demo_booking(user_info):
    """
    Handle Yellow.ai platform demo booking requests
    """
    try:
        # In a real implementation, this would integrate with Yellow.ai's booking system
        return {
            "status": "success",
            "message": "Thank you for your interest in Yellow.ai! Your demo request has been received.",
            "next_steps": [
                "Our team will contact you shortly to schedule the demo",
                "You'll receive an email confirmation",
                "Feel free to ask any questions about Yellow.ai while you wait"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error booking demo: {str(e)}",
            "next_steps": [
                "Please try again later",
                "Contact our support team for assistance"
            ]
        }

def get_integration_info(integration_type):
    """
    Provide information about Yellow.ai's integration capabilities
    """
    return YELLOW_AI_CONFIG["integrations"].get(integration_type, [])

def get_feature_info(feature_name):
    """
    Get detailed information about Yellow.ai platform features
    """
    return YELLOW_AI_CONFIG["features"].get(feature_name, {
        "name": "Feature not found",
        "description": "Information not available"
    })

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
    st.session_state.chat_history = []
if "demo_requests" not in st.session_state:
    st.session_state.demo_requests = []

# ----------------------------
# Sidebar: Chat History & Settings
# ----------------------------

with st.sidebar:
    st.markdown('<h1 class="title mia-branding">MiaChat</h1>', unsafe_allow_html=True)
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
