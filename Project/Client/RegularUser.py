import pickle
import tkinter as tk
from tkinter import messagebox
from Project.Server import Examinor
import requests
from bs4 import BeautifulSoup



class LoginPageGUI:
    def __init__(self, client_object):
        self.client_object = client_object

        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("550x400")
        self.root.configure(bg="#0e1a40")

        self.frame = tk.Frame(self.root, padx=20, pady=20, bg="#0e1a40")
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Login", font=("Segoe UI", 20, "bold"), bg="#0e1a40", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.username_label = tk.Label(self.frame, text="Username:", font=("Segoe UI", 12, "bold"), bg="#0e1a40",
                                       fg="white")
        self.username_label.grid(row=1, column=0, pady=5, sticky="e")

        self.username_entry = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.password_label = tk.Label(self.frame, text="Password:", font=("Segoe UI", 12, "bold"), bg="#0e1a40",
                                       fg="white")
        self.password_label.grid(row=2, column=0, pady=5, sticky="e")

        self.password_entry = tk.Entry(self.frame, show="*", font=("Segoe UI", 12))
        self.password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbutton = tk.Checkbutton(self.frame, text="Show Password",
                                                        variable=self.show_password_var,
                                                        font=("Segoe UI", 10, "bold"), bg="#0e1a40", fg="#d81159",
                                                        activebackground="#0e1a40", activeforeground="#d81159",
                                                        command=self.toggle_password_visibility)
        self.show_password_checkbutton.grid(row=3, column=1, pady=5, sticky="w")

        self.login_button = tk.Button(self.frame, text="Login", command=self.send_data, font=("Segoe UI", 10, "bold"),
                                      bg="#d81159",
                                      fg="white", padx=5, pady=3)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.signup_button = tk.Button(self.frame, command=self.open_signup_page, text="Signup",
                                       font=("Segoe UI", 10, "bold"), bg="#d81159", fg="white", padx=5, pady=3)
        self.signup_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.root.mainloop()

    def toggle_password_visibility(self):
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
        self.client_object.send(pickle.dumps(information))
        response = self.client_object.recv(1024).decode()
        if response == "Correct":
            MainMenuGUI(self.client_object, self.root,username)
        else:
            messagebox.showinfo("Error", "Incorrect password, Try Again!")

    def open_signup_page(self):
        SignUpPageGUI(self.root,self.client_object)

