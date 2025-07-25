
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pyttsx3
from gtts import gTTS
import os

# Initialize pyttsx3 engine
engine = pyttsx3.init()

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract text: {e}")
        return ""

def convert_text_to_speech(text, use_gtts=False, export_mp3=False):
    if use_gtts:
        try:
            tts = gTTS(text=text, lang='en')
            if export_mp3:
                tts.save("output.mp3")
                os.system("start output.mp3")  # For Windows
            else:
                tts.save("temp.mp3")
                os.system("start temp.mp3")
        except Exception as e:
            messagebox.showerror("TTS Error", str(e))
    else:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            messagebox.showerror("TTS Error", str(e))

def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text = extract_text_from_pdf(file_path)
        if text:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, text)

def play_audio():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("No Text", "Please load a PDF or enter some text.")
        return
    convert_text_to_speech(text, use_gtts=use_gtts.get(), export_mp3=export_mp3.get())

def update_volume(val):
    volume = float(val)
    engine.setProperty('volume', volume)

def update_speed(val):
    rate = int(val)
    engine.setProperty('rate', rate)

# GUI Setup
root = tk.Tk()
root.title("PDF to Audiobook Converter")
root.geometry("700x600")

frame = tk.Frame(root)
frame.pack(pady=10)

load_button = tk.Button(frame, text="Load PDF", command=open_pdf)
load_button.pack(side=tk.LEFT, padx=10)

play_button = tk.Button(frame, text="Play Audio", command=play_audio)
play_button.pack(side=tk.LEFT, padx=10)

use_gtts = tk.BooleanVar()
gtts_checkbox = tk.Checkbutton(frame, text="Use gTTS", variable=use_gtts)
gtts_checkbox.pack(side=tk.LEFT, padx=10)

export_mp3 = tk.BooleanVar()
export_checkbox = tk.Checkbutton(frame, text="Export MP3", variable=export_mp3)
export_checkbox.pack(side=tk.LEFT, padx=10)

text_box = tk.Text(root, wrap=tk.WORD, height=25, width=80)
text_box.pack(padx=10, pady=10)

volume_label = tk.Label(root, text="Volume")
volume_label.pack()
volume_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, command=update_volume)
volume_slider.set(1.0)
volume_slider.pack(fill="x", padx=10)

speed_label = tk.Label(root, text="Speed")
speed_label.pack()
speed_slider = tk.Scale(root, from_=100, to=300, orient=tk.HORIZONTAL, command=update_speed)
speed_slider.set(200)
speed_slider.pack(fill="x", padx=10)

root.mainloop()
