import tkinter as tk
import tkinter.font as tkFont
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from  SenderClient import *
from aes import *

class App:
    sender = ""
    password = ""
    tovar = ""

    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")
        self.root.resizable(width=False, height=False)

        # Create email label and entry field
        label_email = tk.Label(self.root, text="Email:")
        label_email.pack()
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        # Create password label and entry field
        label_password = tk.Label(self.root, text="Password:")
        label_password.pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        # Create login button
        button_login = tk.Button(self.root, text="Login", command=self.SecondWindow)
        button_login.pack()

    def SecondWindow(self):
        self.sender = self.entry_email.get()
        self.password = self.entry_password.get()

        # Hide the login window
        self.root.withdraw()

        # Create the second window
        second_window = tk.Toplevel()
        second_window.title("Secure Mail Composer")

        # Set window size and position
        width = 600
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        second_window.geometry(alignstr)
        second_window.resizable(width=False, height=False)

        ft = tkFont.Font(family='Times', size=12)

        label_To = tk.Label(second_window)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40, y=40, width=70, height=25)

        label_Subject = tk.Label(second_window)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40, y=90, width=70, height=25)

        self.email_To = tk.Entry(second_window, textvariable=self.tovar)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120, y=40, width=420, height=30)

        self.email_Subject = tk.Entry(second_window)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120, y=90, width=417, height=30)

        self.email_Body = tk.Text(second_window)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50, y=140, width=500, height=302)

        button_Send = tk.Button(second_window)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470, y=460, width=70, height=25)
        button_Send["command"] = self.button_Send_command

    def send_email(self, subject, body, attach, recipients):
        with open("../TextFiles/RealMessage.txt", 'w') as outfile:
            outfile.write(body)

        session_key_sender, encrypted_session_key_receiver=start_client("localhost", 65535)

        with open("../TextFiles/ReceiverEncryptedKey.txt", 'wb') as outfile:
            outfile.write(encrypted_session_key_receiver)

        encrypt_file(session_key_sender,"../TextFiles/RealMessage.txt","../TextFiles/EncryptedMessage.txt")
        with open("../TextFiles/EncryptedMessage.txt", 'r') as infile:
            EncryptedBody=infile.read()


        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipients
        msg.attach(MIMEText("This is a dummy email"))

        part = MIMEApplication(EncryptedBody, Name="EncyptedMessageBody.txt")
        part['Content-Disposition'] = 'attachment; filename=EncyptedMessageBody.txt'
        msg.attach(part)

        part = MIMEApplication(encrypted_session_key_receiver, Name="wrappedkey.txt")
        part['Content-Disposition'] = 'attachment; filename=wrappedkey.txt'
        msg.attach(part)

        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp_server.starttls()
        smtp_server.login(self.sender, self.password)
        print("Login done")
        smtp_server.sendmail(self.sender, recipients, msg.as_string())
        print("Mail sent")
        smtp_server.quit()

    def button_Send_command(self):
        tovar = self.email_To.get()
        subject = self.email_Subject.get()
        body = self.email_Body.get("1.0", "end")
        att = "Place holder for the key"
        self.send_email(subject, body, att, tovar)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
