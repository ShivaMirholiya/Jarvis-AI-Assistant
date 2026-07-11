import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary
from client import get_ai_response  # Importing Gemini function
from gtts import gTTS
import pygame
import os

# Initialize speech engine
engine = pyttsx3.init()
newsapi = "65e898927e794335944887cd00c301c0"

def speak_old(text):
    # print(f"Jarvis: {text}\n")
    engine.say(text)
    engine.runAndWait()

def speak(text):
    # print(f"Jarvis: {text}\n")
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")



def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open whatsapp" in c.lower():
        speak("Opening WhatsApp")
        webbrowser.open("https://www.whatsapp.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        try:
            link = musicLibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        except KeyError:
            speak("Sorry, I could not find that song in the library.")
            
    elif "news" in c.lower():
        speak("Fetching the latest news...")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if not articles:
                speak("No news articles found.")
                return
            
            # Read only top 3 news to save time
            for article in articles:
                speak(article['title'])
    
    elif "exit" in c.lower() or "quit" in c.lower() or "stop" in c.lower():
        speak("Shutting down systems. Goodbye, Sir!")
        exit()
        
    else:
        print("Jarvis is thinking...")
        answer = get_ai_response(c)
        speak(answer)


if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    r = sr.Recognizer()
    
    while True:
        print("\nWaiting for wake word 'Jarvis'....")
        try:
            with sr.Microphone() as source:
                # Listen for the wake word
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                word = r.recognize_google(audio)
                
            if word.lower() == "jarvis":
                speak("Yes Sir?")
                
                # Listen for the actual command
                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for your command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    command = r.recognize_google(audio)
                    print(f"You: {command}")
                    
                    # Process the command
                    processCommand(command)

        except sr.WaitTimeoutError:
            # Ignore timeout and keep listening
            pass
        except sr.UnknownValueError:
            # Ignore if it couldn't understand the background noise
            pass
        except Exception as e:
            print("Error:", e)