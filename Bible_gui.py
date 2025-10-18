import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import re
import json
import os

# Regex to match verses like "John 3:16"
verse_pattern = re.compile(r"([A-Za-z]+) (\d+):(\d+)\s+(.*?)\s*(?=[A-Za-z]+\s\d+:\d+|$)", re.DOTALL)

def extract_text(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

def parse_verses(text):
    verses_by_book = {}
    for match in verse_pattern.finditer(text):
        book, chapter, verse, content = match.groups()
        book = book.lower()
        if book not in verses_by_book:
            verses_by_book[book] = []
        verses_by_book[book].append({
            "chapter": int(chapter),
            "verse": int(verse),
            "text": content.strip()
        })
    return verses_by_book

def save_json(verses_by_book, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for book, verses in verses_by_book.items():
        with open(os.path.join(output_dir, f"{book}.json"), "w", encoding="utf-8") as f:
            json.dump(verses, f, indent=2)

def convert_pdf_to_json():
    pdf_path = filedialog.askopenfilename(title="Select Bible PDF", filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        return

    try:
        text = extract_text(pdf_path)
        verses = parse_verses(text)
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return
        save_json(verses, output_dir)
        messagebox.showinfo("Success", f"Bible JSON files saved to:\n{output_dir}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Bible PDF to JSON Converter")
root.geometry("400x200")

label = tk.Label(root, text="Select a Bible PDF to convert to JSON", font=("Arial", 12))
label.pack(pady=20)

btn = tk.Button(root, text="Choose PDF and Convert", command=convert_pdf_to_json, font=("Arial", 10))
btn.pack(pady=10)

root.mainloop()
