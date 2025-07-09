import re
import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="WhatsApp Chat Reader", page_icon="📱", layout="wide")

# --- Custom CSS for a better UI ---
st.markdown("""
<style>
    /* General body styling */
    body {
        background-color: #f0f2f5; /* A light grey background */
    }
    .stApp {
        background-color: #e5ddd5; /* WhatsApp-like background */
        background-image: url("https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png");
        background-repeat: repeat;
    }

    /* Chat bubble styling */
    .chat-bubble {
        border-radius: 12px;
        padding: 8px 12px;
        margin-bottom: 8px;
        max-width: 75%;
        word-wrap: break-word;
        display: inline-block;
    }

    /* User's message bubble */
    .user-bubble {
        background-color: #dcf8c6; /* Light green */
        color: #303030;
        text-align: left;
    }

    /* Other sender's message bubble */
    .sender-bubble {
        background-color: #ffffff; /* White */
        color: #303030;
        text-align: left;
    }

    /* Message container alignment */
    .user-message-container {
        display: flex;
        justify-content: flex-end;
    }

    .sender-message-container {
        display: flex;
        justify-content: flex-start;
    }
    
    .sender-name {
        font-weight: bold;
        margin-bottom: 4px;
        color: #027f6e; /* A teal color for sender name */
    }

</style>
""", unsafe_allow_html=True)

# Function to parse WhatsApp chat data
def parse_chat(file_path):
    chat_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Regex to capture timestamp, sender, and message
                match = re.match(r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}) - ([^:]+): (.*)', line)
                if match:
                    timestamp, sender, message = match.groups()
                    chat_data.append({'timestamp': timestamp.strip(), 'sender': sender.strip(), 'message': message.strip()})
    except FileNotFoundError:
        st.error(f"Error: The chat file '{file_path}' was not found. Please make sure it's in the same directory as the script.")
        return None
    return chat_data

# --- Main Application ---
st.title("WhatsApp Chat Viewer")

# Load chat data
chat_data = parse_chat('whatsapp.txt')

if chat_data:
    chat_df = pd.DataFrame(chat_data)

    # --- Sidebar for Filtering ---
    st.sidebar.title("Options")
    senders = sorted(chat_df['sender'].unique())
    
    # Let user identify themselves. Default to "You" if present, otherwise the first sender.
    user_identity = "You" if "You" in senders else senders[0]
    user_sender = st.sidebar.selectbox("Who are you in this chat?", senders, index=senders.index(user_identity))

    # Filter by sender
    selected_sender = st.sidebar.selectbox("Filter by Sender", ["All"] + list(senders))

    if selected_sender != "All":
        filtered_data = chat_df[chat_df['sender'] == selected_sender]
    else:
        filtered_data = chat_df

    # --- Display Chat Messages ---
    st.header("Chat Conversation")
    st.markdown("---")

    for _, row in filtered_data.iterrows():
        is_user = row['sender'] == user_sender

        if is_user:
            st.markdown(
                f"""
                <div class="user-message-container">
                    <div class="chat-bubble user-bubble">
                        {row['message']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div class="sender-message-container">
                    <div class="chat-bubble sender-bubble">
                        <div class="sender-name">{row['sender']}</div>
                        {row['message']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("Could not load chat data. Please check the file 'whatsapp.txt'.")
