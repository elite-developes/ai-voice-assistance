import speech_recognition as sr
import webbrowser # For using browser.
import pyttsx3 # For text to speech. (package)
import musicLibrary
import requests

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "API_KEY"

# Function to perform speech recognition
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
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    
    else:
        speak("Sorry, I don't understand that command.")

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        print("recorgnizing...")
        try:
            with sr.Microphone() as source:
                print("Listening to wake word...")
                recognizer.adjust_for_ambient_noise(source)  # helps with background noise
                audio = recognizer.listen(source, timeout = 5, phrase_time_limit=3)
            
            word = recognizer.recognize_google(audio)
            if (word.lower()=="jarvis"):
                speak("Yaa")
                print("Jarvis is active")
                # Listen for command
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Jarvis error: {0}",format(e))