import tkinter as tk
from PIL import Image, ImageTk
import threading
import pywhatkit as kit
import time
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pyautogui
import requests
import datetime

# Initialize the pyttsx3 engine for speech output
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set the speed of speech

# Dictionary of contacts
contacts = {
    "",
}

# Function to speak a message
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice command
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")
        return None

# Function to send WhatsApp messages using contact names
def send_whatsapp_message():
    try:
        speak("Please tell me the contact's name.")
        name = listen_command()

        if name in contacts:
            phone_number = contacts[name]
            speak(f"What message would you like to send to {name}?")
            message = listen_command()

            if message:
                kit.sendwhatmsg_instantly(f"+{phone_number}", message)
                speak(f"Message sent successfully to {name}!")
            else:
                speak("I didn't catch the message. Please try again.")
        else:
            speak(f"Sorry, I couldn't find {name} in your contacts.")
    except Exception as e:
        print(f"Error sending message: {e}")
        speak("There was an error sending the message. Please try again.")

# Function to get and display the weather of a city
def get_weather():
    speak("Which city's weather update do you need?")
    city = listen_command()
    if city:
        api_key = ""  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response["cod"] == 200:
            temperature = response["main"]["temp"]
            condition = response["weather"][0]["description"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]

            weather_report = f"""
            🌤 **Weather Update for {city}** 🌤
            -----------------------------------
            - **Condition:** {condition.capitalize()}
            - **Temperature:** {temperature}°C
            - **Humidity:** {humidity}%
            - **Wind Speed:** {wind_speed} m/s
            -----------------------------------
            """

            print(weather_report)  # Display text format output
            speak(f"The weather in {city} is {condition} with a temperature of {temperature}°C. Humidity is {humidity}% and wind speed is {wind_speed} meters per second.")
        else:
            speak("Sorry, I couldn't retrieve the weather. Please check the city name.")
            print("Error: Unable to fetch weather data.")

# Function to play music on YouTube
def play_music():
    speak("Which song would you like to play?")
    song = listen_command()
    if song:
        url = f"https://www.youtube.com/results?search_query={song}"
        webbrowser.open(url)
        time.sleep(5)  # Wait for YouTube to load
        speak(f"Playing {song} on YouTube.")
        pyautogui.press('tab', presses=3, interval=0.5)  # Adjust tab count if needed
        pyautogui.press('enter')

# Function to open Google with custom search
def open_google():
    speak("What do you want to search on Google?")
    query = listen_command()
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching for {query} on Google.")

# Function to open YouTube with custom search
def open_youtube():
    speak("What do you want to search on YouTube?")
    query = listen_command()
    if query:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        time.sleep(5)  # Wait for YouTube to load
        speak(f"Searching for {query} on YouTube.")

# Function to execute commands
def execute_command(command):
    if "send message" in command:
        send_whatsapp_message()
    elif "play music" in command:
        play_music()
    elif "open google" in command:
        open_google()
    elif "open youtube" in command:
        open_youtube()
    elif "weather update" in command:  # 🔥 Added weather command here
        get_weather()
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("Sorry, I didn't understand that. Please try again.")

# Function to display the looping GIF
def start_custom_size_gif():
    gif_path = "iron1.gif"  # Replace with your GIF file path

    try:
        gif = Image.open(gif_path)

        global root
        root = tk.Tk()
        root.title("Virtual Assistant")
        root.attributes("-fullscreen", False)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        gif_width = int(screen_width * 0.8)
        gif_height = int(screen_height * 0.8)

        resized_frames = []
        for frame_index in range(gif.n_frames):
            gif.seek(frame_index)
            resized_frame = gif.resize((gif_width, gif_height), Image.Resampling.LANCZOS)
            resized_frames.append(ImageTk.PhotoImage(resized_frame))

        x_position = (screen_width - gif_width) // 2
        y_position = (screen_height - gif_height) // 2
        root.geometry(f"{gif_width}x{gif_height}+{x_position}+{y_position}")

        gif_label = tk.Label(root)
        gif_label.pack()

        def update_frame(index=0):
            gif_label.config(image=resized_frames[index])
            gif_label.image = resized_frames[index]
            next_frame = (index + 1) % gif.n_frames
            root.after(100, update_frame, next_frame)

        update_frame()

        def command_listener():
            while True:
                command = listen_command()
                if command:
                    execute_command(command)

        threading.Thread(target=command_listener, daemon=True).start()

        root.bind("<Escape>", lambda e: root.destroy())
        root.mainloop()

    except Exception as e:
        print(f"Error loading or resizing GIF: {e}")

# Run the assistant
if __name__ == "__main__":
    start_custom_size_gif()