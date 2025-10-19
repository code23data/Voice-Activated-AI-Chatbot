# Voice Activated AI Chatbot
## Overview
This is a Python-based voice assistant that processes voice commands to perform tasks such as opening websites, searching Wikipedia, managing notes and to-do lists, and controlling system functions like shutdown, restart, and lock. It uses speech recognition and text-to-speech functionalities.

## Features
- Open Google and YouTube
- Search Wikipedia for a topic
- Open a specified website
- Display current time
- Manage notes (add, view, remove)
- Manage to-do lists (add, view, mark as done)
- System controls: shutdown, restart, lock screen
- Help command to list available commands

## Requirements
- Python 3.x
- Libraries:
  - `speech_recognition`
  - `wikipedia`
  - `wikipedia-api`
  - `pyttsx3`
  - `webbrowser`
  - `platform`
  - `subprocess`
  - `json`
  - `datetime`
  - `os`
- A working microphone for voice input.


## Installation
1. Clone or download the repository.
2. Install required libraries:
     ```bash
     pip install -r requirements.txt
     ```
3. On Linux, for the lock command, ensure gnome-screensaver is installed (for GNOME-based systems).

## Usage
1. Run the scirpt:
     ```bash
     python main.py
     ```
2. The assistant will greet you and list available commands.
3. Speak a command (e.g., "open Google", "search Wikipedia for Python", "add note").
4. Say "stop", "quit", or "exit" to end the program.

## File Structure
- `voice_assistant.py`: Main script containing the voice assistant logic.
- `notes.json`: Stores notes data.
- `todos.json`: Stores to-do list data.

## Notes
- Notes and to-do lists are saved to notes.json and todos.json files.
- System control commands (shutdown, restart, lock) require appropriate permissions.
- The assistant uses Google Speech Recognition for voice input, requiring an internet connection.

## Limitations
- Speech recognition may fail in noisy environments or with unclear speech.
- Some system commands may not work on unsupported operating systems.

## Troubleshooting
- **Speech recognition errors**: Ensure a stable internet connection and clear speech. Adjust the microphone or ambient noise settings if needed.
- **System command issues**: Verify that your operating system supports the commands and you have sufficient permissions.

## License
This project is unlicensed and provided as-is for educational purposes.
