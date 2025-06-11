import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random

# Load word definitions from a text file
def load_word_definitions(file_path):
    word_dict = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if ' - ' in line:
                    word, definition = line.strip().split(' - ', 1)
                    word_dict[word.lower()] = definition
        return word_dict
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return {}

# Save wrong notes to a text file
def save_wrong_notes_txt(wrong_notes, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for word, definition in wrong_notes.items():
                file.write(f"{word} - {definition}\n")
        messagebox.showinfo("Success", "Wrong notes saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the wrong notes: {e}")

# Main application class
class WordLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Learning Program")
        self.root.geometry("600x400")  # Default size for main screen
        self.root.configure(bg="#f9f9f9")  # Light background color for calmness

        self.word_dict = {}
        self.wrong_notes = {}
        self.current_word = None

        # Screen management using Frames
        self.main_frame = tk.Frame(self.root, bg="#f9f9f9")
        self.learning_frame = tk.Frame(self.root, bg="#f9f9f9")

        # Initial screen setup
        self.show_main_screen()

    def center_widgets(self, frame):
        """Center all widgets in a frame"""
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def show_main_screen(self):
        """Show the main screen"""
        self.clear_screen()
        self.root.geometry("600x400")  # Resize for main screen
        self.center_widgets(self.main_frame)
        self.main_frame.pack(fill="both", expand=True)

        # Top fixed title
        tk.Label(
            self.main_frame,
            text="Learn Vocabulary Program",
            font=("Arial", 20, "bold"),
            bg="#f9f9f9",
            fg="#333333"
        ).pack(pady=20)

        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg="#f9f9f9")
        buttons_frame.pack(pady=20)

        tk.Button(
            buttons_frame,
            text="Select Data File",
            command=self.select_data_file,
            bg="#a8d5e2",  # Soft blue
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=20
        ).pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Start Learning",
            command=self.start_learning,
            bg="#c8e6c9",  # Soft green
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=20
        ).pack(pady=10)

        tk.Button(
            buttons_frame,
            text="View Wrong Notes",
            command=self.show_wrong_notes,
            bg="#ffe0b2",  # Soft orange
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=20
        ).pack(pady=10)

    def show_learning_screen(self):
        """Show the learning screen"""
        self.clear_screen()
        self.root.geometry("600x400")  # Resize for learning screen
        self.center_widgets(self.learning_frame)
        self.learning_frame.pack(fill="both", expand=True)

        # Top fixed title
        tk.Label(
            self.learning_frame,
            text="Learn Vocabulary Program",
            font=("Arial", 20, "bold"),
            bg="#f9f9f9",
            fg="#333333"
        ).grid(row=0, column=0, pady=20)

        # Bottom dynamic content frame
        content_frame = tk.Frame(self.learning_frame, bg="#f9f9f9")
        content_frame.grid(row=1, column=0, pady=20)

        self.words = list(self.word_dict.keys())
        random.shuffle(self.words)
        self.current_index = 0

        # Progress label
        self.progress_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 14),
            bg="#f9f9f9",
            fg="#333333"
        )
        self.progress_label.grid(row=0, column=0, pady=10)

        # Word label
        self.word_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 20, "bold"),
            bg="#f9f9f9",
            fg="#333333"
        )
        self.word_label.grid(row=1, column=0, pady=10)

        # Input field
        self.entry = tk.Entry(
            content_frame,
            font=("Arial", 16),
            relief="flat",
            bg="#e0f7fa",  # Light cyan
            justify="center"
        )
        self.entry.grid(row=2, column=0, pady=10)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        # Result display label
        self.result_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 14),
            bg="#f9f9f9",
            fg="#d32f2f"  # Red for incorrect
        )
        self.result_label.grid(row=3, column=0, pady=10)

        # Definition display label
        self.definition_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 14),
            wraplength=400,
            bg="#f9f9f9",
            fg="#333333"
        )
        self.definition_label.grid(row=4, column=0, pady=10)

        # Next button
        self.next_button = tk.Button(
            content_frame,
            text="Next",
            command=self.next_word,
            state=tk.DISABLED,
            bg="#ffccbc",  # Soft coral
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=10
        )
        self.next_button.grid(row=5, column=0, pady=10)

        # Return to main screen button
        tk.Button(
            content_frame,
            text="Return to Main Screen",
            command=self.show_main_screen,
            bg="#d1c4e9",  # Soft purple
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=20
        ).grid(row=6, column=0, pady=10)

        # Show the first word
        self.show_next_word()

    def clear_screen(self):
        """Clear the current screen"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        for widget in self.learning_frame.winfo_children():
            widget.destroy()
        self.main_frame.pack_forget()
        self.learning_frame.pack_forget()

    def select_data_file(self):
        """Select a data file"""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.word_dict = load_word_definitions(file_path)
            if self.word_dict:
                messagebox.showinfo("Success", "Data file loaded successfully!")
            else:
                messagebox.showwarning("Warning", "The data file is empty or incorrectly formatted.")

    def start_learning(self):
        """Start learning"""
        if not self.word_dict:
            messagebox.showwarning("Warning", "Please select a data file first.")
            return
        self.show_learning_screen()

    def show_next_word(self):
        """Show the next word"""
        if self.current_index < len(self.words):
            self.current_word = self.words[self.current_index]
            self.progress_label.config(text=f"Word {self.current_index + 1} of {len(self.words)}")
            self.word_label.config(text=f"Word: {self.current_word}")
            self.definition_label.config(text="")
            self.result_label.config(text="")
            self.entry.delete(0, tk.END)
            self.next_button.config(state=tk.DISABLED)
            self.entry.unbind("<Return>")
            self.entry.bind("<Return>", lambda event: self.check_answer())
        else:
            messagebox.showinfo("Completed", "You have completed all the words!")
            self.show_main_screen()

    def check_answer(self):
        """Check the answer and handle wrong answers"""
        user_input = self.entry.get().lower()
        if user_input == self.current_word:
            self.result_label.config(text="Correct!", fg="#388e3c")  # Green for correct
            self.definition_label.config(text=f"Definition of '{self.current_word}': {self.word_dict[self.current_word]}")
        else:
            self.result_label.config(text="Incorrect.", fg="#d32f2f")  # Red for incorrect
            # Add to wrong notes
            if self.current_word not in self.wrong_notes:
                self.wrong_notes[self.current_word] = self.word_dict[self.current_word]

        # Enable the "Next" button and bind Enter key to move to the next word
        self.next_button.config(state=tk.NORMAL)
        self.entry.unbind("<Return>")
        self.entry.bind("<Return>", lambda event: self.next_word())

    def next_word(self):
        """Move to the next word"""
        self.current_index += 1
        self.show_next_word()

    def show_wrong_notes(self):
        """Show wrong notes"""
        if not self.wrong_notes:
            messagebox.showinfo("Wrong Notes", "There are no wrong notes!")
            return

        # Create the wrong notes screen
        self.clear_screen()
        self.root.geometry("600x400")  # Resize for wrong notes screen

        # Top fixed title
        tk.Label(
            self.root,
            text="Learn Vocabulary Program",
            font=("Arial", 20, "bold"),
            bg="#f9f9f9",
            fg="#333333"
        ).pack(pady=20)

        # Wrong notes table
        tree = ttk.Treeview(self.root, columns=("Word", "Definition"), show="headings")
        tree.heading("Word", text="Word")
        tree.heading("Definition", text="Definition")
        tree.column("Word", width=150)
        tree.column("Definition", width=400)
        tree.pack(pady=20)

        for word, definition in self.wrong_notes.items():
            tree.insert("", "end", values=(word, definition))

        # Save button
        tk.Button(
            self.root,
            text="Save Wrong Notes",
            command=lambda: self.save_wrong_notes_gui(tree),
            bg="#c8e6c9",  # Soft green
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=20
        ).pack(pady=10)

        # Return to main screen button
        tk.Button(
            self.root,
            text="Return to Main Screen",
            command=self.show_main_screen,
            bg="#d1c4e9",  # Soft purple
            fg="black",
            font=("Arial", 12),
            relief="flat",
            width=20
        ).pack(pady=10)

    def save_wrong_notes_gui(self, tree):
        """Save wrong notes and close the program"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
            title="Save Wrong Notes"
        )
        if file_path:
            wrong_notes = {tree.item(item)["values"][0]: tree.item(item)["values"][1] for item in tree.get_children()}
            save_wrong_notes_txt(wrong_notes, file_path)
            # Automatically close the program after saving
            self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WordLearningApp(root)
    root.mainloop()