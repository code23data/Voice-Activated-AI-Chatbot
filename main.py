import speech_recognition as sr # For recognizing voice as commands
import wikipediaapi # For interacting with Wikipedia API
import wikipedia # For interacting with Wikipedia website
import webbrowser # For opening website URLs
import pyttsx3 # For text-to-speech functionality
import datetime as dt # For getting date and time
import os # For interacting with the operating system (e.g., shutdown)
import platform # For interacting with the operating system (e.g., shutdown)
import subprocess # For interacting with the operating system (e.g., shutdown)
import json  # For saving/loading notes & todos

engine = pyttsx3.init()

r = sr.Recognizer()

# File paths for saving data
NOTES_FILE = "notes.json"
TODOS_FILE = "todos.json"

# Global data storage
notes = {}
todos = {}

def load_data():
    """Load saved notes and todos from files"""
    global notes, todos
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, 'r') as f:
                notes = json.load(f)
        if os.path.exists(TODOS_FILE):
            with open(TODOS_FILE, 'r') as f:
                todos = json.load(f)
    except:
        notes = {}
        todos = {}

def save_data():
    """Save notes and todos to files"""
    try:
        with open(NOTES_FILE, 'w') as f:
            json.dump(notes, f)
        with open(TODOS_FILE, 'w') as f:
            json.dump(todos, f)
    except Exception as e:
        print(f"Save error: {e}")

# Function to handle and process user commands
def takeCommand():
    """
        This function takes the user's speech from microphone
        as input, and transcribes it in text format.
    """
    # Capture audio input from microphone
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,  duration=1)  # Automatically adjust for ambient noise
        print("Say Something!")
        audio_data = r.listen(source, timeout=5, phrase_time_limit=10)

    # Recognizing speech
    try:
        text = r.recognize_google(audio_data, language='en-in')
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak(audio):
    """
        This function takes text and speaks it.
    """
    print(audio)
    engine.say(audio)
    engine.runAndWait()  # Speaks the queued audio and waits until it's finished

def wishMe():
    """
        This function greets the user based on the time of the day.
        It greets either good morning, good afternoon, or good evening
        based on the time of the day.
    """
    currentTime = dt.datetime.now()
    print(f"The current time is: {currentTime}")
    if currentTime.hour < 12:
        speak("Good Morning!")
    elif currentTime.hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

def speak_help():
    """List all available commands"""
    speak("Here are all my commands:")
    print("Open Google, Open YouTube")
    print("Open website [name]")
    print("Search Wikipedia for [topic]")
    print("What time is it")
    print("Add note, View notes, Remove note")
    print("Add todo, View todos, Mark done")
    print("Shutdown, Restart, Lock")
    print("Hello, Help, Stop")

def openGoogle():
    """Opens Google website on device's web browser"""
    speak("Opening Google ...")
    webbrowser.open("https://www.google.com")

def openYouTube():
    """Opens YouTube website on device's web browser"""
    speak("Opening YouTube ...")
    webbrowser.open("https://www.youtube.com")

def searchWikipedia(text):
    "Searches Wikipedia and returns a summary of the web page searched."""
    print(f"Searching Wikipedia for: {text}")  # Debug print
    try:
        summary = wikipedia.summary(text, sentences=5)
        speak("According to Wikipedia:")
        speak(summary)
    except wikipedia.exceptions.WikipediaException as e:
        speak(f"Did not get what to search for: {e}")
    except Exception as e:
        speak(f"Did not get any results for {text} from Wikipedia")

def sayTime():
    """This function prints and says the current time"""
    strTime = dt.datetime.now().strftime("%I:%M %p") # e.g. "05:30 PM"
    speak(f"The time is {strTime}")

def openWebsite(website):
    """Opens website mentioned by user on the device web browser"""
    speak(f"Opening website {website} ...")
    website = website.lower().strip()
    if 'wikipedia' in website:
        webbrowser.open("https://www.wikipedia.org")
    else:
        try:
            webbrowser.open(f"https://{website}.com")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")


def shutdown():
    """Asks user for confirmation and then shuts down the device."""
    speak("Are you sure you want to shut down? (Say yes or no)")
    command = takeCommand().lower()
    if 'yes' in command:
        if platform.system() == "Windows":
            subprocess.run(["shutdown", "/s", "/t", "0"])  # Shutdown immediately
        elif platform.system() == "Darwin":
            subprocess.run(["sudo", "shutdown", "-h", "now"])  # Shutdown immediately
        elif platform.system() == "Linux":
            subprocess.run(["sudo", "shutdown", "now"])  # Shutdown immediately
        else:
            speak("Sorry, looks like I cannot shutdown your device because of your operating system.")


def restart():
    """Asks  user for confirmation and then restarts the device."""
    speak("Are you sure you want to restart? (Say yes or no)")
    command = takeCommand().lower()
    if 'yes' in command:
        if platform.system() == "Windows":
            subprocess.run(["shutdown", "/r", "/t", "0"])  # Restart immediately
        elif platform.system() == "Darwin":
            subprocess.run(["sudo", "shutdown", "-r", "now"])  # Restart immediately
        elif platform.system() == "Linux":
            subprocess.run(["sudo", "reboot"])  # Restart immediately
        else:
            speak("Sorry, looks like I cannot restart your device because of your operating system.")