class MainMenuGUI:
    def __init__(self,client_object,previous_window,username):
        self.username = username
        self.client_object = client_object
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.root.geometry("400x200")
        self.root.configure(bg="#0e1a40")

        self.title_label = tk.Label(self.root, text="Menu", bg="#0e1a40", fg="white", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.examine_button = tk.Button(self.root, text="Examine", width=15, bg="#d81159", fg="white",
                                        font=("Helvetica", 12), command= lambda: self.open_examine(client_object))
        self.examine_button.pack(pady=10)

        self.messages_button = tk.Button(self.root, text="Messages", width=15, bg="#d81159", fg="white",
                                         font=("Helvetica", 12), command=lambda: self.open_messages(client_object))
        self.messages_button.pack(pady=10)

    def open_examine(self,client_object):
        self.client_object.send("examine".encode())
        FirstSymptomWindowGUI(self.root,self.client_object,self.username)
        print("Opening Examine window")

    def open_messages(self,client_object):
        self.client_object.send("messages".encode())
        MessagesMenu(self.root,client_object,self.username)
        print("Opening Messages window")

    def run(self):
        self.root.mainloop()
class FirstSymptomWindowGUI:
    def __init__(self, previous_window, client_object,username):
        self.username = username
        self.previous_window = previous_window
        self.client_object = client_object

        self.previous_window.destroy()

        self.root = tk.Tk()
        self.root.title("Second GUI Example")
        self.root.geometry("550x400")
        self.root.configure(bg="#0e1a40")

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#0e1a40", highlightthickness=0)
        self.canvas.pack()

        self.center_x = self.canvas.winfo_reqwidth() / 2
        self.center_y = self.canvas.winfo_reqheight() / 2

        self.plus = self.canvas.create_line(self.center_x - 50, self.center_y, self.center_x + 50, self.center_y,
                                            fill="red", width=20)
        self.plus = self.canvas.create_line(self.center_x, self.center_y - 50, self.center_x, self.center_y + 50,
                                            fill="red", width=20)

        self.title_label = tk.Label(self.root, text="Enter your first symptom", bg="#0e1a40", fg="white",
                                    font=("Segoe UI", 18, "bold"))
        self.title_label.place(relx=0.5, rely=0.6, anchor="center")

        self.options_list = Examinor.get_all_symptoms()

        self.value_inside = tk.StringVar(self.root)
        self.question_menu = tk.OptionMenu(self.root, self.value_inside, *self.options_list)
        self.question_menu.place(relx=0.5, rely=0.75, anchor="center")

        self.btn_enter = tk.Button(self.root, text="Enter", width=10, font=("Segoe UI", 12, "bold"), bg="#d81159",
                                   fg="white", bd=0,
                                   command=self.on_enter)
        self.btn_enter.place(relx=0.5, rely=0.9, anchor="center")

        self.root.mainloop()

    def on_enter(self):
        """
        Sends the selected symptom to the server and proceeds to the questionnaire window.
        """
        information = self.value_inside.get()
        self.client_object.send(information.encode())
        question = self.client_object.recv(1024).decode()
        QuestionnaireWindowGUI(self.root, self.client_object, question,self.username)

class QuestionnaireWindowGUI:
    def __init__(self, previous_window, client_object, question, username):
        self.username = username
        self.previous_window = previous_window
        self.client_object = client_object
        self.question = question

        self.previous_window.destroy()

        self.root = tk.Tk()
        self.root.title("Questionnaire")
        self.root.geometry("600x400")
        self.root.configure(bg="#0e1a40")

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#0e1a40", highlightthickness=0)
        self.canvas.pack()

        self.center_x = self.canvas.winfo_reqwidth() / 2
        self.center_y = self.canvas.winfo_reqheight() / 2

        self.plus = self.canvas.create_line(self.center_x - 50, self.center_y, self.center_x + 50, self.center_y,
                                            fill="red", width=20)
        self.plus = self.canvas.create_line(self.center_x, self.center_y - 50, self.center_x, self.center_y + 50,
                                            fill="red", width=20)

        self.question_label = tk.Label(self.root, text=self.question, bg="#0e1a40", fg="white",
                                       font=("Segoe UI", 16, "bold"))
        self.question_label.pack(pady=20)

        self.btn_frame = tk.Frame(self.root, bg="#0e1a40")
        self.btn_frame.pack(expand=True)

        self.btn_yes = tk.Button(self.btn_frame, bg="#d81159", font=("Segoe UI", 12, "bold"), fg="white",
                                 text="Yes", width=10, height=3, command=self.on_yes)
        self.btn_yes.pack(side=tk.LEFT, padx=(50, 10))

        self.btn_no = tk.Button(self.btn_frame, bg="#d81159", font=("Segoe UI", 12, "bold"), fg="white", text="No",
                                width=10, height=3, command=self.on_no)
        self.btn_no.pack(side=tk.RIGHT, padx=(10, 50))

        self.root.mainloop()

    def show_text(self, question1):
        """
        Displays the provided question or result text in the GUI window.

        Parameters:
            question1 (str): The question or result text to be displayed.
        """
        try:
            self.question_label.destroy()
        except tk.TclError:
            pass
        if not "You have" in question1:
            self.question_label = tk.Label(self.root, text=question1, bg="#0e1a40", fg="white",
                                           font=("Segoe UI", 16, "bold"))
            self.question_label.pack(pady=20)
            symptom = question1[18:len(question1) - 2]
            print(symptom)

        else:

            self.question_label = tk.Label(self.root, text=question1, bg="#0e1a40", fg="#d81159",
                                           font=("Segoe UI", 14, "bold"))
            self.question_label.pack(pady=20)
            self.btn_no.destroy()
            self.btn_yes.destroy()
            self.btn_try_again = tk.Button(self.btn_frame, bg="#d81159", font=("Segoe UI", 12, "bold"), fg="white",
                                           text="Menu", width=10,
                                           height=3, command=lambda: self.back_to_menu())
            self.btn_try_again.pack(side=tk.LEFT, padx=(50, 10))
            print(question1[9:].lower())
            self.btn_more_info = tk.Button(self.btn_frame, bg="#d81159", font=("Segoe UI", 12, "bold"), fg="white",
                                           text="More Information", width=15,
                                           height=3, command=lambda: self.go_to_info(question1[9:].lower()))
            self.btn_more_info.pack(side=tk.RIGHT, padx=(10, 50))

    def back_to_menu(self):
        response = messagebox.askquestion("Confirmation", "Do you want your results to be reviewed by a Doctor?")
        self.client_object.send(pickle.dumps(["Menu", response]))
        MainMenuGUI(self.client_object, self.root, self.username)

    def go_to_info(self, disease):
        response = messagebox.askquestion("Confirmation", "Do you want your results to be reviewed by a Doctor?")
        self.client_object.send(pickle.dumps(["Information", response]))
        DiseaseReportGUI(self.root, disease, self.client_object, self.username)

    def on_yes(self):
        """
        Sends the client's 'Yes' response to the server and displays the result accordingly.
        """
        self.client_object.send("yes".encode())
        result = self.client_object.recv(1024).decode()
        self.show_text(result)

    def on_no(self):
        """
        Sends the client's 'No' response to the server and displays the result accordingly.
        """
        self.client_object.send("no".encode())
        result = self.client_object.recv(1024).decode()
        self.show_text(result)
class SignUpPageGUI:
    def __init__(self, previous_window, client_object):
        self.previous_window = previous_window
        self.client_object = client_object
        self.options = Examinor.get_all_diseases()
        self.options.insert(0, "None")
        self.past_diseases_var1 = tk.StringVar()
        self.past_diseases_var2 = tk.StringVar()
        self.past_diseases_var3 = tk.StringVar()

        self.previous_window.destroy()

        self.root = tk.Tk()
        self.root.title("Sign Up Page")
        self.root.geometry("500x650")
        self.root.configure(bg="#0e1a40")

        # Title label
        self.title_label = tk.Label(self.root, text="Sign Up", bg="#0e1a40", fg="white", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Labels
        tk.Label(self.root, text="First Name:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.15, anchor="w")
        tk.Label(self.root, text="Last Name:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.25, anchor="w")
        tk.Label(self.root, text="Gender:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.35, anchor="w")
        tk.Label(self.root, text="Are you a doctor?", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.45, anchor="w")
        tk.Label(self.root, text="Username:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.55, anchor="w")
        tk.Label(self.root, text="Password:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.65, anchor="w")
        tk.Label(self.root, text="Past Diseases:", bg="#0e1a40", fg="white", font=("Segoe UI", 12)).place(relx=0.1, rely=0.75, anchor="w")

        # Entry fields
        self.entry_first_name = tk.Entry(self.root, font=("Segoe UI", 12), bg="white")
        self.entry_first_name.place(relx=0.5, rely=0.15, anchor="w")

        self.entry_last_name = tk.Entry(self.root, font=("Segoe UI", 12), bg="white")
        self.entry_last_name.place(relx=0.5, rely=0.25, anchor="w")

        self.gender_var = tk.StringVar()
        tk.Radiobutton(self.root, text="Male", variable=self.gender_var, value="Male", bg="white", fg="#d81159",
                       font=("Segoe UI", 10), selectcolor="#0e1a40", indicatoron=0).place(relx=0.5, rely=0.35, anchor="w")
        tk.Radiobutton(self.root, text="Female", variable=self.gender_var, value="Female", bg="white", fg="#d81159",
                       font=("Segoe UI", 10), selectcolor="#0e1a40", indicatoron=0).place(relx=0.65, rely=0.35, anchor="w")

        self.is_doctor_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Yes", variable=self.is_doctor_var, onvalue=True, offvalue=False, bg="white", fg="#d81159",
                       font=("Segoe UI", 10), selectcolor="#0e1a40").place(relx=0.5, rely=0.45, anchor="w")

        self.entry_username = tk.Entry(self.root, font=("Segoe UI", 12), bg="white")
        self.entry_username.place(relx=0.5, rely=0.55, anchor="w")

        self.entry_password = tk.Entry(self.root, show="*", font=("Segoe UI", 12), bg="white")
        self.entry_password.place(relx=0.5, rely=0.65, anchor="w")

        self.past_diseases_var1.set("None")
        self.past_diseases_var2.set("None")
        self.past_diseases_var3.set("None")

        self.opt_menu1 = tk.OptionMenu(self.root, self.past_diseases_var1, *self.options)
        self.opt_menu1.config(bg="white")
        self.opt_menu1.place(relx=0.5, rely=0.75, anchor="w")

        self.opt_menu2 = tk.OptionMenu(self.root, self.past_diseases_var2, *self.options)
        self.opt_menu2.config(bg="white")
        self.opt_menu2.place(relx=0.6, rely=0.75, anchor="w")

        self.opt_menu3 = tk.OptionMenu(self.root, self.past_diseases_var3, *self.options)
        self.opt_menu3.setvar("None")
        self.opt_menu3.config(bg="white")
        self.opt_menu3.place(relx=0.7, rely=0.75, anchor="w")


        self.btn_submit = tk.Button(self.root, text="Submit", width=10, font=("Segoe UI", 12), bg="#d81159", fg="white", bd=0,
                                    command=self.submit_signup)
        self.btn_submit.place(relx=0.4, rely=0.95, anchor="center")

        self.btn_login = tk.Button(self.root, text="Login", width=10, font=("Segoe UI", 12), bg="#d81159", fg="white", bd=0,
                                   command=self.back_to_login
                                   )
        self.btn_login.place(relx=0.7, rely=0.95, anchor="center")

        self.root.mainloop()

    def back_to_login(self):
        """
        Destroys the current window and navigates back to the login page.
        """
        self.root.destroy()
        LoginPageGUI(self.client_object)

    def submit_signup(self):
        """
        Processes the client's sign-up information and sends it to the server.

        Retrieves values from entry fields and option menus, such as first name, last name, gender, username,
        password, user type, and past diseases.
        Sends the client's sign-up information to the server using a predefined format.
        Destroys the sign-up window and navigates back to the login page.
        """
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        gender = self.gender_var.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        is_doctor = self.is_doctor_var.get()
        past_diseases = [
            self.past_diseases_var1.get(),
            self.past_diseases_var2.get(),
            self.past_diseases_var3.get()
        ]

        if not first_name:
            messagebox.showinfo("Error", "Please enter your first name!")
            return
        if not last_name:
            messagebox.showinfo("Error", "Please enter your last name!")
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

        information = ["SIGNUP", first_name, last_name, gender, username, password, is_doctor, past_diseases]

        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Gender:", gender)
        print("Is Doctor:", is_doctor)
        print("Username:", username)
        print("Password:", password)
        print("Past Diseases:", past_diseases)

        print(information)

        self.client_object.send(pickle.dumps(information))
        self.root.destroy()
        LoginPageGUI(self.client_object)

class DiseaseReportGUI:
    def __init__(self,previous_window, disease_name,client_object,username):
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title(f"Report for {disease_name}")
        self.root.geometry("700x750")
        self.root.configure(bg="#0e1a40")

        self.client_object = client_object
        self.advices = client_object.recv(1024)
        self.advices = pickle.loads(self.advices)
        self.username = username

        self.title_label = tk.Label(self.root, text=f"Report for {disease_name}", bg="#0e1a40", fg="white",
                                    font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=20)

        self.report_text = tk.Text(self.root, wrap="word", bg="white", fg="#0e1a40", font=("Helvetica", 14), bd=0)
        self.report_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.report_text.insert(tk.END,self.fetch_report(disease_name))



        self.menu_button = tk.Button(self.root, text="Menu", width=10, bg="#d81159", fg="white",
                                     font=("Helvetica", 12), command=self.show_menu)
        self.menu_button.pack(pady=10)

        self.root.mainloop()

    def fetch_report(self, disease_name):

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

    def show_menu(self):
        self.client_object.send("menu".encode())
        MainMenuGUI(self.client_object,self.root,self.username)
        print("Menu button clicked")


class MessagesGUI:
    def __init__(self,previous_window,client_object,username):
        self.client_object = client_object
        self.username = username
        data = client_object.recv(1024)
        self.messages = pickle.loads(data)
        print(self.messages)
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title("Messages")
        self.root.geometry("600x450")
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

        self.load_messages()

        self.messages_listbox.bind("<<ListboxSelect>>", self.show_message_content)

        self.message_content_text = tk.Text(self.root, width=60, height=10, wrap=tk.WORD, bg="#0e1a40", fg="white")
        self.message_content_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.menu_button = tk.Button(self.root, text="Menu", width=10, command= lambda : self.menu(client_object), bg="#d81159", fg="white")
        self.menu_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        self.delete_button = tk.Button(self.root, text="Delete", width=10, command=self.delete, bg="#d81159", fg="white")
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        self.reply_button = tk.Button(self.root, text="Reply", width=10, command=lambda: self.reply_message(client_object),
                                      bg="#d81159", fg="white")
        self.reply_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

    def load_messages(self):
        # self.messages = [
        #     {"sender": "User1", "subject": "Question about prescription", "message": "Hello, doctor! I have a question about my prescription."},
        #     {"sender": "User2", "subject": "Appointment Request", "message": "Dear Doctor, I would like to schedule an appointment."},
        #     {"sender": "User3", "subject": "Feedback", "message": "Hi, I just wanted to give some feedback on my recent visit."},
        # ]

        for message in self.messages:
            self.messages_listbox.insert(tk.END, f"From: {message['sender']} - Subject: {message['subject']}")


    def reply_message(self,client_object):
        selected_index = self.messages_listbox.curselection()
        message_to_reply = self.messages[selected_index[0]]
        data = ["reply",message_to_reply]
        self.client_object.send(pickle.dumps(data))
        SendMessageGUI(self.root,client_object,self.username,message_to_reply['sender'])
    def show_message_content(self, event):
        selection = self.messages_listbox.curselection()
        if selection:
            message_index = selection[0]
            message = self.messages[message_index]
            self.message_content_text.delete('1.0', tk.END)
            self.message_content_text.insert(tk.END, f"From: {message['sender']}\nSubject: {message['subject']}\n\n{message['message']}")

    def menu(self,client_object):
        self.client_object.send(pickle.dumps(["menu"]))
        MessagesMenu(self.root,client_object,self.username)

    def delete(self):
        selected_index = self.messages_listbox.curselection()
        if selected_index:
            self.messages_listbox.delete(selected_index)
            print("Message deleted successfully.")
        else:
            print("Please select a message to delete.")

    def run(self):
        self.root.mainloop()


from tkinter import messagebox


class SendMessageGUI:
    def __init__(self, previous_window, client_object, username, recipient):
        self.client_object = client_object
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title("Send Message")
        self.root.geometry("500x250")
        self.root.configure(bg="#0e1a40")

        self.title_label = tk.Label(self.root, text="Send Message", bg="#0e1a40", fg="white",
                                    font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='n')

        self.recipient_label = tk.Label(self.root, text="Recipient:", bg="#0e1a40", fg="white",
                                        font=("Helvetica", 12))
        self.recipient_label.grid(row=1, column=0, sticky='E', pady=5)

        self.recipient_entry = tk.Entry(self.root, width=30, bg="white", fg="black", font=("Helvetica", 12))
        self.recipient_entry.insert(tk.END, recipient)  # Default text
        self.recipient_entry.grid(row=1, column=1, pady=5)

        self.subject_label = tk.Label(self.root, text="Subject:", bg="#0e1a40", fg="white", font=("Helvetica", 12))
        self.subject_label.grid(row=2, column=0, sticky='E', pady=5)

        self.subject_entry = tk.Entry(self.root, width=30, bg="white", fg="black", font=("Helvetica", 12))
        self.subject_entry.grid(row=2, column=1, pady=5)

        self.message_label = tk.Label(self.root, text="Message:", bg="#0e1a40", fg="white", font=("Helvetica", 12))
        self.message_label.grid(row=3, column=0, sticky='E')

        self.message_entry = tk.Text(self.root, width=34, height=3, bg="white", fg="black")
        self.message_entry.grid(row=3, column=1, pady=7, rowspan=3, ipady=10)

        self.send_button = tk.Button(self.root, text="Send", height=1, width=10, bg="#d81159", fg="white",
                                     font=("Helvetica", 12), command=self.send_message)
        self.send_button.grid(row=7, column=0, padx=5, pady=5)

        self.menu_button = tk.Button(self.root, text="Menu", height=1, width=10, bg="#d81159", fg="white",
                                     font=("Helvetica", 12), command=lambda: self.menu(client_object, username))
        self.menu_button.grid(row=7, column=1, padx=5, pady=5)

    def send_message(self):
        recipient = self.recipient_entry.get()
        subject = self.subject_entry.get()
        message = self.message_entry.get("1.0", tk.END)
        message_pattern = [recipient, subject, message]
        self.client_object.send(pickle.dumps(message_pattern))
        print("Recipient:", recipient)
        print("Subject:", subject)
        print("Message:", message)

        self.recipient_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.message_entry.delete("1.0", tk.END)

        messagebox.showinfo("Success", "Message sent successfully!")

    def menu(self, client_object, username):
        client_object.send(pickle.dumps(["menu"]))
        MessagesMenu(self.root, client_object, username)

    def run(self):
        self.root.mainloop()


class MessagesMenu:
    def __init__(self,previous_window,client_object,username):
        previous_window.destroy()
        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.root.geometry("400x200")
        self.root.configure(bg="#0e1a40")

        self.title_label = tk.Label(self.root, text="Menu", bg="#0e1a40", fg="white", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.examine_button = tk.Button(self.root, text="Send Message", width=15, bg="#d81159", fg="white",
                                        font=("Helvetica", 12), command= lambda: self.open_sender(client_object,username))
        self.examine_button.pack(pady=10)

        self.messages_button = tk.Button(self.root, text="Your Messages", width=15, bg="#d81159", fg="white",
                                         font=("Helvetica", 12), command=lambda: self.open_messages(client_object,username))
        self.messages_button.pack(pady=10)

        self.messages_button = tk.Button(self.root, text="Main Menu", width=15, bg="#d81159", fg="white",
                                         font=("Helvetica", 12),
                                         command= lambda : self.back_to_menu(client_object,username))
        self.messages_button.pack(pady=10)

    def back_to_menu(self,client_object,username):
        client_object.send("menu".encode())
        MainMenuGUI(client_object,self.root,username)
    def open_sender(self,client_object,username):
        client_object.send("send message".encode())
        SendMessageGUI(self.root,client_object,username,'')
        print("Opening Examine window")

    def open_messages(self,client_object,username):
        client_object.send("view messages".encode())
        MessagesGUI(self.root,client_object,username)
        print("Opening Messages window")
    def run(self):
        self.root.mainloop()



