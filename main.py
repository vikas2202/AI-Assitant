import openai
import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import subprocess
import os
import smtplib
import requests
from email.message import EmailMessage
from tkinter import filedialog

# Set up OpenAI API key
openai.api_key = "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"  # Replace with your OpenAI API key

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Capture voice input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("I'm listening.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language="en-in")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Network error. Please try again.")
            return None

def play_music():
    """Play music from a selected directory."""
    speak("Please select a folder containing your music files.")
    folder_path = filedialog.askdirectory(title="Select Music Folder")
    if folder_path:
        music_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav'))]
        if music_files:
            speak("Playing music from your folder.")
            for music in music_files:
                file_path = os.path.join(folder_path, music)
                print(f"Now playing: {music}")
                os.startfile(file_path)
                break
        else:
            speak("No music files found in the selected folder.")
    else:
        speak("No folder selected.")

def send_email():
    """Send an email using SMTP."""
    try:
        speak("Please provide the recipient's email address.")
        recipient = input("Recipient Email: ")  # You can also use speech input
        speak("What should the subject of the email be?")
        subject = take_command()
        speak("What message would you like to send?")
        message = take_command()
        
        # Login credentials for your email account
        sender_email = "YOUR_EMAIL@gmail.com"
        sender_password = "YOUR_PASSWORD"  # Use an app password for better security
        
        # Prepare the email
        email = EmailMessage()
        email['From'] = sender_email
        email['To'] = recipient
        email['Subject'] = subject
        email.set_content(message)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(email)

        speak("Email has been sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I encountered an error while sending the email. Please try again.")

def search_wikipedia(query):
    """Search Wikipedia for a query."""
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(result)
    except wikipedia.DisambiguationError as e:
        speak("The query is ambiguous. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def chat_with_gpt(prompt):
    """Interact with OpenAI GPT."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
        speak(reply)
        print(f"AI: {reply}")
    except Exception as e:
        speak("I encountered an error while communicating with OpenAI.")

def execute_command(command):
    """Execute tasks based on user commands."""
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}.")
    elif "open notepad" in command:
        subprocess.Popen("notepad.exe")
        speak("Opening Notepad.")
    elif "search wikipedia for" in command:
        query = command.replace("search wikipedia for", "").strip()
        search_wikipedia(query)
    elif "play music" in command:
        play_music()
    elif "send an email" in command:
        send_email()
    elif "open browser" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening browser.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        exit()
    else:
        # Use GPT for conversational queries
        chat_with_gpt(command)

# Main program loop
def main():
    """Run the assistant."""
    speak("Hello! I am your assistant. How can I help you today?")
    while True:
        command = take_command()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()