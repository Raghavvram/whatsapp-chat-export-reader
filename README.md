# WhatsApp Chat Export Reader

A Streamlit-based UI to read and view WhatsApp chat exports in a WhatsApp-like interface.

## Features

*   View WhatsApp chat conversations.
*   Filter messages by sender.
*   Customizable dark theme.
*   Unique chat bubble colors for each participant.

## Setup and Installation

This project uses `uv` for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/whatsapp-chat-export-reader.git
    cd whatsapp-chat-export-reader
    ```

2.  **Install `uv` (if you don't have it):**
    ```bash
    pip install uv
    ```
    Or refer to the official `uv` documentation for installation.

3.  **Create a virtual environment and install dependencies:**
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**
    ```bash
    uv run streamlit run WhatsappExportWebUI.py
    ```

    This will open the application in your web browser.

2.  **Upload your WhatsApp chat export file:**
    *   Export your WhatsApp chat (without media) to a `.txt` file.
    *   In the Streamlit application, use the file uploader to select your exported `.txt` file. The file can have any name.

## Customization

*   **Theme:** The application is configured with a dark theme by default. All theme settings are hardcoded within `WhatsappExportWebUI.py`.
*   **Chat Bubble Colors:** Each sender's chat bubble will have a unique, consistently generated color.
*   **Background Image:** The WhatsApp-like background image can be changed by modifying the `background-image` URL in the CSS section of `WhatsappExportWebUI.py`.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests.

## License

[Specify your license here, e.g., MIT License]