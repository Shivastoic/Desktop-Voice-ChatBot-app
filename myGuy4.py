import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import threading
import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = "Add your ChatGpt api key here"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def handle_voice_input():
    conversation = []
    while True:
        try:
            with sr.Microphone() as source:
                status_label.configure(text="Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                status_label.configure(text="Recognizing...")
                user_input = recognizer.recognize_google(audio)
                user_input_entry.delete(0, tk.END)
                user_input_entry.insert(0, user_input)
                status_label.configure(text="Chatbot is responding...")
        except sr.UnknownValueError:
            status_label.configure(text="Could not understand audio. Please try again.")
            continue

        conversation.append("You (Voice): " + user_input)
        response = chat_with_gpt("\n".join(conversation))
        conversation.append(":)  " + response)

        chat_history_text.configure(state=tk.NORMAL)
        chat_history_text.insert(tk.END, "\n".join(conversation[-2:]))
        chat_history_text.configure(state=tk.DISABLED)
        chat_history_text.see(tk.END)

        engine.say(response)
        engine.runAndWait()

        if user_input.lower() in ["quit", "exit", "ok bye"]:
            break


def button_click():
    threading.Thread(target=handle_voice_input).start()


app = ctk.CTk()
app.geometry("600x500")
app.title("Voice Assistant")


# GUI components
frame = ctk.CTkFrame(app, width=580, height=220)
frame.place(x=10, y=10)
user_input_entry = ctk.CTkEntry(frame, width=500, corner_radius=10, height=40)
user_input_entry.place(x=40, y=60)
start_button = ctk.CTkButton(
    frame,
    text="Ask",
    font=("Roboto", 24),
    text_color="White",
    width=160,
    height=40,
    corner_radius=20,
    fg_color="#252B48",
    hover_color="#445069",
    command=button_click,
)
start_button.place(x=210, y=120)
status_label = ctk.CTkLabel(frame, text="", font=("Roboto", 15))
status_label.place(x=40, y=30)


chat_history_text = ctk.CTkTextbox(
    app,
    wrap=tk.WORD,
    height=250,
    width=580,
    border_width=2,
    border_color="#5B9A8B",
    corner_radius=10,
)
chat_history_text.place(x=10, y=240)


app.mainloop()
