import datetime
import webbrowser
import pyttsx3
import requests
import time
import threading
import random
import os
import pywhatkit as kit
import tkinter as tk
from tkinter import scrolledtext
import openai
import http.client  # Importing http.client for additional API calls

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for pyttsx3
engine.setProperty('rate', 175)  # Speed of speech
engine.setProperty('volume', 1)   # Volume level (0.0 to 1.0)

# List available voices and set a specific voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for different voices

# Set your OpenAI API key directly
openai.api_key = "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"

# Function to create a splash screen
def show_splash_screen():
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x200")
    splash_label = tk.Label(splash, text="Welcome to Jarvis!", font=("Helvetica", 16))
    splash_label.pack(pady=20)
    splash.after(3000, splash.destroy)  # Close the splash screen after 3 seconds

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user with a professional opening
def greet_user():
    current_time = datetime.datetime.now()
    hour = current_time.strftime("%I:%M %p")  # Get the current time in 12-hour format with AM/PM
    greeting = ""
    
    if current_time.hour < 12:
        greeting = "Good morning!"
    elif 12 <= current_time.hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    # Professional introduction
    introduction = "I am Lisa, your personal assistant. I can help you with various tasks including checking the time, searching the web, providing weather updates, and much more."
    
    # Get the temperature in Tanta
    temperature_info = get_temperature("Tanta")  # Fixed city name
    return f"{greeting} It's {hour}. {introduction} {temperature_info} How can I assist you today?"

# Function for simple conversation
def simple_conversation(user_input):
    responses = {
        "how are you": "I'm just a program, but thanks for asking!",
        "what's your name": "I am Lisa, your personal assistant.",
        "tell me a joke": "Why did the computer go to the doctor? Because it had a virus!",
        "help": "Here are some things I can do:\n"
                 "- Tell you the current time\n"
                 "- Search the web\n"
                 "- Provide the current temperature\n"
                 "- Set an alarm\n"
                 "- Play a YouTube video\n"
                 "- Send a WhatsApp message\n"
                 "- Shut down the system\n"
                 "- Calculate an expression\n"
                 "- Fetch the latest news\n"
                 "- Remind you of something\n"
                 "- Play a random song from your playlist\n"
                 "- Exit the assistant" }
    return responses.get(user_input, "I'm not sure how to respond to that. You can ask for help to see what I can do.")

# Function to search the web
def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching the web for {query}."

# Function to get temperature from Visual Crossing API in Celsius
def get_temperature(city):
    API_KEY = 'QSYXS2A39PL5Z94TFDLFEJSRS'  # Your Visual Crossing API key
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        if "currentConditions" in data:
            temperature_f = data["currentConditions"]["temp"]
            # Convert temperature from Fahrenheit to Celsius
            temperature_c = (temperature_f - 32) * 5.0 / 9.0
            return f"The current temperature in {city} is {temperature_c:.2f}°C."
        else:
            return "Temperature data is not available."
    else:
        return f"Error: {data.get('message', 'City not found or invalid API key.')}"
    
# Function to set an alarm
def set_alarm(alarm_time):
    def alarm():
        while True:
            if time.strftime("%H:%M") == alarm_time:
                print("Alarm ringing!")
                speak("Alarm ringing!")
                break
            time.sleep(60)
    threading.Thread(target=alarm).start()

# Function to play a YouTube video
def play_youtube_video(video_url):
    webbrowser.open(video_url)
    return f"Playing video: {video_url}"

# Function to send WhatsApp messages
def send_whatsapp_message(phone_number, message):
    kit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
    return f"Message sent to {phone_number}."

# Function to shut down the system
def shutdown_system():
    os.system("shutdown /s /t 1")

# Function to calculate
def calculator(expression):
    try:
        result = eval(expression)
        return f"The result is {result}."
    except Exception as e:
        return "There was an error in your calculation."

# Function to fetch news headlines
def get_news():
    API_KEY = '66a75570b94f42599e5e3862308cd313'  # Your News API key
    response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}")
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [article["title"] for article in articles]
        return "Top headlines: " + ", ".join(headlines[:5]) if headlines else "No news available."
    else:
        return "Failed to fetch news."