def lock():
    """Asks user for confirmation and then locks the device."""
    speak("Are you sure you want to lock the screen? (Say yes or no)")
    command = takeCommand().lower()
    if 'yes' in command:
        try:
            if platform.system() == "Windows":
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])  # Lock screen on Windows
            elif platform.system() == "Darwin":
                subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])  # Lock screen on macOS
            elif platform.system() == "Linux":
                subprocess.run(["gnome-screensaver-command", "-l"])  # Lock screen on Linux (Gnome)
            else:
                speak("Sorry, looks like I cannot lock your screen because of your operating system.")
        except Exception as e:
            speak(f"Sorry, could not lock your screen due to the following error: {str(e)}")

# For Managing Notes

def addNote():
    """Allows user to add a note."""
    speak("What would you like to add to your note?")
    note_content = takeCommand()
    if note_content:
        note_name = f"note {len(notes) + 1}"
        notes[note_name] = note_content
        save_data()
        speak(f"Note added: {note_name} with content: {note_content}")
    else:
        speak("Sorry, I didn't get that. Please try again.")

def viewNotes():
    """Displays all notes."""
    if notes:
        speak("Here are your notes:")
        for note_name, note_content in notes.items():
            speak(f"{note_name}: {note_content}")
    else:
        speak("You don't have any notes yet.")

def removeNote():
    """Removes a note by name."""
    speak("Which note would you like to remove? Say 'all' to remove all notes.")
    note_to_remove = takeCommand().lower().strip()
    if 'all' in note_to_remove:
        # removeAllNotes()
        global notes
        notes.clear()
        save_data()
        speak("All notes removed")
    else:
        if note_to_remove in notes:
            del notes[note_to_remove]
            speak(f"Note {note_to_remove} has been removed.")
        else:
            speak(f"No note found with the name {note_to_remove}.")

# For Managing To-Do Lists

def addTodo():
    """Allows user to add a to-do task."""
    speak("What is your to-do task?")
    task_content = takeCommand()
    if task_content:
        task_name = f"task {len(todos) + 1}"
        todos[task_name] = {"task": task_content, "status": "Not Done"}
        speak(f"To-Do added: {task_name} with task: {task_content}")
    else:
        speak("Sorry, I didn't get that. Please try again.")

def viewTodos():
    """Displays all to-do tasks."""
    if todos:
        speak("Here are your to-do tasks:")
        for task_name, task_info in todos.items():
            speak(f"{task_name}: {task_info['task']} - Status: {task_info['status']}")
    else:
        speak("You don't have any to-do tasks yet.")

def markTodoDone():
    """Marks a to-do task as done."""
    speak("Which task would you like to mark as done?")
    task_to_mark = takeCommand().lower()
    for task_name in todos:
        if task_to_mark in task_name or task_to_mark in todos[task_name]['task'].lower():
            todos[task_name]['status'] = 'Done'
            save_data()
            speak(f"Marked {task_name} as done!")
            return
    speak("Task not found.")

# Running the chatbot as a script
if __name__ == "__main__":
    load_data() # Load saved data
    wishMe()
    speak_help()
    speak("Speak your command, or say 'stop', or 'quit', or 'exit' to end the program")
    while True:
        try:
            command = takeCommand().lower()

            if not command:
                    continue

            if 'google' in command:
                openGoogle()
            elif 'youtube' in command:
                openYouTube()
            elif 'search wikipedia' in command:
                searchWikipedia(command.replace("search wikipedia for ", "").strip())
            elif 'open website' in command:
                try:
                    openWebsite(command.replace("open website", "").strip())
                except Exception as e:
                    speak("Please try again ...")
                    continue
            elif "the time" in command or 'time' in command:
                sayTime()
            elif 'hello' in command:
                speak("Hello. Hope you are doing well. How can I help you?\n\nGive commands such as 'open Google', 'open YouTube', or 'search Wikipedia for <topic>'")
            elif 'shutdown' in command:
                    shutdown()
            elif 'restart' in command:
                restart()
            elif 'lock' in command:
                lock()
            elif 'add note' in command:
                addNote()
            elif 'view notes' in command:
                viewNotes()
            elif 'remove note' in command:
                removeNote()
            elif 'add to do' in command:
                addTodo()
            elif 'view to dos' in command or 'view to do' in command:
                viewTodos()
            elif 'mark done' in command:
                markTodoDone()
            elif 'exit' in command or 'quit' in command or 'stop' in command:
                speak("Goodbye!")
                break
            elif 'help' in command:
                speak_help()
            else:
                speak("Not a valid command. Try again.")
        except KeyboardInterrupt:
            speak("Goodbye!")
            save_data()
            break
        except Exception as e:
            speak("Something went wrong. Try again.")
            print(f"Error: {e}")
