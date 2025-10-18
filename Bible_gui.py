import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import re
import json
import os
import random

# Regex pattern to match verses like "John 3:16"
verse_pattern = re.compile(r"([A-Za-z]+) (\d+):(\d+)\s+(.*?)(?=\s+[A-Za-z]+\s\d+:\d+|$)", re.DOTALL)

def extract_text(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        try:
            full_text += page.extract_text() + "\n"
        except:
            continue
    return full_text

def parse_verses(text):
    verses_by_book = {}
    for match in verse_pattern.finditer(text):
        book, chapter, verse, content = match.groups()
        book = book.lower().strip()
        if book not in verses_by_book:
            verses_by_book[book] = []
        verses_by_book[book].append({
            "chapter": int(chapter),
            "verse": int(verse),
            "text": content.strip()
        })
    return verses_by_book

def apply_divine_entropy(verses_by_book):
    for book in verses_by_book:
        random.shuffle(verses_by_book[book])
    return verses_by_book

def save_json(verses_by_book, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for book, verses in verses_by_book.items():
        filename = f"{book.replace(' ', '_')}.json"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            json.dump(verses, f, indent=2)

def show_random_verse(verses_by_book):
    all_verses = []
    for verses in verses_by_book.values():
        all_verses.extend(verses)
    verse = random.choice(all_verses)
    messagebox.showinfo("📜 Divine Verse", f"{verse['chapter']}:{verse['verse']} — {verse['text']}")

def convert_pdf_to_json():
    pdf_path = filedialog.askopenfilename(title="Select Bible PDF", filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        return

    output_dir = filedialog.askdirectory(title="Select Output Folder")
    if not output_dir:
        return

    try:
        progress_bar.start()
        root.update()

        text = extract_text(pdf_path)
        verses = parse_verses(text)

        if entropy_var.get():
            verses = apply_divine_entropy(verses)

        save_json(verses, output_dir)
        progress_bar.stop()
        show_random_verse(verses)
        messagebox.showinfo("✅ Success", f"Bible JSON files saved to:\n{output_dir}")
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("❌ Error", str(e))

# GUI setup
root = tk.Tk()
root.title("📜 Divine Bible JSONifier")
root.geometry("460x280")

label = tk.Label(root, text="Select a Bible PDF to convert to JSON", font=("Arial", 12))
label.pack(pady=10)

btn = tk.Button(root, text="Choose PDF and Convert", command=convert_pdf_to_json, font=("Arial", 10))
btn.pack(pady=5)

entropy_var = tk.BooleanVar()
entropy_check = tk.Checkbutton(root, text="Enable Divine Entropy (scramble verses)", variable=entropy_var)
entropy_check.pack(pady=5)

progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=20)

footer = tk.Label(root, text="Made for chaos. Powered by scripture.", font=("Arial", 9), fg="gray")
footer.pack(pady=5)

root.mainloop()