# Function to set a reminder
def set_reminder(reminder):
    print(f"Reminder set: {reminder}")
    speak(f"Reminder set: {reminder}")

# Function to create a personalized playlist
def play_random_song(playlist):
    song = random.choice(playlist)
    webbrowser.open(song)
    return f"Playing a random song from your playlist: {song}"

# Function to interact with ChatGPT
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can choose a different model if needed
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "I'm sorry, I couldn't process that request."

# Function to fetch prayer times
def get_prayer_times(city):
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey your_token"  # Replace with your actual token
    }
    conn.request("GET", f"/pray/all?data.city={city}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Function to fetch football leagues
def get_football_leagues():
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey your_token"  # Replace with your actual token
    }
    conn.request("GET", "/football/leaguesList", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Function to fetch currently playing movies
def get_playing_movies():
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'authorization': "apikey your_token",  # Replace with your actual token
        'content-type': "application/json"
    }
    conn.request("GET", "/watching/moviesPlaying", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Function to handle user input
def handle_input():
    command = entry.get().lower()
    entry.delete(0, tk.END)  # Clear the entry box
    response = ""

    if "time" in command:
      response = datetime.datetime.now().strftime("%H:%M")
      speak(response)

    elif "search" in command:
        query = command.split("search ")[-1]
        response = search_web(query)
        speak(response)

    elif "temperature" in command:
        city = "Tanta"  # Fixed city name
        response = get_temperature(city)
        speak(response)

    elif "set an alarm" in command:
        alarm_time = command.split("set an alarm for ")[-1]
        set_alarm(alarm_time)
        response = f"Alarm set for {alarm_time}."
        speak(response)

    elif "play" in command and "youtube" in command:
        video_url = command.split("play ")[-1]
        response = play_youtube_video(video_url)
        speak(response)

    elif "whatsapp" in command:
        details = command.split("send ")[-1].split(" to ")
        phone_number = details[1].split(" ")[0]
        message = details[0]
        response = send_whatsapp_message(phone_number, message)
        speak(response)

    elif "shutdown" in command:
        shutdown_system()
        response = "Shutting down the system."
        speak(response)

    elif "calculate" in command:
        expression = command.split("calculate ")[-1]
        response = calculator(expression)
        speak(response)

    elif "news" in command:
        response = get_news()
        speak(response)

    elif "remind me" in command:
        reminder = command.split("remind me to ")[-1]
        set_reminder(reminder)

    elif "play a song" in command:
        playlist = ["song1_url", "song2_url", "song3_url"]  # Replace with actual song URLs
        response = play_random_song(playlist)
        speak(response)

    elif "chat" in command:
        user_prompt = command.split("chat ")[-1]
        response = chat_with_gpt(user_prompt)
        speak(response)

    elif "prayer times" in command:
        city = command.split("in ")[-1] if "in " in command else "istanbul"
        response = get_prayer_times(city)
        speak(response)

    elif "football leagues" in command:
        response = get_football_leagues()
        speak(response)

    elif "currently playing movies" in command:
        response = get_playing_movies()
        speak(response)

    elif "exit" in command or "quit" in command:
        response = "Goodbye! Have a great day!"
        speak(response)
        root.quit()

    else:
        response = simple_conversation(command)  # Fixed the typo here
        speak(response)

    # Display the response in the text area
    output_area.config(state=tk.NORMAL)
    output_area.insert(tk.END, f"You: {command}\nAssistant: {response}\n\n")
    output_area.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Voice Assistant")

# Show the splash screen
show_splash_screen()

# Create a text area for output
output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_area.pack(padx=10, pady=10)

# Create an entry box for user input
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

# Create a button to submit the input
submit_button = tk.Button(root, text="Submit", command=handle_input)
submit_button.pack(pady=10)

# Start the application
welcome_message = greet_user()
speak(welcome_message)  # Speak the welcome message
output_area.config(state=tk.NORMAL)
output_area.insert(tk.END, f"Assistant: {welcome_message}\n\n")  # Display the welcome message in the output area
output_area.config(state=tk.DISABLED)
root.mainloop()