import tkinter as tk

class MessagesGUI:
    def __init__(self):
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

        self.reply_button = tk.Button(self.root, text="Reply", width=10, command=self.reply , bg="#d81159", fg="white")
        self.reply_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        self.delete_button = tk.Button(self.root, text="Delete", width=10, command=self.delete, bg="#d81159", fg="white")
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

    def load_messages(self):
        # Simulated messages
        self.messages = [
            {"sender": "User1", "subject": "Question about prescription", "message": "Hello, doctor! I have a question about my prescription."},
            {"sender": "User2", "subject": "Appointment Request", "message": "Dear Doctor, I would like to schedule an appointment."},
            {"sender": "User3", "subject": "Feedback", "message": "Hi, I just wanted to give some feedback on my recent visit."},
        ]

        for message in self.messages:
            self.messages_listbox.insert(tk.END, f"From: {message['sender']} - Subject: {message['subject']}")

    def show_message_content(self, event):
        selection = self.messages_listbox.curselection()
        if selection:
            message_index = selection[0]
            message = self.messages[message_index]
            self.message_content_text.delete('1.0', tk.END)
            self.message_content_text.insert(tk.END, f"From: {message['sender']}\nSubject: {message['subject']}\n\n{message['message']}")

    def reply(self):
        selected_index = self.messages_listbox.curselection()
        if selected_index:
            sender = self.messages_listbox.get(selected_index).split(" - ")[0].split(": ")[1]
            print(f"Replying to message from {sender}")
        else:
            print("Please select a message to reply to.")

    def delete(self):
        selected_index = self.messages_listbox.curselection()
        if selected_index:
            self.messages_listbox.delete(selected_index)
            print("Message deleted successfully.")
        else:
            print("Please select a message to delete.")

    def run(self):
        self.root.mainloop()

class SendMessageGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Send Message")
        self.root.geometry("400x300")
        self.root.configure(bg="#0e1a40")

        self.title_label = tk.Label(self.root, text="Send Message", bg="#0e1a40", fg="white",
                                    font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.message_label = tk.Label(self.root, text="Message:", bg="#0e1a40", fg="white", font=("Helvetica", 12))
        self.message_label.pack(pady=5)

        self.message_entry = tk.Text(self.root, width=40, height=10, bg="white", fg="black")
        self.message_entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send", width=10, bg="#d81159", fg="white", font=("Helvetica", 12),
                                     command=self.send_message)
        self.send_button.pack(pady=10)

    def send_message(self):
        message = self.message_entry.get("1.0", tk.END)
        # Here you can add code to send the message to the doctor
        print("Message sent:", message)

    def run(self):
        self.root.mainloop()



