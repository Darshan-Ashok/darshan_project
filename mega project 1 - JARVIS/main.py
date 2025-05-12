import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary  # Ensure this module and music data exist
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()

# News API key
newsapi = "068438614a1e4ef2ab7cef9cbd3db336"

def speak(text):
    """Use text-to-speech to speak the given text."""
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    """Process the spoken command."""
    command = c.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in command:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:5]:  # Limit to top 5 articles
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't find any news articles.")
        else:
            speak("Failed to fetch news.")
    else:
        speak("Sorry, I didn't understand that command.")
        print("Unrecognized command:", c)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    recognizer = sr.Recognizer()

    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            word = recognizer.recognize_google(audio)
            print(f"Detected word: {word}")

            if "jarvis" in word.lower():
                speak("Yes?")
                print("Jarvis Active...")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                try:
                    command = recognizer.recognize_google(audio)
                    print(f"Detected command: {command}")
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that. Please try again.")
                except sr.RequestError as e:
                    speak(f"Error with recognition service: {e}")
            else:
                print("Wake word not detected.")

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except sr.UnknownValueError:
            print("Could not understand audio. Please speak clearly.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
