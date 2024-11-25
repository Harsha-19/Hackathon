import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import webbrowser
import requests

recognizer = sr.Recognizer()
pygame.mixer.init()


def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.RequestError as e:
            print(f"API error: {e}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except Exception as ex:
            print(f"Unexpected error: {ex}")
        return None  
    

def respond_with_audio(text):
    print(f"Chatbot says: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    try:
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.unload()
        if os.path.exists(filename):
            os.remove(filename)


def handle_command(command):
    if "open google" in command:
        respond_with_audio("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "cyber scams" in command:
        respond_with_audio("Let me fetch some information about cyber scams.")
        info = fetch_cyber_scams_info()
        respond_with_audio(info)
    else:
        respond_with_audio("I'm sorry, I didn't understand that command. Can you repeat it?")


def fetch_cyber_scams_info():
    try:
        response = "Cyber scams include phishing, identity theft, ransomware, and more."
        return response
    except Exception as e:
        return "I couldn't fetch the information right now. Please try again later."


def start_chatbot():
    welcome_text = "Hello! How can I assist you today?"
    respond_with_audio(welcome_text)
    while True:
        user_input = get_audio_input()
        if user_input is None:
            continue  
        if user_input.lower() in ["exit", "quit", "bye"]:
            respond_with_audio("Goodbye! Have a nice day!")
            pygame.mixer.quit()  
        else:
            handle_command(user_input.lower())
            
start_chatbot()