import pickle
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Server import Examinor
#new

def login_page(client_object):
    """
    Displays a login page GUI for the client to enter their credentials.

    Parameters:
        client_object (socket object): The socket object representing the client connection.

    This function creates a login page using Tkinter GUI toolkit for the client to enter their username and password.
    Upon clicking the login button, the entered credentials are sent to the server for authentication.

    If the authentication is successful, the client is redirected to the first symptom window.
    If the authentication fails, an error message is displayed, and the client can try again.

    The function also provides an option to toggle password visibility and a button to navigate to the signup page.
    """

    def toggle_password_visibility(password_entry):
        if show_password_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    root = tk.Tk()
    root.title("Login Page")
    root.geometry("550x400")
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
        """
        Sends the entered username and password to the server for authentication.
        Upon successful authentication, navigates to the first symptom window.
        Displays an error message if authentication fails.
        """
        information = ["LOGIN", username_entry.get(), password_entry.get()]
        client_object.send(pickle.dumps(information))
        response = client_object.recv(1024).decode()
        if response == "Correct":
            first_symptom_window(root, client_object)
        else:
            messagebox.showinfo("Error", "Incorrect password, Try Again!")

    login_button = tk.Button(frame, text="Login", command=send_data, font=("Segoe UI", 10, "bold"), bg="#d81159",
                             fg="white", padx=5, pady=3)
    login_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    signup_button = tk.Button(frame, command=lambda: signup_page(root, client_object), text="Signup",
                              font=("Segoe UI", 10, "bold"), bg="#d81159", fg="white", padx=5, pady=3)
    signup_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    root.mainloop()

def first_symptom_window(previous_window, client_object):
    """
    Displays the second GUI window for the client to enter their first symptom.

    Parameters:
        previous_window (Tk object): The previous window to be destroyed.
        client_object (socket object): The socket object representing the client connection.

    This function creates a new Tkinter window (root2) for the client to enter their first symptom.
    The previous window (previous_window) is destroyed before displaying the new window.

    The new window allows the client to select their first symptom from a list of options.
    Upon clicking the 'Enter' button, the selected symptom is sent to the server, and the client proceeds
    to the questionnaire window.

    The function utilizes the Examinor class to retrieve a list of all available symptoms for the client to choose from.
    """
    previous_window.destroy()

    def on_enter():
        """
        Sends the selected symptom to the server and proceeds to the questionnaire window.
        """
        information = value_inside.get()
        client_object.send(information.encode())
        question = client_object.recv(1024).decode()
        questionaaire(root2, client_object, question)

    root2 = tk.Tk()
    root2.title("Second GUI Example")
    root2.geometry("550x400")
    root2.configure(bg="#0e1a40")

    canvas2 = tk.Canvas(root2, width=400, height=300, bg="#0e1a40", highlightthickness=0)
    canvas2.pack()

    center_x = canvas2.winfo_reqwidth() / 2
    center_y = canvas2.winfo_reqheight() / 2

    plus = canvas2.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=20)
    plus = canvas2.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=20)

    title_label = tk.Label(root2, text="Enter your first symptom", bg="#0e1a40", fg="white",
                           font=("Segoe UI", 18, "bold"))
    title_label.place(relx=0.5, rely=0.6, anchor="center")

    options_list = Examinor.get_all_symptoms()

    value_inside = tk.StringVar(root2)
    question_menu = tk.OptionMenu(root2, value_inside, *options_list)
    question_menu.place(relx=0.5, rely=0.75, anchor="center")

    btn_enter = tk.Button(root2, text="Enter", width=10, font=("Segoe UI", 12, "bold"), bg="#d81159", fg="white", bd=0,
                          command=on_enter)
    btn_enter.place(relx=0.5, rely=0.9, anchor="center")

    root2.mainloop()

def questionaaire(previous_window,client_object,question):
    """
       Displays a GUI window for the client to answer a specific question (part of the questionnaire).

       Parameters:
           previous_window (Tk object): The previous window to be destroyed.
           client_object (socket object): The socket object representing the client connection.
           question (str): The question to be displayed for the client to answer.

       This function creates a Tkinter window to display a specific question from the questionnaire.
       The previous window (previous_window) is destroyed before displaying the new window.

       The client is presented with the question and given options to answer 'Yes' or 'No'.
       Upon clicking either option, the client's response is sent to the server, and the result is displayed
       accordingly.

       The function utilizes the on_yes and on_no functions to handle the client's response and update the GUI
       accordingly.
       """
    previous_window.destroy()
    def show_text(question1):
        """
               Displays the provided question or result text in the GUI window.

               Parameters:
                   question1 (str): The question or result text to be displayed.
               """
        global question_label
        try:
            if question_label:
                question_label.destroy()
        except NameError:
            pass
        if not "You have" in question1:
            question_label = tk.Label(root, text=question1, bg="#0e1a40", fg="white", font=("Segoe UI", 12, "bold"))
            question_label.place(relx=0.15, rely=0.55)
        else:

            question_label = tk.Label(root, text=question1, bg="#0e1a40", fg="#d81159", font=("Segoe UI", 14, "bold"))
            question_label.place(relx=0.22, rely=0.65,anchor='w')
            btn_no.destroy()
            btn_yes.destroy()

    def on_yes():
        """
        Sends the client's 'Yes' response to the server and displays the result accordingly.
        """
        question_label.destroy()
        client_object.send("yes".encode())
        result = client_object.recv(1024).decode()
        show_text(result)

    def on_no():
        """
        Sends the client's 'No' response to the server and displays the result accordingly.
        """
        question_label.destroy()
        client_object.send("no".encode())
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

    root.mainloop()

