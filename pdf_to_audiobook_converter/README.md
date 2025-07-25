# 📘 PDF to Audiobook Converter

A Python GUI application that converts PDF files into spoken audio using Text-to-Speech engines.

---

## 🛠 Features

- 📄 Load and extract text from PDF files
- 🔊 Convert extracted or custom text to speech using:
  - `pyttsx3` (Offline)
  - `gTTS` (Google Text-to-Speech)
- 💾 Export audio as `.mp3`
- 🎛️ Adjustable volume and speech speed
- 🖼️ Simple GUI using `Tkinter`

---

## 🚀 Getting Started

### 🔧 Prerequisites

Make sure you have **Python 3.6+** installed on your Windows system.  
You can download Python from [python.org](https://www.python.org/downloads/).

> ✅ **Check “Add Python to PATH” during installation**

### 📦 Installation

Open a terminal (CMD or PowerShell) and run:

```bash
pip install PyMuPDF pyttsx3 gTTS fpdf
