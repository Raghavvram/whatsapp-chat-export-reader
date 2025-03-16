
import re
import streamlit as st
import pandas as pd

# Function to parse WhatsApp chat data
def parse_chat(file_path):
    chat_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'(\d+/\d+/\d+, \d+:\d+) - (.+?): (.+)', line)
            if match:
                timestamp, sender, message = match.groups()
                chat_data.append({'timestamp': timestamp, 'sender': sender, 'message': message})
    return chat_data

# Parse and load chat data
chat_data = parse_chat('whatsapp.txt')
chat_df = pd.DataFrame(chat_data)

# Streamlit interface
st.title("WhatsApp Chat Viewer")

# Sidebar to filter by sender
senders = chat_df['sender'].unique()
selected_sender = st.sidebar.selectbox("Filter by Sender", ["All"] + list(senders))

# Filter chat data based on the selected sender
if selected_sender != "All":
    filtered_data = chat_df[chat_df['sender'] == selected_sender]
else:
    filtered_data = chat_df

# Function to display chat bubbles with text alignment for sender
def display_message_bubble(sender, message):
    if sender == "You":  # Sent messages aligned right
        st.markdown(
            f"""
            <div style='background-color: #1f8a70; color: white; border-radius: 15px; padding: 10px; margin: 10px; 
                        text-align: right; align-self: flex-end; max-width: 70%;'>
                <span style='text-align: right; font-size: 14px; font-family: Arial, sans-serif;'>{message}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:  # Received messages aligned left
        st.markdown(
            f"""
            <div style='background-color: #35477d; color: white; border-radius: 15px; padding: 10px; margin: 10px; 
                        text-align: left; align-self: flex-start; max-width: 70%;'>
                <strong style='font-size: 14px; font-family: Arial, sans-serif;'>{sender}:</strong>
                <span style='text-align: left; font-size: 14px; font-family: Arial, sans-serif;'>{message}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# Display chat data with styled bubbles
for index, row in filtered_data.iterrows():
    display_message_bubble(row['sender'], row['message'])