def signup_page(previous_window, client_object):
    """
    Displays the sign-up page GUI window for the client to register.

    Parameters:
        previous_window (Tk object): The previous window to be destroyed.
        client_object (socket object): The socket object representing the client connection.

    This function creates a new Tkinter window for the client to register with their information.
    The previous window (previous_window) is destroyed before displaying the new window.

    The sign-up page includes entry fields for the client to input their first name, last name, username, password,
    and select their gender. Additionally, the client can select past diseases from option menus.

    Upon clicking the 'Submit' button, the client's registration information is sent to the server for processing.
    If the client chooses to go back to the login page, they can click the 'Login' button, which directs them to
    the login page.
    """
    previous_window.destroy()

    def back_to_login():
        """
        Destroys the current window and navigates back to the login page.
        """
        root.destroy()
        login_page(client_object)

    def submit_signup():
        """
        Processes the client's sign-up information and sends it to the server.

        Retrieves values from entry fields and option menus, such as first name, last name, gender, username,
        password, and past diseases.
        Sends the client's sign-up information to the server using a predefined format.
        Destroys the sign-up window and navigates back to the login page.
        """
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        gender = gender_var.get()
        username = entry_username.get()
        password = entry_password.get()
        past_diseases = [
            past_diseases_var1.get(),
            past_diseases_var2.get(),
            past_diseases_var3.get()
        ]
        information = ["SIGNUP", first_name, last_name, gender, username, password, past_diseases]


        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Gender:", gender)
        print("Username:", username)
        print("Password:", password)
        print("Past Diseases:", past_diseases)

        print(information)

        client_object.send(pickle.dumps(information))
        root.destroy()
        login_page(client_object)

    root = tk.Tk()
    root.title("Sign Up Page")
    root.geometry("500x600")
    root.configure(bg="#0e1a40")

    # Title label
    title_label = tk.Label(root, text="Sign Up", bg="#0e1a40", fg="white", font=("Segoe UI", 16, "bold"))
    title_label.pack(pady=(20, 10))

    # Labels
    tk.Label(root, text="First Name:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.15, anchor="w")
    tk.Label(root, text="Last Name:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.25, anchor="w")
    tk.Label(root, text="Gender:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.35, anchor="w")
    tk.Label(root, text="Username:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.45, anchor="w")
    tk.Label(root, text="Password:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.55, anchor="w")
    tk.Label(root, text="Past Diseases:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.65, anchor="w")

    # Entry fields
    entry_first_name = tk.Entry(root, font=("Segoe UI", 12), bg="white")
    entry_first_name.place(relx=0.5, rely=0.15, anchor="w")

    entry_last_name = tk.Entry(root, font=("Segoe UI", 12), bg="white")
    entry_last_name.place(relx=0.5, rely=0.25, anchor="w")

    gender_var = tk.StringVar()
    gender_var.set("Male")
    tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", bg="#0e1a40", fg="white",
                   font=("Segoe UI", 10)).place(relx=0.5, rely=0.35, anchor="w")
    tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", bg="#0e1a40", fg="white",
                   font=("Segoe UI", 10)).place(relx=0.65, rely=0.35, anchor="w")

    entry_username = tk.Entry(root, font=("Segoe UI", 12), bg="white")
    entry_username.place(relx=0.5, rely=0.45, anchor="w")

    entry_password = tk.Entry(root, show="*", font=("Segoe UI", 12), bg="white")
    entry_password.place(relx=0.5, rely=0.55, anchor="w")

    past_diseases_var1 = tk.StringVar(root)
    past_diseases_var2 = tk.StringVar(root)
    past_diseases_var3 = tk.StringVar(root)

    options = Examinor.get_all_diseases()
    options.insert(0, "None")

    past_diseases_var1.set("None")
    past_diseases_var2.set("None")
    past_diseases_var3.set("None")

    opt_menu1 = tk.OptionMenu(root, past_diseases_var1, *options)
    opt_menu1.config(bg="white")
    opt_menu1.place(relx=0.5, rely=0.65, anchor="w")

    opt_menu2 = tk.OptionMenu(root, past_diseases_var2, *options)
    opt_menu2.config(bg="white")
    opt_menu2.place(relx=0.5, rely=0.7, anchor="w")

    opt_menu3 = tk.OptionMenu(root, past_diseases_var3, *options)
    opt_menu3.config(bg="white")
    opt_menu3.place(relx=0.5, rely=0.75, anchor="w")

    btn_submit = tk.Button(root, text="Submit", width=10, font=("Segoe UI", 12), bg="#d81159", fg="white", bd=0,
                           command=submit_signup)
    btn_submit.place(relx=0.5, rely=0.85, anchor="center")

    btn_login = tk.Button(root, text="Login", width=10, font=("Segoe UI", 12), bg="#d81159", fg="white", bd=0,
                          command=back_to_login)
    btn_login.place(relx=0.5, rely=0.95, anchor="center")

    root.mainloop()