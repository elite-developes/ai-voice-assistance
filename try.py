import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import time  # <-- For adding delay

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "API_KEY"

# Function to perform speech synthesis
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Process Commands after wake word
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, song not found.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Only speak top 5 headlines
                speak(article['title'])
        else:
            speak("Failed to fetch news.")
    else:
        speak("Sorry, I don't understand that command.")

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening to wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yaa, how can I help you?")   # <-- Clearer phrase
                time.sleep(1)  # <-- Important: allow time for audio to play before mic restarts

                print("Jarvis is active")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"Jarvis error: {e}")
