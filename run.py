import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import threading
import time
from pynput.keyboard import Key, Listener, Controller

# Inicjalizacja zmiennych
sending = False
message_entries = []
available_themes = ["ubuntu", "arc", "plastik"]

# Instancja kontrolera klawiatury
keyboard = Controller()

def update_character_count(event):
    message_entry = event.widget
    text = message_entry.get()
    character_count_label.config(text=f"Liczba znaków: {len(text)}")

def validate_inputs(repeats_text, delay_text):
    if not repeats_text.isdigit() or int(repeats_text) <= 0:
        raise ValueError("Nieprawidłowa wartość 'Powtórzenia'. Wprowadź dodatnią liczbę.")
    if not delay_text.isdigit() or int(delay_text) < 0:
        raise ValueError("Nieprawidłowa wartość 'Opóźnienie'. Wprowadź liczbę nieujemną.")

def send_messages():
    global sending
    if sending:
        return

    messages = [entry.get() for entry in message_entries]
    repeats_text = repeats_entry.get()
    delay_text = delay_entry.get()

    try:
        validate_inputs(repeats_text, delay_text)
        repeats = int(repeats_text)
        delay = int(delay_text) / 1000

        if all(not message for message in messages):
            raise ValueError("Brak wiadomości do wysłania.")

        sending = True
        for _ in range(repeats):
            for message in messages:
                if not sending:
                    break
                if not message:
                    continue
                keyboard.type(message)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(delay)
            if not sending:
                break
        if sending:
            messagebox.showinfo("Sukces", "Wszystkie wiadomości zostały wysłane.")
    except ValueError as e:
        messagebox.showerror("Błąd", str(e))
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
    finally:
        sending = False

def start_sending():
    global sending
    if not sending:
        threading.Thread(target=send_messages).start()

def stop_sending():
    global sending
    sending = False
    messagebox.showinfo("Zatrzymano", "Wysyłanie wiadomości zostało zatrzymane.")

def on_key_release(key):
    if key == Key.f2:
        stop_sending()

def on_key_press(key):
    if key == Key.f1:
        start_sending()

def change_theme(event):
    selected_theme = theme_var.get()
    style.set_theme(selected_theme)

keyboard_listener = Listener(on_release=on_key_release, on_press=on_key_press)
keyboard_listener.start()

root = tk.Tk()
root.title("Wysyłacz Wiadomości")

style = ThemedStyle(root)
style.set_theme("ubuntu")

theme_var = tk.StringVar(value="ubuntu")

ttk.Label(root, text="Wybierz motyw:").pack()
theme_option = ttk.Combobox(root, textvariable=theme_var, values=available_themes)
theme_option.bind("<<ComboboxSelected>>", change_theme)
theme_option.pack()

for i in range(6):
    ttk.Label(root, text=f"Wiadomość {i + 1}:").pack()
    message_entry = ttk.Entry(root)
    message_entry.pack()
    message_entry.bind("<KeyRelease>", update_character_count)
    message_entries.append(message_entry)

ttk.Label(root, text="Powtórzenia:").pack()
repeats_entry = ttk.Entry(root)
repeats_entry.pack()

ttk.Label(root, text="Opóźnienie (ms):").pack()
delay_entry = ttk.Entry(root)
delay_entry.pack()

character_count_label = ttk.Label(root, text="Liczba znaków: 0")
character_count_label.pack()

ttk.Button(root, text="Wyślij wiadomości", command=start_sending).pack()
ttk.Button(root, text="Zatrzymaj wysyłanie", command=stop_sending).pack()

root.mainloop()
