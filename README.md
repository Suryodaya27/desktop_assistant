# Desktop Assistant

This is a desktop assistant application that performs various tasks based on user commands.

## Usage

### Activation
- **Command**: Activate
- **Function**: Activates the assistant

### Open Applications
- **Command**: Open [Application]
  - **Functions**:
    - Open Youtube
    - Open Code
    - Open Google
    - Open WhatsApp

### Task Management
- **Command**: Add task [TASK]
  - **Function**: Adds a task to the to-do list
- **Command**: Show todo list
  - **Function**: Displays the to-do list
- **Command**: Remove task [TASK_ID]
  - **Function**: Removes a task from the to-do list

### News
- **Command**: Show recent news
  - **Function**: Displays recent news

### Messaging
- **Command**: Open whatsapp message of [CONTACT_NAME]
  - **Function**: Opens the chat with the specified contact in WhatsApp
- **Command**: Send whatsapp message to [CONTACT_NAME] that [MESSAGE]
  - **Function**: Sends a message to the specified contact in WhatsApp

### Reminder
- **Command**: Set reminder [TIME] [DATE] on [MESSAGE]
  - **Function**: Sets a reminder for the specified time and date with the given message
- **Command**: Show reminder
  - **Function**: Displays the list of reminders
- **Command**: Delete reminder [REMINDER_ID]
  - **Function**: Deletes the specified reminder

### Web Search
- **Command**: Web search [QUESTION]
  - **Function**: Performs a web search for the given question

### Text and Image Processing
- **Command**: Summarize text
  - **Function**: Summarizes text
- **Command**: Explain image
  - **Function**: Explains the contents of an image
- **Command**: Solve
  - **Function**: Solves a problem based on an image

## Dependencies

- Python 3.x
- Additional libraries as required (e.g., SpeechRecognition, pyttsx3, requests, etc.)

## Installation

1. Clone the repository:
2. Create Google api key and store in .env file
3. Install Dependencies
4. Run python app.py
