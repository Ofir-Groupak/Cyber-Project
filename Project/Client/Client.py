import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests

def start_client():
    """
    starts the client
    :return: client_socket, server public key , client private key
    """
    server_ip = '127.0.0.1'
    server_port = 4444

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    server_public_key_pem = client_socket.recv(2048)
    global server_public_key
    server_public_key = serialization.load_pem_public_key(
        server_public_key_pem,
        backend=default_backend()
    )

    global client_private_key, client_public_key
    # Generate RSA key pair for the server
    client_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    client_public_key = client_private_key.public_key()
    client_socket.send(client_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    return client_socket , server_public_key , client_private_key

def decrypt_with_private_key(data,client_private_key):
    """
        Decrypts data using the server's private key.

        Parameters:
            data (bytes): The encrypted data to be decrypted.

        Returns:
            bytes: The decrypted data, or an empty string if decryption fails.
        """
    return client_private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def encrypt_with_public_key(data,server_public_key):
    """
       Encrypts data using a client's public key.

       Parameters:
           data (bytes): The data to be encrypted.
           client_object: The client object which has the public key.

       Returns:
           bytes: The encrypted data.
       """
    return server_public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
class LoginPageGUI:
    def __init__(self, client_object,server_key,client_key,previous_window=None):
        """
               Initializes the LoginPageGUI.

               Parameters:
                   client_object: The client object for server communication.
                   server_key: The server's public key for encryption.
                   client_key: The client's private key for decryption.
                   previous_window (optional): The previous Tkinter window to be destroyed, if any.
               """
        global server_public_key
        server_public_key = server_key

        global client_private_key
        client_private_key = client_key
        if previous_window:
            previous_window.destroy()

        self.client_object = client_object

        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("550x400")
        self.root.configure(bg="#0e1a40")

        self.frame = tk.Frame(self.root, padx=20, pady=20, bg="#0e1a40")
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Login", font=("Segoe UI", 24, "bold"), bg="#0e1a40", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.username_label = tk.Label(self.frame, text="Username:", font=("Segoe UI", 16, "bold"), bg="#0e1a40",
                                       fg="white")
        self.username_label.grid(row=1, column=0, pady=5, sticky="e")

        self.username_entry = tk.Entry(self.frame, font=("Segoe UI", 16))
        self.username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.password_label = tk.Label(self.frame, text="Password:", font=("Segoe UI", 16, "bold"), bg="#0e1a40",
                                       fg="white")
        self.password_label.grid(row=2, column=0, pady=5, sticky="e")

        self.password_entry = tk.Entry(self.frame, show="*", font=("Segoe UI", 16))
        self.password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbutton = tk.Checkbutton(self.frame, text="Show Password",
                                                        variable=self.show_password_var,
                                                        font=("Segoe UI", 16, "bold"), bg="#0e1a40", fg="#CB2525",
                                                        activebackground="#0e1a40", activeforeground="#CB2525",
                                                        command=self.toggle_password_visibility)
        self.show_password_checkbutton.grid(row=3, column=1, pady=5, sticky="w")

        self.login_button = tk.Button(self.frame, text="Login", command=self.send_data, font=("Segoe UI", 12, "bold"),
                                      bg="#CB2525",
                                      fg="white", padx=5, pady=3)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.signup_button = tk.Button(self.frame, command=self.open_signup_page, text="Signup",
                                       font=("Segoe UI", 12, "bold"), bg="#CB2525", fg="white", padx=5, pady=3)
        self.signup_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.root.mainloop()

    def toggle_password_visibility(self):
        """
        Toggles the visibility of the password entry field.
        """
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def send_data(self):
        """
        Sends the entered username and password to the server for authentication.
        Upon successful authentication, navigates to the first symptom window.
        Displays an error message if authentication fails.
        """
        username = self.username_entry.get()
        information = ["LOGIN", username, self.password_entry.get()]
        data = encrypt_with_public_key(pickle.dumps(information),server_public_key)
        self.client_object.send(data)
        response = self.client_object.recv(1024)
        response = pickle.loads(response)
        if response[0] == "Correct":

            if response[1]=="True":
                MainMenuGUI(self.client_object, self.root,username)
            else:
                MainMenuGUI(self.client_object, self.root,username)
        else:
            messagebox.showerror("Error", "Incorrect username or password, Try Again!")

    def open_signup_page(self):
        """
        Sends a request to the server to open the signup page and navigates to the signup page GUI.
        """
        data = encrypt_with_public_key(pickle.dumps(["SIGNUP"]),server_public_key)
        self.client_object.send(data)
        SignUpPageGUI(self.root,self.client_object)
