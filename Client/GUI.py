import tkinter as tk
from tkinter import *
def login_page(client_object):
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
        response = client_object.recv(1024).decode()
        if response=="Login Accepted":
            first_symptom_window(root,client_object)

    login_button = tk.Button(frame, text="Login",command=send_data, font=("Helvetica", 12), bg="red",
                             fg="white", padx=10, pady=5)
    login_button.grid(row=3, column=1, columnspan=2, pady=10)

    signup_button = tk.Button(frame,command=sign_up, text="Signup", font=("Helvetica", 12), bg="red",
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

def first_symptom_window(previous_window,client_object):
    previous_window.destroy()

    def on_enter():
        information = entry.get()
        client_object.send(information.encode())
        question = client_object.recv(1024).decode()
        questionaaire(root2,client_object,"niger?")


    # Create main window
    root2 = tk.Tk()
    root2.title("Second GUI Example")

    # Set window size and background color
    root2.geometry("400x300")
    root2.configure(bg="blue")

    # Create canvas
    canvas2 = tk.Canvas(root2, width=300, height=200, bg="blue", highlightthickness=0)
    canvas2.pack()

    # Calculate center coordinates for the plus sign
    center_x = canvas2.winfo_reqwidth() / 2
    center_y = canvas2.winfo_reqheight() / 2

    # Draw red plus sign at the center
    plus = canvas2.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=20)
    plus = canvas2.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=20)

    # Create title
    title_label = tk.Label(root2, text="Enter your first symptom", bg="blue", fg="white", font=("Arial Bold", 18))
    title_label.place(relx=0.5, rely=0.6, anchor="center")

    # Create text box
    entry = tk.Entry(root2)
    entry.place(relx=0.5, rely=0.75, anchor="center")

    # Create Enter button
    btn_enter = tk.Button(root2, text="Enter", width=10, command=on_enter)
    btn_enter.place(relx=0.5, rely=0.9, anchor="center")

    # Run the second event loop
    root2.mainloop()

def questionaaire(previous_window,client_object,question):
    previous_window.destroy()

    def on_yes():
        print("Yes button clicked")

    def on_no():
        print("No button clicked")

    # Create main window
    root = tk.Tk()
    root.title("GUI Example")

    # Set window size and background color
    root.geometry("500x400")
    root.configure(bg="blue")

    # Create canvas
    canvas = tk.Canvas(root, width=400, height=300, bg="blue", highlightthickness=0)
    canvas.pack()

    # Calculate center coordinates for the plus sign
    center_x = canvas.winfo_reqwidth() / 2
    center_y = canvas.winfo_reqheight() / 2

    # Draw red plus sign at the center
    plus = canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=20)
    plus = canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=20)

    question_label = tk.Label(root, text=question, bg="blue", fg="white", font=("Arial Bold", 24))
    question_label.place(relx=0.15,rely=0.55)

    # Create buttons frame
    buttons_frame = tk.Frame(root, bg="blue")
    buttons_frame.pack(expand=True)

    # Create Yes button
    btn_yes = tk.Button(buttons_frame, text="Yes", width=10, height=3, command=on_yes)
    btn_yes.pack(side=tk.LEFT, padx=(50, 10))

    # Create No button
    btn_no = tk.Button(buttons_frame, text="No", width=10, height=3, command=on_no)
    btn_no.pack(side=tk.RIGHT, padx=(10, 50))



    # Run the event loop
    root.mainloop()

