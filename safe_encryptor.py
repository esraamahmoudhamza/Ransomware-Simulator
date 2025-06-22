import os
from tkinter import messagebox, Toplevel, Label, filedialog
from ttkthemes import ThemedTk
from tkinter import ttk
from cryptography.fernet import Fernet

class FancyEncryptor:
    def __init__(self, master):
        self.master = master
        self.master.title("Fancy Safe Encryptor")
        self.master.geometry("650x500")
        self.master.configure(bg="#003366")

        self.master.set_theme("arc")

        self.file_path = None
        self.key_file = None
        self.key = None
        self.blinking = False

        self.title_label = Label(master, text="Welcome to the Safe Encryptor Simulator",
                                 font=("Helvetica", 18, "bold"), bg="#003366", fg="white")
        self.title_label.pack(pady=25)

        self.animate_label = Label(master, text="Protect or Lock your file with a click!",
                                   font=("Helvetica", 14, "italic"), bg="#003366", fg="white")
        self.animate_label.pack(pady=10)

        self.select_button = ttk.Button(master, text="Select File", command=self.select_file)
        self.select_button.pack(pady=10)

        self.encrypt_button = ttk.Button(master, text="Encrypt File", command=self.encrypt_file, state="disabled")
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ttk.Button(master, text="Decrypt File", command=self.decrypt_file, state="disabled")
        self.decrypt_button.pack(pady=10)

        self.progress = ttk.Progressbar(master, length=400, mode='determinate')
        self.progress.pack(pady=15)

        self.status_label = Label(master, text="", font=("Helvetica", 14, "bold"), bg="#003366", fg="white")
        self.status_label.pack(pady=10)

        self.animate_text()

    def animate_text(self):
        current = self.animate_label.cget("fg")
        next_color = "white" if current == "#66ccff" else "#66ccff"
        self.animate_label.config(fg=next_color)
        self.master.after(500, self.animate_text)

    def select_file(self):
        base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_folder")
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
            messagebox.showinfo("Info", f"'test_folder' was created here:\n{base_folder}\nPlease add files to encrypt.")
        file = filedialog.askopenfilename(initialdir=base_folder, 
                                          title="Select file to encrypt",
                                          filetypes=[("All supported", "*.txt *.pdf *.jpg *.png *.pptx *.docx"),
                                                     ("Text files", "*.txt"),
                                                     ("PDF files", "*.pdf"),
                                                     ("Images", "*.jpg *.png"),
                                                     ("PowerPoint", "*.pptx"),
                                                     ("Word Docs", "*.docx")])
        if file:
            self.file_path = file
            self.key_file = os.path.join(os.path.dirname(self.file_path), "encryption.key")
            self.status_label.config(text=f"Selected file:\n{os.path.basename(file)}")
            self.encrypt_button.config(state="normal")
            self.decrypt_button.config(state="disabled")

    def encrypt_file(self):
        if not self.file_path or not os.path.exists(self.file_path):
            messagebox.showerror("Error", "Please select a valid file first.")
            return

        self.key = Fernet.generate_key()
        with open(os.path.join(os.path.dirname(self.file_path), "encryption.key"), "wb") as kf:
            kf.write(self.key)

        fernet = Fernet(self.key)
        self.progress['value'] = 0
        self.master.update_idletasks()

        try:
            with open(self.file_path, "rb") as f:
                data = f.read()
            encrypted = fernet.encrypt(data)
            with open(self.file_path, "wb") as f:
                f.write(encrypted)
            self.progress['value'] = 100
            self.status_label.config(text="File encrypted successfully!")
            self.show_ransom_window()
            self.decrypt_button.config(state="normal")
            self.encrypt_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")
            self.progress['value'] = 0

    def decrypt_file(self):
        if not self.file_path or not os.path.exists(self.file_path):
            messagebox.showerror("Error", "Please select a valid file first.")
            return
        if not self.key_file or not os.path.exists(self.key_file):
            messagebox.showerror("Error", "Encryption key not found!")
            return

        with open(self.key_file, "rb") as kf:
            self.key = kf.read()

        fernet = Fernet(self.key)
        self.progress['value'] = 0
        self.master.update_idletasks()

        try:
            with open(self.file_path, "rb") as f:
                encrypted = f.read()
            decrypted = fernet.decrypt(encrypted)
            with open(self.file_path, "wb") as f:
                f.write(decrypted)
            self.progress['value'] = 100
            self.status_label.config(text="File decrypted successfully!")
            self.show_restore_window()
            self.encrypt_button.config(state="normal")
            self.decrypt_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")
            self.progress['value'] = 0

    def show_ransom_window(self):
        ransom_win = Toplevel(self.master)
        ransom_win.title("RANSOMWARE ALERT")
        ransom_win.geometry("450x250")
        ransom_win.configure(bg="red")
        Label(ransom_win, text="This is a RANSOMWARE simulation!\nYour file is encrypted.",
              font=("Helvetica", 16, "bold"), fg="white", bg="red").pack(expand=True)

    def show_restore_window(self):
        restore_win = Toplevel(self.master)
        restore_win.title("Files Restored")
        restore_win.geometry("450x250")
        restore_win.configure(bg="green")
        Label(restore_win, text="Your files have been successfully restored!",
              font=("Helvetica", 16, "bold"), fg="white", bg="green").pack(expand=True)


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = FancyEncryptor(root)
    root.mainloop()