class MainMenuGUI:
    def __init__(self, client_object, previous_window, username):
        """
               Initializes the MainMenuGUI.

               Parameters:
                   client_object: The client object for server communication.
                   previous_window: The previous Tkinter window to be destroyed.
                   username (str): The username of the logged-in user.
        """
        self.username = username
        self.client_object = client_object
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.root.geometry("800x650")
        self.root.configure(bg="#0e1a40")

        self.magen_david_label = tk.Label(self.root, text="\u2721", bg="#CB2525", fg="white", font=("Helvetica", 30))
        self.magen_david_label.pack(fill=tk.X)

        self.title_label = tk.Label(self.root, text=f"Hello {username}!", bg="#0e1a40", fg="white", font=("Helvetica", 30, "bold"))
        self.title_label.pack(pady=20)

        self.line_canvas = tk.Canvas(self.root, bg="#0e1a40", height=2, highlightthickness=0)
        self.line_canvas.create_line(0, 0, 800, 0, fill="white", width=1)
        self.line_canvas.pack(fill=tk.X)


        data = client_object.recv(1024)
        data = decrypt_with_private_key(data , client_private_key).decode()
        self.button_frame = tk.Frame(self.root, bg="#0e1a40")
        self.button_frame.pack(pady=20)

        if data == "False":
            self.examine_button = tk.Button(self.button_frame, text="Examine", width=25, height=4, bg="#CB2525", fg="white",
                                            font=("Helvetica", 16), command=lambda: self.open_examine(client_object))
            self.examine_button.grid(row=0, column=0, padx=20, pady=20)

            self.send_message_button = tk.Button(self.button_frame, text="Send Message", width=25, height=4,
                                                 bg="#CB2525", fg="white",
                                                 font=("Helvetica", 16),
                                                 command=lambda: self.send_messages(client_object))
            self.send_message_button.grid(row=0, column=1, padx=20, pady=20)

            self.view_messages_button = tk.Button(self.button_frame, text="View Messages", width=25, height=4,
                                                  bg="#CB2525", fg="white",
                                                  font=("Helvetica", 16),
                                                  command=lambda: self.open_messages(client_object))
            self.view_messages_button.grid(row=1, column=1, padx=20, pady=20)

            self.logout_button = tk.Button(self.button_frame, text="Logout", width=25, height=4, bg="#CB2525",
                                           fg="white",
                                           font=("Helvetica", 16), command=lambda: self.logout(client_object))
            self.logout_button.grid(row=1, column=0, padx=20, pady=20)

        else:
            self.send_message_button = tk.Button(self.button_frame, text="Send Message", width=25, height=4, bg="#CB2525", fg="white",
                                                 font=("Helvetica", 16), command=lambda:self.send_messages(client_object) )
            self.send_message_button.grid(row=0, column=1, padx=20, pady=20)

            self.view_messages_button = tk.Button(self.button_frame, text="View Messages", width=25, height=4, bg="#CB2525", fg="white",
                                                  font=("Helvetica", 16), command=lambda: self.open_messages(client_object))
            self.view_messages_button.grid(row=1, column=1, padx=20, pady=20)

            self.logout_button = tk.Button(self.button_frame, text="Logout", width=25, height=4, bg="#CB2525", fg="white",
                                           font=("Helvetica", 16), command=lambda: self.logout(client_object))
            self.logout_button.grid(row=2, column=1, padx=20, pady=20)

    def logout(self, client_object):
        """
               Logs out the user by sending a logout request to the server.
        """
        data = encrypt_with_public_key("logout".encode(), server_public_key)
        client_object.send(data)
        LoginPageGUI(self.client_object, server_public_key , client_private_key , self.root)

    def open_examine(self, client_object):
        """
               Opens the examination window by sending an examination request to the server.
        """
        data = encrypt_with_public_key("examine".encode(), server_public_key)
        client_object.send(data)
        FirstSymptomWindowGUI(self.root, self.client_object, self.username)

    def open_messages(self, client_object):
        """
               Opens the messages window by sending a request to the server to view messages.
        """
        data = encrypt_with_public_key("open messages".encode(), server_public_key)
        client_object.send(data)
        MessagesGUI(self.root, self.client_object, self.username)
    def send_messages(self,client_object):
        """
               Opens the send message window by sending a request to the server to send a message.
        """
        data = encrypt_with_public_key("send messages".encode(), server_public_key)
        client_object.send(data)
        SendMessageGUI(self.root, self.client_object, self.username," ")
    def run(self):
        """
                Runs the main loop of the Tkinter window.
        """
        self.root.mainloop()
