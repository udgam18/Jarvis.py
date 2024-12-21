import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime
import smtplib
import requests
import pyautogui
import os
import openai
import logging
import random
import time
import threading

# Initialize logging
logging.basicConfig(filename='jarvis.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize OpenAI API with your API key
openai.api_key = 'your_openai_api_key_here'

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Task list
tasks = []

# User profile
user_profile = {
    "name": "User ",
    "preferred_voice": 0,
    "weather_city": "New York"
}

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User  said: {query}\n")
    except sr.UnknownValueError:
        print("No input")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("Sorry, I am unable to process your request at the moment.")
        return "None"
    return query.lower()

def open_website(url):
    speak(f"Opening {url}")
    webbrowser.open(url)

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No information found. Please try another query.")

def get_date():
    now = datetime.datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    speak(f"Today's date is {date}")

def get_time():
    now = datetime.datetime.now()
    time = now.strftime("%I:%M %p")
    speak(f"The current time is {time}")

def get_weather(city_name=None):
    if city_name is None:
        city_name = user_profile["weather_city"]
    api_key = 'your_api_key_here'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        speak(f"The temperature in {city_name} is {temperature} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found. Please try again.")

def get_weather_forecast(city_name=None):
    if city_name is None:
        city_name = user_profile["weather_city"]
    api_key = 'your_api_key_here'
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        speak(f"Here is the 5-day weather forecast for {city_name}:")
        for forecast in data['list'][:5]:  # Get the first 5 forecasts
            date_time = forecast['dt_txt']
            temperature = forecast['main']['temp']
            weather_desc = forecast['weather'][0]['description']
            speak(f"On {date_time}, the temperature will be {temperature} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found. Please try again.")

def send_email(receiver_email, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        message = f"Subject: {subject}\n\n {body}"
        server.sendmail('your_email@gmail.com', receiver_email, message)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email at the moment.")

def create_model():
    speak("I will guide you to a website where you can create a model.")
    open_website("https://teachablemachine.withgoogle.com/")

def attempt_model_creation():
    try:
        create_model()
    except Exception as e:
        print(e)
        speak("Sorry, I cannot create a model for you at the moment.")

def search_web(query):
    try:
        speak(f"Searching the web for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        print(e)
        speak("Sorry, I cannot search the web for you at the moment.")

def move_screen(direction):
    if direction == "up":
        pyautogui.scroll(100)
    elif direction == "down":
        pyautogui.scroll(-100)
    elif direction == "left":
        pyautogui.hscroll(100)
    elif direction == "right":
        pyautogui.hscroll(-100)

def close_application(app_name):
    app_map = {
        "chrome": "chrome.exe",
        "whatsapp": "whatsapp.exe",
        "notepad": "notepad.exe",
        "outlook": "outlook.exe",
        "nitrosense": "nitrosense.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "calculator": "calculator.exe",
        "file explorer": "explorer.exe",
        "terminal": "cmd.exe"
    }
    app_name_lower = app_name.lower()
    if app_name_lower in app_map:
        os.system(f"taskkill /f /im {app_map[app_name_lower]}")
        speak(f"{app_name.capitalize()} has been closed.")
    else:
        speak(f"Sorry, I cannot close {app_name}. Please ensure it is installed and try again.")

def open_application(app_name):
    app_map = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vscode": r"C:\Users\YourUsername\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "notepad": r"C:\Windows\System32\notepad.exe",
        "library": r"C:\Path\To\Your\Library\Application.exe",
        "microsoft store": r"C:\Windows\SystemApps\Microsoft.WindowsStore_8wekyb3d8bbwe\WinStore.App.exe",
        "outlook": r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
        "nitrosense": r"C:\Program Files\NitroSense\NitroSense.exe",
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        "office": r"C:\Program Files\Microsoft Office\root\Office16\O365HomePrem.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
        "file explorer": r"C:\Windows\explorer.exe",
        "terminal": r"C:\Windows\System32\cmd.exe",
        "whatsapp": r"C:\Users\YourUsername\AppData\Local\WhatsApp\WhatsApp.exe"
    }
    app_name_lower = app_name.lower()
    if app_name_lower in app_map:
        os.startfile(app_map[app_name_lower])
        speak(f"{app_name.capitalize()} is opening.")
    else:
        speak(f"Sorry, I cannot open {app_name}. Please ensure it is installed and try again.")

def shut_down():
    speak("Shutting down the laptop. Closing all applications.")
    os.system("shutdown /s /t 1")

def handle_general_query(query):
    try:
        speak(f"Searching the web for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        print(e)
        speak("Sorry, I cannot search the web for you at the moment.")

def ask_chatgpt(question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=question,
            max_tokens=100
        )
        speak(response.choices[0].text.strip())
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't find an answer to your question.")

def set_reminder(reminder, time):
    def reminder_thread(reminder, time):
        time.sleep(time)  # Wait for the specified time
        speak(f"Reminder: {reminder}")
    threading.Thread(target=reminder_thread, args=(reminder, time)).start()

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ]
    joke = random.choice(jokes)
    speak(joke)

def get_quote():
    quotes = [
        "The best way to predict the future is to invent it. - Alan Kay",
        "Life is 10% what happens to us and 90% how we react to it. - Charles R. Swindoll",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer"
    ]
    quote = random.choice(quotes)
    speak(quote)

def currency_converter(amount, from_currency, to_currency):
    api_key = 'your_currency_api_key_here'
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    if "error" not in data:
        rate = data["rates"].get(to_currency)
        if rate:
            converted_amount = amount * rate
            speak(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
        else:
            speak("Sorry, I couldn't find the conversion rate for that currency.")
    else:
        speak("Sorry, I couldn't fetch the currency data.")

def unit_converter(value, from_unit, to_unit):
    conversion_factors = {
        "meters": 1,
        "kilometers": 1000,
        "miles": 1609.34,
        "feet": 0.3048,
        "inches": 0.0254,
        "grams": 1,
        "kilograms": 1000,
        "pounds": 453.592
    }
    if from_unit in conversion_factors and to_unit in conversion_factors:
        converted_value = value * (conversion_factors[to_unit] / conversion_factors[from_unit])
        speak(f"{value} {from_unit} is equal to {converted_value:.2f} {to_unit}.")
    else:
        speak("Sorry, I couldn't perform that conversion.")

def note_taking(note):
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    speak("Your note has been saved.")

def help_command():
    commands = [
        "Say 'hi jarvis' to start the assistant.",
        "Use 'jarvis open <application>' to open an application.",
        "Use 'jarvis close <application>' to close an application.",
        "Ask 'jarvis what's the date' to get the current date.",
        "Ask 'jarvis what's the time' to get the current time.",
        "Ask 'jarvis what's the weather' to get the weather information.",
        "Ask 'jarvis what's the weather forecast' for a 5-day forecast.",
        "Use 'jarvis search the web for <query>' to search the web.",
        "Use 'jarvis search wikipedia for <query>' to search Wikipedia.",
        "Use 'jarvis send email' to send an email.",
        "Use 'jarvis create a model' to create a model.",
        "Use 'jarvis tell me a joke' for a random joke.",
        "Use 'jarvis give me a quote' for a motivational quote.",
        "Use 'jarvis convert <amount> <from_currency> to <to_currency>' for currency conversion.",
        "Use 'jarvis convert <value> <from_unit> to <to_unit>' for unit conversion.",
        "Say 'jarvis shut down' to shut down the assistant.",
        "Say 'jarvis help' to get this list of commands.",
        "Use 'jarvis take a note <your note>' to save a note.",
        "Use 'jarvis add task <task>' to add a task to your task list.",
        "Use 'jarvis view tasks' to see your current tasks.",
        "Use 'jarvis delete task <task_number>' to delete a specific task.",
        "Use 'jarvis remind me to <task> at <time>' to set a reminder.",
        "Use 'jarvis set my city to <city>' to change the default weather city.",
        "Use 'jarvis change voice to <voice_number>' to change the voice of the assistant.",
        "Use 'jarvis play music' to start playing music.",
        "Use 'jarvis stop music' to stop the music.",
        "Use 'jarvis search images for <query>' to find images on the web.",
        "Use 'jarvis play a game' to start a simple text-based game."
    ]
    speak("Here are the commands you can use:")
    for command in commands:
        speak(command)

def add_task(task):
    tasks.append(task)
    speak(f"Task '{task}' has been added to your task list.")

def view_tasks():
    if tasks:
        speak("Here are your current tasks:")
        for index, task in enumerate(tasks, start=1):
            speak(f"Task {index}: {task}")
    else:
        speak("You have no tasks in your list.")

def delete_task(task_number):
    try:
        task_number = int(task_number) - 1
        if 0 <= task_number < len(tasks):
            removed_task = tasks.pop(task_number)
            speak(f"Task '{removed_task}' has been removed from your task list.")
        else:
            speak("Invalid task number. Please try again.")
    except ValueError:
        speak("Please provide a valid task number.")

def set_weather_city(city_name):
    user_profile["weather_city"] = city_name
    speak(f"Weather city has been set to {city_name}.")

def change_voice(voice_number):
    if 0 <= voice_number < len(voices):
        engine.setProperty('voice', voices[voice_number].id)
        user_profile["preferred_voice"] = voice_number
        speak(f"Voice has been changed to voice number {voice_number}.")
    else:
        speak("Invalid voice number. Please try again.")

def play_music():
    # Placeholder for music playback functionality
    speak("Playing music...")

def stop_music():
    # Placeholder for stopping music playback functionality
    speak("Music has been stopped.")

def search_images(query):
    speak(f"Searching for images of {query}")
    webbrowser.open(f"https://www.google.com/search?hl=en&tbm=isch&q={query}")

def play_game():
    speak("Let's play a number guessing game! I'm thinking of a number between 1 and 100.")
    number_to_guess = random.randint(1, 100)
    attempts = 0
    while True:
        speak("Please guess a number.")
        guess = take_command()
        if guess.isdigit():
            guess = int(guess)
            attempts += 1
            if guess < number_to_guess:
                speak("Too low! Try again.")
            elif guess > number_to_guess:
                speak("Too high! Try again.")
            else:
                speak(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
                break
        else:
            speak("Please provide a valid number.")

def personalized_greeting():
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

if __name__ == "__main__":
    running = False

    while True:
        query = take_command()

        if query == "hi jarvis":
            personalized_greeting()
            speak("Hello, I am your assistant Jarvis. How can I assist you today?")
            running = True
        elif query == "jarvis shut down":
            shut_down()
        elif query == "jarvis help":
            help_command()
        elif query == "jarvis exit":
            exit_assistant()

        if running:
            if query == "none":
                continue

            if query.startswith("jarvis open "):
                app_name = query.replace("jarvis open ", "")
                open_application(app_name)
            elif query.startswith("jarvis close "):
                app_name = query.replace("jarvis close ", "")
                close_application(app_name)
            elif query.startswith("jarvis search wikipedia for "):
                search_wikipedia(query.replace("jarvis search wikipedia for ", ""))
            elif query.startswith("jarvis search the web for "):
                search_web(query.replace("jarvis search the web for ", ""))
            elif query.startswith("jarvis what do you mean by "):
                handle_general_query(query.replace("jarvis what do you mean by ", ""))
            elif query == "jarvis what's the date" or query == "jarvis what is the date":
                get_date()
            elif query == "jarvis what's the time" or query == "jarvis what is the time":
                get_time()
            elif query == "jarvis what's the weather" or query == "jarvis what is the weather":
                get_weather()
            elif query == "jarvis what's the weather forecast" or query == "jarvis what is the weather forecast":
                get_weather_forecast()
            elif query == "jarvis send email":
                receiver_email = "receiver@example.com"
                subject = "Test Subject"
                body = "Test Body"
                send_email(receiver_email, subject, body)
            elif query == "jarvis create a model":
                attempt_model_creation()
            elif query.startswith("jarvis set a reminder for "):
                parts = query.replace("jarvis set a reminder for ", "").split(" at ")
                if len(parts) == 2:
                    reminder = parts[0]
                    time = int(parts[1])  # Assuming time is in seconds
                    set_reminder(reminder, time)
            elif query.startswith("jarvis set my city to "):
                city_name = query.replace("jarvis set my city to ", "")
                set_weather_city(city_name)
            elif query.startswith("jarvis change voice to "):
                voice_number = int(query.replace("jarvis change voice to ", ""))
                change_voice(voice_number)
            elif query.startswith("jarvis play music"):
                play_music()
            elif query.startswith("jarvis stop music"):
                stop_music()
            elif query.startswith("jarvis search images for "):
                image_query = query.replace("jarvis search images for ", "")
                search_images(image_query)
            elif query.startswith("jarvis play a game"):
                play_game()
            elif query.startswith("jarvis tell me a joke"):
                tell_joke()
            elif query.startswith("jarvis give me a quote"):
                get_quote()
            elif query.startswith("jarvis convert "):
                parts = query.replace("jarvis convert ", "").split(" to ")
                if len(parts) == 2:
                    from_part = parts[0].split()
                    to_part = parts[1].split()
                    if len(from_part) == 3 and len(to_part) == 2:
                        amount = float(from_part[0])
                        from_currency = from_part[1]
                        to_currency = to_part[1]
                        currency_converter(amount, from_currency, to_currency)
                    elif len(from_part) == 3 and len(to_part) == 3:
                        value = float(from_part[0])
                        from_unit = from_part[1]
                        to_unit = to_part[1]
                        unit_converter(value, from_unit, to_unit)
            elif query.startswith("jarvis take a note "):
                note = query.replace("jarvis take a note ", "")
                note_taking(note)
            elif query.startswith("jarvis add task "):
                task = query.replace("jarvis add task ", "")
                add_task(task)
            elif query == "jarvis view tasks":
                view_tasks()
            elif query.startswith("jarvis delete task "):
                task_number = query.replace("jarvis delete task ", "")
                delete_task(task_number)
            elif query == "jarvis news updates":
                news_updates()
            else:
                speak("Let me search for an answer.")
                ask_chatgpt(query)
# Additional features can be added here as needed

# Function to fetch and read the latest news headlines
def news_updates():
    api_key = 'your_news_api_key_here'
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "ok":
        speak("Here are the latest news headlines:")
        for article in data["articles"][:5]:  # Get the first 5 articles
            speak(article["title"])
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

# Function to set a personalized greeting based on the time of day
def personalized_greeting():
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

# Main loop to run the assistant
if __name__ == "__main__":
    running = False

    while True:
        query = take_command()

        if query == "hi jarvis":
            personalized_greeting()
            speak("Hello, I am your assistant Jarvis. How can I assist you today?")
            running = True
        elif query == "jarvis shut down":
            shut_down()
        elif query == "jarvis help":
            help_command()
        elif query == "jarvis exit":
            exit_assistant()

        if running:
            if query == "none":
                continue

            if query.startswith("jarvis open "):
                app_name = query.replace("jarvis open ", "")
                open_application(app_name)
            elif query.startswith("jarvis close "):
                app_name = query.replace("jarvis close ", "")
                close_application(app_name)
            elif query.startswith("jarvis search wikipedia for "):
                search_wikipedia(query.replace("jarvis search wikipedia for ", ""))
            elif query.startswith("jarvis search the web for "):
                search_web(query.replace("jarvis search the web for ", ""))
            elif query.startswith("jarvis what do you mean by "):
                handle_general_query(query.replace("jarvis what do you mean by ", ""))
            elif query == "jarvis what's the date" or query == "jarvis what is the date":
                get_date()
            elif query == "jarvis what's the time" or query == "jarvis what is the time":
                get_time()
            elif query == "jarvis what's the weather" or query == "jarvis what is the weather":
                get_weather()
            elif query == "jarvis what's the weather forecast" or query == "jarvis what is the weather forecast":
                get_weather_forecast()
            elif query == "jarvis send email":
                receiver_email = "receiver@example.com"
                subject = "Test Subject"
                body = "Test Body"
                send_email(receiver_email, subject, body)
            elif query == "jarvis create a model":
                attempt_model_creation()
            elif query.startswith("jarvis set a reminder for "):
                parts = query.replace("jarvis set a reminder for ", "").split(" at ")
                if len(parts) == 2:
                    reminder = parts[0]
                    time = int(parts[1])  # Assuming time is in seconds
                    set_reminder(reminder, time)
            elif query.startswith("jarvis set my city to "):
                city_name = query.replace("jarvis set my city to ", "")
                set_weather_city(city_name)
            elif query.startswith("jarvis change voice to "):
                voice_number = int(query.replace("jarvis change voice to ", ""))
                change_voice(voice_number)
            elif query.startswith("jarvis play music"):
                play_music()
            elif query.startswith("jarvis stop music"):
                stop_music()
            elif query.startswith("jarvis search images for "):
                image_query = query.replace("jarvis search images for ", "")
                search_images(image_query)
            elif query.startswith("jarvis play a game"):
                play_game()
            elif query.startswith("jarvis tell me a joke"):
                tell_joke()
            elif query.startswith("jarvis give me a quote"):
                get_quote()
            elif query.startswith("jarvis convert "):
                parts = query.replace("jarvis convert ", "").split(" to ")
                if len(parts) == 2:
                    from_part = parts[0].split()
                    to_part = parts[1].split()
                    if len(from_part) == 3 and len(to_part) == 2:
                        amount = float(from_part[0])
                        from_currency = from_part[1]
                        to_currency = to_part[1]
                        currency_converter(amount, from_currency, to_currency)
                    elif len(from_part) == 3 and len(to_part) == 3:
                        value = float(from_part[0])
                        from_unit = from_part[1]
                        to_unit = to_part[1]
                        unit_converter(value, from_unit, to_unit)
            elif query.startswith("jarvis take a note "):
                note = query.replace("jarvis take a note ", "")
                note_taking(note)
            elif query.startswith("jarvis add task "):
                task = query.replace("jarvis add task ", "")
                add_task(task)
            elif query == "jarvis view tasks":
                view_tasks()
            elif query.startswith("jarvis delete task "):
                task_number = query.replace("jarvis delete task ", "")
                delete_task(task_number)
            elif query == "jarvis news updates":
                news_updates()
            else:
                speak("Let me search for an answer.")
                ask_chatgpt(query)