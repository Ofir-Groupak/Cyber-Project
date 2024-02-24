import tkinter as tk
from tkinter import *
from tkinter import messagebox

def login_page(client_object):
    def toggle_password_visibility(password_entry):
        if show_password_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    root = tk.Tk()
    root.title("Login Page")
    root.geometry("550x400")

    # Set background color to a darker shade of blue
    root.configure(bg="#0e1a40")

    frame = tk.Frame(root, padx=20, pady=20, bg="#0e1a40")
    frame.pack(expand=True)

    title_label = tk.Label(frame, text="Login", font=("Segoe UI", 20, "bold"), bg="#0e1a40", fg="white")
    title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    tk.Label(frame, text="Username:", font=("Segoe UI", 12, "bold"), bg="#0e1a40", fg="white").grid(row=1, column=0,
                                                                                                    pady=5, sticky="e")
    username_entry = tk.Entry(frame, font=("Segoe UI", 12))
    username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

    tk.Label(frame, text="Password:", font=("Segoe UI", 12, "bold"), bg="#0e1a40", fg="white").grid(row=2, column=0,
                                                                                                    pady=5, sticky="e")
    password_entry = tk.Entry(frame, show="*", font=("Segoe UI", 12))
    password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

    show_password_var = tk.BooleanVar()
    show_password_checkbutton = tk.Checkbutton(frame, text="Show Password", variable=show_password_var,
                                               font=("Segoe UI", 10, "bold"), bg="#0e1a40", fg="white",
                                               command=lambda: toggle_password_visibility(password_entry))
    show_password_checkbutton.grid(row=3, column=1, pady=5, sticky="w")

    def send_data():
        information = username_entry.get() + "#" + password_entry.get()
        client_object.send(information.encode())
        response = client_object.recv(1024).decode()
        if response == "Correct":
            first_symptom_window(root, client_object)
        else:
            messagebox.showinfo("Error", "Incorrect password,Try Again!")

    login_button = tk.Button(frame, text="Login", command=send_data, font=("Segoe UI", 10, "bold"), bg="#d81159",
                             fg="white", padx=5, pady=3)
    login_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    signup_button = tk.Button(frame, command=sign_up, text="Signup", font=("Segoe UI", 10, "bold"), bg="#d81159",
                              fg="white", padx=5, pady=3)
    signup_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    root.mainloop()
def sign_up(previous_window):
    previous_window.destroy()
    root = tk.Tk()
    root.title("Signup Page")
    root.geometry("550x400")

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

def first_symptom_window(previous_window,client_object):
    previous_window.destroy()

    def on_enter():
        information = entry.get()
        client_object.send(information.encode())
        question = client_object.recv(1024).decode()
        questionaaire(root2, client_object, question)

    # Create main window
    root2 = tk.Tk()
    root2.title("Second GUI Example")


    # Set window size and background color
    root2.geometry("550x400")
    root2.configure(bg="#0e1a40")


    # Create canvas
    canvas2 = tk.Canvas(root2, width=400, height=300, bg="#0e1a40", highlightthickness=0)
    canvas2.pack()

    # Calculate center coordinates for the plus sign
    center_x = canvas2.winfo_reqwidth() / 2
    center_y = canvas2.winfo_reqheight() / 2

    # Draw red plus sign at the center
    plus = canvas2.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=20)
    plus = canvas2.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=20)

    # Create title
    title_label = tk.Label(root2, text="Enter your first symptom", bg="#0e1a40", fg="white",
                           font=("Segoe UI", 18, "bold"))
    title_label.place(relx=0.5, rely=0.6, anchor="center")

    # Create text box
    entry = tk.Entry(root2)
    entry.place(relx=0.5, rely=0.75, anchor="center")

    # Create Enter button
    btn_enter = tk.Button(root2, text="Enter", width=10, font=("Segoe UI", 12, "bold"), bg="#d81159", fg="white", bd=0,
                          command=on_enter)
    btn_enter.place(relx=0.5, rely=0.9, anchor="center")

    # Run the second event loop
    root2.mainloop()

def questionaaire(previous_window,client_object,question):
    previous_window.destroy()

    def show_text(question):
        if not "You have" in question:
            question_label = tk.Label(root, text=question, bg="#0e1a40", fg="white", font=("Segoe UI", 12, "bold"))
            question_label.place(relx=0.15, rely=0.55)
        else:
            question_label = tk.Label(root, text=question, bg="#0e1a40", fg="white", font=("Segoe UI", 12, "bold"))
            question_label.place(relx=0.3, rely=0.65)
            btn_no.destroy()
            btn_yes.destroy()

    def on_yes():
        client_object.send("yes".encode())
        question_label.destroy()
        result = client_object.recv(1024).decode()
        show_text(result)

    def on_no():
        client_object.send("no".encode())
        question_label.destroy()
        result = client_object.recv(1024).decode()
        show_text(result)

    root = tk.Tk()
    root.title("GUI Example")

    root.geometry("500x400")
    root.configure(bg="#0e1a40")

    canvas = tk.Canvas(root, width=400, height=300,bg="#0e1a40", highlightthickness=0)
    canvas.pack()

    center_x = canvas.winfo_reqwidth() / 2
    center_y = canvas.winfo_reqheight() / 2

    plus = canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=20)
    plus = canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=20)

    question_label = tk.Label(root, text=question, bg="#0e1a40", fg="white", font=("Segoe UI", 12, "bold"))
    question_label.place(relx=0.15, rely=0.55)

    buttons_frame = tk.Frame(root, bg="#0e1a40")
    buttons_frame.pack(expand=True)

    btn_yes = tk.Button(buttons_frame,bg="#d81159",font=("Segoe UI", 12, "bold"), text="Yes", width=10, height=3, command=on_yes)
    btn_yes.pack(side=tk.LEFT, padx=(50, 10))

    btn_no = tk.Button(buttons_frame,bg="#d81159",font=("Segoe UI", 12, "bold"), text="No", width=10, height=3, command=on_no)
    btn_no.pack(side=tk.RIGHT, padx=(10, 50))

    root.mainloop()

    # Run the event loop
    root.mainloop()