class FirstSymptomWindowGUI:
    def __init__(self, previous_window, client_object, username):
        """
                Initializes the FirstSymptomWindowGUI.

                Parameters:
                    previous_window: The previous Tkinter window to be destroyed.
                    client_object: The client object for server communication.
                    username (str): The username of the logged-in user.
        """
        self.username = username
        self.previous_window = previous_window
        self.client_object = client_object

        self.previous_window.destroy()

        self.root = tk.Tk()
        self.root.title("First Symptom Window")
        self.root.geometry("550x400")
        self.root.configure(bg="#0e1a40")

        # Magen David label at the top
        self.magen_david_label = tk.Label(self.root, text="\u2721", bg="#CB2525", fg="white", font=("Helvetica", 30))
        self.magen_david_label.pack(fill=tk.X)

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#0e1a40", highlightthickness=0)
        self.canvas.pack()

        self.title_label = tk.Label(self.root, text="Enter your first symptom", bg="#0e1a40", fg="white",
                                    font=("Segoe UI", 18, "bold"))
        self.title_label.place(relx=0.5, rely=0.35, anchor="center")

        data =  client_object.recv(1024)


        data = decrypt_with_private_key(data, client_private_key)
        self.options_list = pickle.loads(data)

        self.value_inside = tk.StringVar(self.root)
        self.question_menu = tk.OptionMenu(self.root, self.value_inside, *self.options_list)
        self.question_menu.config(font=("Segoe UI", 14))
        self.question_menu.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_enter = tk.Button(self.root, text="Enter", width=10, font=("Segoe UI", 12, "bold"), bg="#CB2525",
                                   fg="white", bd=0,
                                   command=self.on_enter)
        self.btn_enter.place(relx=0.5, rely=0.65, anchor="center")

        self.root.mainloop()

    def on_enter(self):
        """
        Sends the selected symptom to the server and proceeds to the questionnaire window.

        This function retrieves the selected symptom from the dropdown menu, encrypts it using the server's public key,
        and sends it to the server. Then, it waits for a response from the server, which contains the next question
        to be displayed in the questionnaire window. The response is decrypted using the client's private key before
        initializing the QuestionnaireWindowGUI with the received question.
        """
        information = self.value_inside.get()
        data = encrypt_with_public_key(information.encode(), server_public_key)
        self.client_object.send(data)

        question = self.client_object.recv(1024)
        question = decrypt_with_private_key(question, client_private_key)
        QuestionnaireWindowGUI(self.root, self.client_object, question, self.username)

