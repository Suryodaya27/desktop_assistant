import speech_recognition as sr
import webbrowser
import pyttsx3
import os
from bs4 import BeautifulSoup
import requests
import google.generativeai as genai
import time
import PIL.Image
import subprocess
from PIL import ImageGrab
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access API key
google_api_key = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Todo list to store tasks
todo_list = []

#saved contacts for sending whatsApp messsage
contacts = {
    "mom": "+917666703174",
    "dad": "+919768323800",
    "brother": "+919004289288",
    "sister": "+919892564991",
}

#priority queue for reminder based on time and date
reminder = []


def activate_assistant():
    print("Assistant activated. You can now give commands.")
    engine.say("Assistant activated. You can now give commands.")
    engine.runAndWait()

def deactivate_assistant():
    print("Assistant deactivated.")
    engine.say("Assistant deactivated.")
    engine.runAndWait()

def open_website(url, name):
    print(f"Opening {name}...")
    engine.say(f"Opening {name}...")
    engine.runAndWait()
    webbrowser.open(url)

def get_breaking_news():
    url = "https://www.ndtv.com/india"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all("h2", class_="newsHdng")
    breaking_news = [item.get_text() for item in news_items]
    return breaking_news

def add_task(task):
    todo_list.append(task)
    print(f"Task '{task}' added to todo list.")
    engine.say(f"Task '{task}' added to todo list.")
    engine.runAndWait()

def show_todo_list():
    if todo_list:
        print("Todo List:")
        for i, task in enumerate(todo_list, 1):
            print(f"{i}. {task}")
    else:
        print("Todo list is empty.")

def remove_task(task_index):
    try:
        task_index = int(task_index)
        if 1 <= task_index <= len(todo_list):
            removed_task = todo_list.pop(task_index - 1)
            print(f"Task '{removed_task}' removed from todo list.")
            engine.say(f"Task '{removed_task}' removed from todo list.")
            engine.runAndWait()
        else:
            print("Invalid task index.")
            engine.say("Invalid task index.")
            engine.runAndWait()
    except ValueError:
        print("Invalid task index.")
        engine.say("Invalid task index.")
        engine.runAndWait()

def gemini(question):
    engine.say("Please wait while I generate the response.")
    try:
        user_prompt = f"Given question:{question} please explain in short and simple manner without using extra characters as much as possible."
        response = model.generate_content(user_prompt)
        print(response.text)
        result = response.text.replace('*','')
        engine.say(result)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        engine.say("Sorry, I encountered an error while generating the response.")
        engine.runAndWait()

def open_whatsapp_message(contact):
    contact_number = contacts.get(contact.lower())
    if contact_number:
        print(f"Opening WhatsApp message of {contact} ")
        engine.say(f"Opening WhatsApp message of {contact}...")
        engine.runAndWait()
        os.system(f"start whatsapp://send?phone={contact_number}")
    else:
        print(f"Contact '{contact}' not found.")
        engine.say(f"Contact '{contact}' not found.")
        engine.runAndWait()

def send_whatsapp_message(contact, message):
    contact_number = contacts.get(contact.lower())
    if contact_number:
        print(f"Sending WhatsApp message to {contact}...")
        engine.say(f"Sending WhatsApp message to {contact}...")
        engine.runAndWait()
        os.system(f"https://api.whatsapp.com/send?phone={contact_number}&text={message}")
    else:
        print(f"Contact '{contact}' not found.")
        engine.say(f"Contact '{contact}' not found.")
        engine.runAndWait()

def set_reminder(time, date, message):
    reminder.append((time, date, message))
    print(f"Reminder set for {time} on {date}.")
    engine.say(f"Reminder set for {time} on {date}.")
    engine.runAndWait()

def show_reminder():
    if reminder:
        print("Reminder:")
        for i, (time, date, message) in enumerate(reminder, 1):
            print(f"{i}. {message} on {date} at {time}")
    else:
        print("No reminders set.")

def delete_reminder(reminder_index):
    try:
        reminder_index = int(reminder_index)
        if 1 <= reminder_index <= len(reminder):
            time, date, message = reminder.pop(reminder_index - 1)
            print(f"Reminder '{message}' on {date} at {time} deleted.")
            engine.say(f"Reminder '{message}' on {date} at {time} deleted.")
            engine.runAndWait()
        else:
            print("Invalid reminder index.")
            engine.say("Invalid reminder index.")
            engine.runAndWait()
    except ValueError:
        print("Invalid reminder index.")
        engine.say("Invalid reminder index.")
        engine.runAndWait()

