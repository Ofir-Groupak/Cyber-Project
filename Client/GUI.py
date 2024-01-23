import tkinter as tk
from tkinter import *
def login_page():
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("350x300")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    title_label = tk.Label(frame, text="Login", font=("Helvetica", 20, "bold"))
    title_label.grid(row=0, column=1, columnspan=2, pady=10)

    tk.Label(frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky="e")
    username_entry = tk.Entry(frame, font=("Helvetica", 12))
    username_entry.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, sticky="e")
    password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12))
    password_entry.grid(row=2, column=1, pady=5, padx=10)

    def send_data():
        information = username_entry.get() + "#" + password_entry.get()
        client_object.send(information.encode())

    login_button = tk.Button(frame, text="Login",command=send_data, font=("Helvetica", 12), bg="red",
                             fg="white", padx=10, pady=5)
    login_button.grid(row=3, column=1, columnspan=2, pady=10)

    signup_button = tk.Button(frame,command=sign_up(root), text="Signup", font=("Helvetica", 12), bg="red",
                              fg="white", padx=10, pady=5)
    signup_button.grid(row=4, column=1, pady=10,padx=10)
    root.mainloop()

def sign_up(previous_window):
    previous_window.destroy()
    root = tk.Tk()
    root.title("Signup Page")
    root.geometry("400x300")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    title_label = tk.Label(frame, text="Signup", font=("Helvetica", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky="e")
    username_entry = tk.Entry(frame, font=("Helvetica", 12))
    username_entry.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, sticky="e")
    password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12))
    password_entry.grid(row=2, column=1, pady=5, padx=10)

    signup_button = tk.Button(frame, text="Signup", font=("Helvetica", 12), bg="#4CAF50", fg="white",
                              padx=10, pady=5)
    signup_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()
login_page()