class QuestionnaireWindowGUI:
    def __init__(self, previous_window, client_object, question, username):
        """
               Initializes the QuestionnaireWindowGUI.

               Parameters:
                   previous_window: The previous Tkinter window to be destroyed.
                   client_object: The client object for server communication.
                   question (str): The current question to be displayed.
                   username (str): The username of the logged-in user.
        """
        self.username = username
        self.previous_window = previous_window
        self.client_object = client_object
        self.question = question

        self.previous_window.destroy()

        self.root = tk.Tk()
        self.root.title("Questionnaire")
        self.root.geometry("800x600")
        self.root.configure(bg="#0e1a40")

        self.magen_david_label = tk.Label(self.root, text="\u2721", bg="#CB2525", fg="white", font=("Helvetica", 40))
        self.magen_david_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.canvas = tk.Canvas(self.root, bg="#0e1a40", height=5, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        self.question_label = tk.Label(self.root, text=self.question, bg="#0e1a40", fg="white",
                                       font=("Segoe UI", 20, "bold"))
        self.question_label.grid(row=1, column=0, columnspan=2, pady=20)

        self.btn_yes = tk.Button(self.root, bg="#CB2525", font=("Segoe UI", 16, "bold"), fg="white",
                                 text="Yes", width=15, height=3, command=self.on_yes)
        self.btn_yes.grid(row=2, column=0, padx=100, pady=(50, 20))

        self.btn_no = tk.Button(self.root, bg="#CB2525", font=("Segoe UI", 16, "bold"), fg="white", text="No",
                                width=15, height=3, command=self.on_no)
        self.btn_no.grid(row=2, column=1, padx=100, pady=(50, 20))

        self.root.mainloop()

    def update_text(self):
        """
        Displays the provided question or result text in the GUI window.

        Parameters:
            question1 (str): The question or result text to be displayed.
        """
        question1 = self.client_object.recv(1024)
        question1 = decrypt_with_private_key(question1, client_private_key).decode()
        try:
            self.question_label.destroy()
        except tk.TclError:
            pass
        if not "You have" in question1:
            self.question_label = tk.Label(self.root, text=question1, bg="#0e1a40", fg="white",
                                           font=("Segoe UI", 20, "bold"))
            self.question_label.grid(row=1, column=0, columnspan=2, pady=20)
            symptom = question1[18:len(question1) - 2]

        else:

            self.question_label = tk.Label(self.root, text=question1, bg="#0e1a40", fg="#CB2525",
                                           font=("Segoe UI", 18, "bold"))
            self.question_label.grid(row=1, column=0, columnspan=2, pady=20)
            self.btn_no.destroy()
            self.btn_yes.destroy()
            self.btn_try_again = tk.Button(self.root, bg="#CB2525", font=("Segoe UI", 16, "bold"), fg="white",
                                           text="Menu", width=15,
                                           height=3, command=lambda: self.back_to_menu())
            self.btn_try_again.grid(row=2, column=0, padx=100, pady=(50, 20))
            self.btn_more_info = tk.Button(self.root, bg="#CB2525", font=("Segoe UI", 16, "bold"), fg="white",
                                           text="More Information", width=20,
                                           height=3, command=lambda: self.go_to_info(question1[9:].lower()))
            self.btn_more_info.grid(row=2, column=1, padx=100, pady=(50, 20))

    def back_to_menu(self):
        """
                Sends the confirmation response to the server and navigates back to the main menu.
        """
        response = messagebox.askquestion("Confirmation", "Do you want your results to be reviewed by a Doctor?")
        data = encrypt_with_public_key(pickle.dumps(["Menu", response]), server_public_key)
        self.client_object.send(data)
        MainMenuGUI(self.client_object, self.root, self.username)

    def go_to_info(self, disease):
        """
                Sends the confirmation response to the server and navigates to the disease information window.

                Parameters:
                    disease (str): The name of the disease to retrieve information for.
        """
        response = messagebox.askquestion("Confirmation", "Do you want your results to be reviewed by a Doctor?")
        data = encrypt_with_public_key(pickle.dumps(["Information", response]), server_public_key)
        self.client_object.send(data)
        DiseaseReportGUI(self.root, disease, self.client_object, self.username)

    def on_yes(self):
        """
        Sends the client's 'Yes' response to the server and displays the result accordingly.
        """
        data = encrypt_with_public_key("yes".encode(), server_public_key)
        self.client_object.send(data)

        self.update_text()

    def on_no(self):
        """
        Sends the client's 'No' response to the server and displays the result accordingly.
        """
        data = encrypt_with_public_key("no".encode(), server_public_key)
        self.client_object.send(data)

        self.update_text()


class SignUpPageGUI:
    def __init__(self, previous_window, client_object):
        """
        Initializes the Sign-Up Page GUI.

        Parameters:
            previous_window (tk.Tk): The previous window to be destroyed.
            client_object (socket): The client socket object for communication with the server.
        """
        self.previous_window = previous_window
        self.client_object = client_object
        options = self.client_object.recv(1024)
        options = decrypt_with_private_key(options, client_private_key)
        options = pickle.loads(options)
        self.options = options[0]
        self.doctors = options[1]
        self.options.insert(0, "None")
        self.past_diseases_var1 = tk.StringVar()
        self.past_diseases_var2 = tk.StringVar()
        self.past_diseases_var3 = tk.StringVar()

        self.previous_window.destroy()

        self.root = tk.Tk()
        self.root.title("Sign Up Page")
        self.root.geometry("500x650")
        self.root.configure(bg="#0e1a40")

        # ID label and entry field
        tk.Label(self.root, text="ID:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.13,
                                                                                               anchor="w")
        self.entry_id = tk.Entry(self.root, font=("Segoe UI", 12), bg="white")
        self.entry_id.place(relx=0.5, rely=0.13, anchor="w")

        # Title label
        self.title_label = tk.Label(self.root, text="Sign Up", bg="#0e1a40", fg="white", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Labels
        tk.Label(self.root, text="Username:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1,
                                                                                                     rely=0.23,
                                                                                                     anchor="w")
        tk.Label(self.root, text="Password:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1,
                                                                                                     rely=0.33,
                                                                                                     anchor="w")
        tk.Label(self.root, text="Gender:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.43,
                                                                                                   anchor="w")
        tk.Label(self.root, text="Are you a doctor?", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1,
                                                                                                             rely=0.53,
                                                                                                             anchor="w")

        tk.Label(self.root, text="Past Diseases:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1,
                                                                                                          rely=0.63,
                                                                                                          anchor="w")

        # Entry fields
        self.entry_username = tk.Entry(self.root, font=("Segoe UI", 12), bg="white")
        self.entry_username.place(relx=0.5, rely=0.23, anchor="w")

        self.entry_password = tk.Entry(self.root, font=("Segoe UI", 12), bg="white")
        self.entry_password.place(relx=0.5, rely=0.33, anchor="w")

        self.gender_var = tk.StringVar()
        tk.Radiobutton(self.root, text="Male", variable=self.gender_var, value="Male", bg="white", fg="#CB2525",
                       font=("Segoe UI", 10), selectcolor="#0e1a40", indicatoron=0).place(relx=0.5, rely=0.43,
                                                                                          anchor="w")
        tk.Radiobutton(self.root, text="Female", variable=self.gender_var, value="Female", bg="white", fg="#CB2525",
                       font=("Segoe UI", 10), selectcolor="#0e1a40", indicatoron=0).place(relx=0.65, rely=0.43,
                                                                                          anchor="w")

        self.is_doctor_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Yes", variable=self.is_doctor_var, onvalue=True, offvalue=False, bg="white",
                       fg="#CB2525",
                       font=("Segoe UI", 10), selectcolor="#0e1a40", command=self.toggle_doctor_option).place(relx=0.5,
                                                                                                              rely=0.53,
                                                                                                              anchor="w")

        self.past_diseases_var1 = tk.StringVar(self.root)
        self.past_diseases_var2= tk.StringVar(self.root)
        self.past_diseases_var3= tk.StringVar(self.root)


        self.opt_menu1 = tk.OptionMenu(self.root, self.past_diseases_var1, *self.options)
        self.opt_menu1.config(bg="white")
        self.opt_menu1.place(relx=0.5, rely=0.63, anchor="w")

        self.opt_menu2 = tk.OptionMenu(self.root, self.past_diseases_var2, *self.options)
        self.opt_menu2.config(bg="white")
        self.opt_menu2.place(relx=0.6, rely=0.63, anchor="w")

        self.opt_menu3 = tk.OptionMenu(self.root, self.past_diseases_var3, *self.options)
        self.opt_menu3.setvar("None")
        self.opt_menu3.config(bg="white")
        self.opt_menu3.place(relx=0.7, rely=0.63, anchor="w")

        # Doctor Selection
        self.doctor_label = tk.Label(self.root, text="Choose Doctor:", bg="#0e1a40", fg="white", font=("Segoe UI", 12))
        self.doctor_label.place(relx=0.1, rely=0.73, anchor="w")

        self.doctor_var = tk.StringVar()
        self.doctor_var.set("")

        self.doctor_entry = tk.Entry(self.root, textvariable=self.doctor_var, font=("Segoe UI", 12), bg="white",
                                     width=17,
                                     state="normal")
        self.doctor_entry.place(relx=0.5, rely=0.73, anchor="w")

        self.doctor_listbox = tk.Listbox(self.root, selectmode="single", font=("Segoe UI", 10), bg="white", bd=0,
                                         width=21,
                                         relief="flat", height=2)
        self.doctor_listbox.place(relx=0.5, rely=0.77, anchor="w")
        self.doctor_listbox.bind("<<ListboxSelect>>", self.on_select)

        self.search_doctor()

        self.btn_search_doctor = tk.Button(self.root, text="Search", width=8, font=("Segoe UI", 10), bg="#CB2525",
                                           fg="white", bd=0,
                                           command=self.search_doctor)
        self.btn_search_doctor.place(relx=0.8, rely=0.73, anchor="w")

        self.btn_submit = tk.Button(self.root, text="Submit", width=10, font=("Segoe UI", 12), bg="#CB2525", fg="white",
                                    bd=0,
                                    command=self.submit_signup)
        self.btn_submit.place(relx=0.35, rely=0.9, anchor="center")

        self.btn_login = tk.Button(self.root, text="Login", width=10, font=("Segoe UI", 12), bg="#CB2525", fg="white",
                                   bd=0,
                                   command=self.back_to_login)
        self.btn_login.place(relx=0.7, rely=0.9, anchor="center")

        self.root.mainloop()

    def back_to_login(self):
        """
        Destroys the current window and navigates back to the login page.
        """
        data = encrypt_with_public_key(pickle.dumps(["LOGIN"]), server_public_key)
        self.client_object.send(data)
        self.root.destroy()
        LoginPageGUI(self.client_object, server_public_key, client_private_key)

    def toggle_doctor_option(self):
        """
        Toggles the doctor selection option based on whether the user is a doctor or not.
        """
        if not self.is_doctor_var.get():
            self.doctor_entry.config(state="normal")
            self.doctor_listbox.config(state="normal")
        else:
            self.doctor_entry.delete(0, 'end')
            self.doctor_entry.insert(0, 'Disabled')
            self.doctor_entry.config(state="disabled")
            self.doctor_listbox.config(state="disabled")



    def search_doctor(self):
        """
        Filters the doctor options based on the letters typed by the user.
        If the search query is empty, display all doctors.
        """
        search_query = self.doctor_var.get().lower()
        if search_query:
            filtered_options = [option for option in self.doctors if search_query in option.lower()]
        else:
            filtered_options = self.doctors
        self.doctor_listbox.delete(0, 'end')
        for option in filtered_options:
            self.doctor_listbox.insert('end', option)

    def on_select(self, event):
        """
        Function to handle selection of doctor from the listbox.
        """
        selected = self.doctor_listbox.curselection()
        if selected:
            index = selected[0]
            value = self.doctor_listbox.get(index)
            self.doctor_var.set(value)

    def submit_signup(self):
        """
        Processes the client's sign-up information and sends it to the server.

        Retrieves values from entry fields and option menus, such as first name, last name, gender, username,
        password, user type, and past diseases.
        Sends the client's sign-up information to the server using a predefined format.
        Destroys the sign-up window and navigates back to the login page.
        """
        id = self.entry_id.get()
        gender = self.gender_var.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        is_doctor = self.is_doctor_var.get()
        past_diseases = [
            self.past_diseases_var1.get(),
            self.past_diseases_var2.get(),
            self.past_diseases_var3.get()
        ]
        selected_doctor = self.doctor_var.get()

        if len(id)!=9:
            messagebox.showinfo("Error, Id must be 9 characters long!")
            return
        if not id:
            messagebox.showinfo("Error", "Please enter your ID!")
            return

        if not gender:
            messagebox.showinfo("Error", "Please enter your gender!")
            return

        if not username:
            messagebox.showinfo("Error", "Please enter your username!")
            return
        if not password:
            messagebox.showinfo("Error", "Please enter your password!")
            return

        information = ["SIGNUP", id, gender, username, password, is_doctor, past_diseases, selected_doctor]
        data = encrypt_with_public_key(pickle.dumps(information), server_public_key)
        self.client_object.send(data)
        response = self.client_object.recv(1024)
        response = decrypt_with_private_key(response,client_private_key)
        if "sucsess" in response.decode():
            messagebox.showinfo("Sucsess", "User Created, Please Login!")
            self.root.destroy()
            LoginPageGUI(self.client_object, server_public_key, client_private_key)
        else:
            messagebox.showerror("Error", "Username already exists! Please choose another username")
            return
class DiseaseReportGUI:
    def __init__(self,previous_window, disease_name,client_object,username):
        """
               Initializes the DiseaseReportGUI.

               Parameters:
                   previous_window: The previous Tkinter window to be destroyed.
                   disease_name (str): The name of the disease for the report.
                   client_object: The client object for server communication.
                   username (str): The username of the logged-in user.
        """
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title(f"Report for {disease_name}")
        self.root.geometry("700x750")
        self.root.configure(bg="#0e1a40")

        self.client_object = client_object
        self.advices = client_object.recv(1024)
        self.advices = decrypt_with_private_key(self.advices,client_private_key)
        self.advices = pickle.loads(self.advices)
        self.username = username

        self.title_label = tk.Label(self.root, text=f"Report for {disease_name}", bg="#0e1a40", fg="white",
                                    font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=20)

        self.report_text = tk.Text(self.root, wrap="word", bg="white", fg="#0e1a40", font=("Helvetica", 14), bd=0)
        self.report_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.report_text.insert(tk.END,self.fetch_report(disease_name))



        self.menu_button = tk.Button(self.root, text="Menu", width=10, bg="#CB2525", fg="white",
                                     font=("Helvetica", 12), command=self.go_to_menu)
        self.menu_button.pack(pady=10)

        self.root.mainloop()

    def fetch_report(self, disease_name):
        """
               Fetches the report for the specified disease from Wikipedia and formats it.

               Parameters:
                   disease_name (str): The name of the disease to fetch the report for.

               Returns:
                   str: The formatted disease report.
               """
        url = f"https://en.wikipedia.org/wiki/{disease_name}"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find(id="mw-content-text")
        paragraphs = content_div.find_all('p')

        report = ""

        for i in range(1, 3):
            try:
                report += paragraphs[i].get_text() + "\n\n"
            except Exception as e:
                print(disease_name)

        report+="Our Advices :" + "\n"

        number = 1
        for advice in self.advices:
            report+=str(number)+ "- " +advice + "\n"
            number = int(number) + 1

        if report == "Error: list index out of range" or report=="":
            print(disease_name)
        return report

    def go_to_menu(self):
        """
        Sends a request to the server to return to the main menu.
        """
        data = encrypt_with_public_key("menu".encode(),server_public_key)
        self.client_object.send(data)
        MainMenuGUI(self.client_object,self.root,self.username)

class MessagesGUI:
    def __init__(self,previous_window,client_object,username):
        """
               Initializes the MessagesGUI.

               Parameters:
                   previous_window: The previous Tkinter window to be destroyed.
                   client_object: The client object for server communication.
                   username (str): The username of the logged-in user.
        """
        self.client_object = client_object
        self.username = username
        data = client_object.recv(1024)
        data = decrypt_with_private_key(data , client_private_key)
        self.messages = pickle.loads(data)


        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title("Messages")
        self.root.geometry("600x500")
        self.root.configure(bg="#0e1a40")

        self.title_label = tk.Label(self.root, text="Messages", font=("Helvetica", 16, "bold"), bg="#0e1a40", fg="white")
        self.title_label.pack(pady=10)

        self.messages_frame = tk.Frame(self.root)
        self.messages_frame.pack(fill=tk.BOTH, expand=True)

        self.messages_listbox = tk.Listbox(self.messages_frame, width=60, height=10, bg="#0e1a40", fg="white")
        self.messages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.messages_frame, orient=tk.VERTICAL, command=self.messages_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messages_listbox.config(yscrollcommand=self.scrollbar.set)

        if self.messages==[]:
            self.msg_label = tk.Label(self.root, text="You don't have any messages yet!", font=("Helvetica", 16, "bold"), bg="#0e1a40",
                                        fg="white")
            self.msg_label.pack(pady=10)

        self.load_messages()

        self.messages_listbox.bind("<<ListboxSelect>>", self.show_message_content)

        self.message_content_text = tk.Text(self.root, width=60, height=10, wrap=tk.WORD, bg="#0e1a40", fg="white")
        self.message_content_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.menu_button = tk.Button(self.root, text="Menu", width=10, command= lambda : self.menu(client_object), bg="#CB2525", fg="white")
        self.menu_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        self.reply_button = tk.Button(self.root, text="Reply", width=10, command=lambda: self.reply_message(client_object),
                                      bg="#CB2525", fg="white")
        self.reply_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))
        self.delete_button = tk.Button(self.root, text="Delete", width=10,
                                      command=lambda: self.delete_message(client_object),
                                      bg="#CB2525", fg="white")
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

    def load_messages(self):
        """
                Loads messages into the messages listbox.
        """
        for message in self.messages:
            self.messages_listbox.insert(tk.END, f"From: {message['sender']} - Subject: {message['subject']}")


    def reply_message(self,client_object):
        """
                Sends a reply to the selected message.

                Parameters:
                    client_object: The client object for server communication.
        """
        selected_index = self.messages_listbox.curselection()

        message_to_reply = self.messages[selected_index[0]]
        data = ["reply",message_to_reply]
        data = encrypt_with_public_key(pickle.dumps(data),server_public_key)
        self.client_object.send(data)
        SendMessageGUI(None,client_object,self.username,message_to_reply['sender'])

    def delete_message(self,client_object):
        """
                Deletes the selected message.

                Parameters:
                    client_object: The client object for server communication.
                """
        selected_index = self.messages_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "Select a message!")
            return
        message_to_reply = self.messages[selected_index[0]]
        print(selected_index,message_to_reply)
        data = ["delete",message_to_reply['sender'],message_to_reply['subject']]
        data = encrypt_with_public_key(pickle.dumps(data), server_public_key)
        self.client_object.send(data)
        self.messages_listbox.delete(selected_index)
        self.message_content_text.delete('1.0', tk.END)
        messagebox.showinfo("Success", "Message Removed successfully!")

    def show_message_content(self, event):
        """
          Displays the content of the selected message.

          Parameters:
              event: The event triggering the function.
          """
        selection = self.messages_listbox.curselection()
        if selection:
            message_index = selection[0]
            message = self.messages[message_index]
            self.message_content_text.delete('1.0', tk.END)
            self.message_content_text.insert(tk.END,
                                             f"From: {message['sender']}\nSubject: {message['subject']}\n\n{message['message']}")

    def menu(self,client_object):
        """
        Sends a request to return to the main menu.

        Parameters:
            client_object: The client object for server communication.
        """
        data = encrypt_with_public_key(pickle.dumps(["menu"]),server_public_key)
        self.client_object.send((data))

        data = self.client_object.recv(1024)
        data = decrypt_with_private_key(data , client_private_key)
        if "DOCTOR" in data.decode():
            MainMenuGUI(client_object,self.root,self.username)
        else:
            MainMenuGUI(client_object,self.root,self.username)

    def delete(self):
        """
        Deletes the selected message.
        """
        selected_index = self.messages_listbox.curselection()
        if selected_index:
            self.messages_listbox.delete(selected_index)
            print("Message deleted successfully.")
        else:
            print("Please select a message to delete.")

    def run(self):
        """
        Runs the Tkinter event loop.
        """
        self.root.mainloop()

