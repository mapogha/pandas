# modules/speech.py
import speech_recognition as sr
import pyttsx3
import config

engine = pyttsx3.init() #Moved engine initialization out of the speak function to only intialize once

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Adjust for silence
        audio = r.listen(source)

    try:
        print("Recognizing...")
        user_query = r.recognize_google(audio, language=config.SPEECH_LANGUAGE)  # Use the language from config
        print(f"User said: {user_query}\n")
        return user_query.lower() # Return the value
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")
        return "none"