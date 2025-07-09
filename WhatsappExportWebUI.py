import re
import streamlit as st
import pandas as pd
import hashlib
import colorsys

# --- Page Configuration ---
st.set_page_config(page_title="WhatsApp Chat Reader", page_icon="📱", layout="wide")

# Function to generate a consistent color from a string
def get_color_from_name(name):
    # Use SHA256 hash to get a consistent number from the name
    hash_object = hashlib.sha256(name.encode())
    hex_dig = hash_object.hexdigest()
    # Take the first few characters of the hash to generate a hue
    hue = int(hex_dig[:6], 16) % 360

    # Convert HSL to RGB. Fixed saturation and lightness for good contrast on dark background.
    # Saturation (S) around 0.7-0.9, Lightness (L) around 0.5-0.7 for vibrant but not too bright colors.
    rgb = colorsys.hls_to_rgb(hue / 360, 0.6, 0.8)
    # Convert RGB to hex
    return '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

# --- Custom CSS for a better UI ---
st.markdown("""
<style>
    /* General body styling */
    body {
        background-color: #0E1117 !important; /* Dark background */
        color: #FAFAFA !important; /* Light text */
    }
    .stApp {
        background-color: #0E1117 !important; /* Dark background */
        background-image: url("https://www.transparenttextures.com/patterns/dark-mosaic.png"); /* Dark WhatsApp-like background */
        background-repeat: repeat;
        color: #FAFAFA !important; /* Light text */
    }

    /* Chat bubble styling */
    .chat-bubble {
        border-radius: 12px;
        padding: 8px 12px;
        margin-bottom: 8px;
        max-width: 75%;
        word-wrap: break-word;
        display: inline-block;
        color: #0E1117 !important; /* Dark text for chat bubbles */
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
        color: #FAFAFA !important; /* Light text for sender name */
    }

    /* Headings and Titles */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stTitle"],
    [data-testid="stHeader"] {
        color: #262730 !important; /* Dark text for headings and titles */
    }

</style>
""", unsafe_allow_html=True)

# Function to parse WhatsApp chat data
def parse_chat(file_content):
    chat_data = []
    for line in file_content.splitlines():
        # Regex to capture timestamp, sender, and message
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}) - ([^:]+): (.*)', line)
        if match:
            timestamp, sender, message = match.groups()
            chat_data.append({'timestamp': timestamp.strip(), 'sender': sender.strip(), 'message': message.strip()})
    return chat_data

# --- Main Application ---
st.title("WhatsApp Chat Viewer")

uploaded_file = st.file_uploader("Upload your WhatsApp chat export file", type=["txt"])

if uploaded_file is not None:
    file_contents = uploaded_file.getvalue().decode("utf-8")
    chat_data = parse_chat(file_contents)

    if chat_data:
        chat_df = pd.DataFrame(chat_data)

        # Generate colors for each sender
        sender_colors = {sender: get_color_from_name(sender) for sender in chat_df['sender'].unique()}

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
            current_sender_color = sender_colors[row['sender']]

            if is_user:
                st.markdown(
                    f"""
                    <div class="user-message-container">
                        <div class="chat-bubble" style="background-color: {current_sender_color};">
                            <div class="sender-name">{row['sender']}</div>
                            {row['message']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""
                    <div class="sender-message-container">
                        <div class="chat-bubble" style="background-color: {current_sender_color};">
                            <div class="sender-name">{row['sender']}</div>
                            {row['message']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Could not parse chat data from the uploaded file. Please ensure it's a valid WhatsApp chat export.")
else:
    st.info("Please upload a WhatsApp chat export file to view the conversation.")