class SendMessageGUI:
    def __init__(self, previous_window, client_object, username, recipient):
        """
        Initializes the SendMessageGUI.

        Parameters:
            previous_window: The previous Tkinter window to be destroyed.
            client_object: The client object for server communication.
            username (str): The username of the logged-in user.
            recipient (str): The recipient of the message.
        """
        self.client_object = client_object
        try:
            previous_window.destroy()
        except AttributeError:
            pass
        self.root = tk.Tk()
        self.root.title("Send Message")
        self.root.geometry("500x250")
        self.root.configure(bg="#0e1a40")
        self.username = username
        self.recipient = recipient
        self.title_label = tk.Label(self.root, text="Send Message", bg="#0e1a40", fg="white",
                                    font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='n')

        self.recipient_label = tk.Label(self.root, text="Recipient:", bg="#0e1a40", fg="white",
                                        font=("Helvetica", 12))
        self.recipient_label.grid(row=1, column=0, sticky='E', pady=5)

        data = self.client_object.recv(1024)
        data = decrypt_with_private_key(data , client_private_key)
        self.options = pickle.loads(data)
        self.recipient_var = tk.StringVar(self.root)
        self.recipient_var.set(recipient)



        self.opt_menu1 = tk.OptionMenu(self.root, self.recipient_var, *self.options)
        self.opt_menu1.config(bg="white")


        self.opt_menu1.grid(row=1, column=1, pady=5)

        self.subject_label = tk.Label(self.root, text="Subject:", bg="#0e1a40", fg="white", font=("Helvetica", 12))
        self.subject_label.grid(row=2, column=0, sticky='E', pady=5)

        self.subject_entry = tk.Entry(self.root, width=30, bg="white", fg="black", font=("Helvetica", 12))
        self.subject_entry.grid(row=2, column=1, pady=5)

        self.message_label = tk.Label(self.root, text="Message:", bg="#0e1a40", fg="white", font=("Helvetica", 12))
        self.message_label.grid(row=3, column=0, sticky='E')

        self.message_entry = tk.Text(self.root, width=34, height=3, bg="white", fg="black")
        self.message_entry.grid(row=3, column=1, pady=7, rowspan=3, ipady=10)

        self.send_button = tk.Button(self.root, text="Send", height=1, width=10, bg="#CB2525", fg="white",
                                         font=("Helvetica", 12), command=self.send_message)
        self.send_button.grid(row=7, column=0, padx=5, pady=5)
        if recipient==" ":

            self.menu_button = tk.Button(self.root, text="Menu", height=1, width=10, bg="#CB2525", fg="white",
                                         font=("Helvetica", 12), command=lambda: self.go_to_menu(client_object, username))
            self.menu_button.grid(row=7, column=1, padx=5, pady=5)

    def send_message(self):
        """
        Sends the composed message to the recipient.

        If recipient is set, sends the message and closes the window. Otherwise, sends the message and stays on the window.
        """
        receiver = self.recipient_var.get()
        subject = self.subject_entry.get()
        message = self.message_entry.get("1.0", tk.END)
        message_pattern = ["Send Message",receiver, subject, message]
        message_pattern = encrypt_with_public_key(pickle.dumps(message_pattern),server_public_key)
        self.client_object.send(message_pattern)


        self.subject_entry.delete(0, tk.END)
        self.message_entry.delete("1.0", tk.END)

        messagebox.showinfo("Success", "Message sent successfully!")

        if self.recipient!=" ":
            self.client_object.send(encrypt_with_public_key(pickle.dumps(["back"]),server_public_key))
            self.root.destroy()


    def go_to_menu(self, client_object, username):
        """
        Navigates to the main menu.

        Parameters:
            client_object: The client object for server communication.
            username (str): The username of the logged-in user.
        """
        print("menu")
        data = encrypt_with_public_key(pickle.dumps(["menu"]),server_public_key)
        print(data)
        client_object.send(data)


        data = self.client_object.recv(1024)
        data = decrypt_with_private_key(data , client_private_key)
        print(data)
        if "DOCTOR" in data.decode():
            MainMenuGUI(client_object,self.root,self.username)
        else:
            MainMenuGUI(client_object,self.root,self.username)

        self.root.mainloop()

if __name__ == "__main__":
    client_socket = start_client()
    LoginPageGUI(client_socket[0],client_socket[1],client_socket[2])