def capture_screenshot():
    # Take a screenshot of the currently active window
    subprocess.run(["snippingtool", "/clip"])  # Open Snipping Tool and copy to clipboard
    time.sleep(2)  # Wait for Snipping Tool to open
    screenshot = ImageGrab.grabclipboard()

    if screenshot is None:
        print("Failed to take screenshot.")
        return None

    return screenshot

def save_image(image, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = time.strftime("%Y%m%d%H%M%S")
    image_path = os.path.join(folder, f"screenshot_{timestamp}.png")
    image.save(image_path)
    return image_path

def summarize_text():
    engine.say("Please snip the text you want to summarize.")
    folder = "screenshots"
    screenshot = capture_screenshot()
    if screenshot:
        image_path = save_image(screenshot, folder)
        print("Image saved at:", image_path)
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(["Summarize the text present",img], stream=True)
        response.resolve()
        os.remove(image_path)
        print(response.text)
        engine.say(response.text)

def explain_image():
    engine.say("Please snip the image you me to explain.")
    folder = "screenshots"
    screenshot = capture_screenshot()
    if screenshot:
        image_path = save_image(screenshot, folder)
        print("Image saved at:", image_path)
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(["Explain image content",img], stream=True)
        response.resolve()
        os.remove(image_path)
        print(response.text)
        engine.say(response.text)

def solve():
    engine.say("Please snip the question you want to solve.")
    folder = "screenshots"
    screenshot = capture_screenshot()
    if screenshot:
        image_path = save_image(screenshot, folder)
        print("Image saved at:", image_path)
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(["Answer the question",img], stream=True)
        response.resolve()
        os.remove(image_path)
        print(response.text)
        engine.say(response.text)

def process_command(command, assistant_active):
    command = command.lower()
    if "activate" in command:
        activate_assistant()
        assistant_active = True
    
    elif assistant_active:
        if "open youtube" in command:
            open_website("https://www.youtube.com", "YouTube")
        elif "open google" in command:
            open_website("https://www.google.com", "Google")
        elif "open code" in command:
            open_website("https://leetcode.com/problemset/all/", "LeetCode")
        elif "open whatsapp" in command:
            os.system("start whatsapp://")
        elif "show recent news" in command:
            news_list = get_breaking_news()
            print("Recent News:")
            for news in news_list:
                print("-", news)
            engine.say("Here are the recent news headlines.")
            engine.runAndWait()
        elif "add task" in command:
            task = command.replace("add task", "").strip()
            add_task(task)
        elif "show to do list" in command:
            show_todo_list()
        elif "remove task" in command:
            task_index = command.replace("remove task", "").strip()
            remove_task(task_index)
        elif "ask assistant" in command:
            question = command.replace("ask assistant", "").strip()
            gemini(question)
        elif "open whatsapp message" in command:
            contact = command.replace("open whatsapp message of", "").strip()
            #print(command)
            #message will look like
            #send whatsapp message of CONTACT_NAME 
            contact = contact.strip()
            open_whatsapp_message(contact)
        elif "send whatsapp message" in command:
            contact, message = command.replace("send whatsapp message to", "").strip().split("that")
            contact = contact.strip()
            message = message.strip()
            send_whatsapp_message(contact, message)
        elif "set reminder" in command:
            command = command.replace("set reminder", "").strip()
            time, date, message = command.split("on")
            set_reminder(time, date, message)
        elif "show reminders" in command:
            show_reminder()
        elif "delete reminder" in command:
            reminder_index = command.replace("delete reminder", "").strip()
            delete_reminder(reminder_index)
        elif "web search" in command:
            query = command.replace("web search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "summarise text" in command:
            summarize_text()
        elif "explain image" in command:
            explain_image()
        elif "solve" in command:
            solve()
        elif "deactivate" in command:
            deactivate_assistant()
            assistant_active = False
        else:
            print(f"Unknown command: {command}")
            engine.say("Sorry, I didn't understand that.")
            engine.runAndWait()
    else:
        print("Assistant is inactive. Say 'activate assistant' to enable it.")
        engine.say("Assistant is inactive. Say 'activate assistant' to enable it.")
        engine.runAndWait()
    return assistant_active

def listen_and_process():
    assistant_active = False
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening... Speak something:")
                audio = recognizer.listen(source,phrase_time_limit=5 , timeout=3)
                print("Processing...")
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            assistant_active = process_command(command, assistant_active)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    listen_and_process()
