from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import smtplib
import json

everything_is_ok = False

# USE LAST EMAILS FOR ENTRIES #

# SENDER EMAIL #
def use_last_sender_email():
    try:
        with open('email.json', "r") as data_value:
            data = json.load(data_value)
        sender_email = data['sender_email']
        sender_user_ask = messagebox.askokcancel(title='Use the last email', message=f"Your last email is {sender_email} are you sure you wanna continue?")
        if sender_user_ask:
            sender_email_input.delete(0, END)
            sender_email_input.insert(0, sender_email)
    except FileNotFoundError:
        messagebox.showinfo(title='Oops', message="You dont have any email")


# RECEIVER EMAIL #
def use_last_receiver_email():
    try:
        with open('email.json', "r") as data_value:
            data = json.load(data_value)
        receiver_email = data['receiver_email']
        receiver_user_ask = messagebox.askokcancel(title='Use the last email', message=f"Your last email is {receiver_email} are you sure you wanna continue?")
        if receiver_user_ask:
            receiver_email_input.delete(0, END)
            receiver_email_input.insert(0, receiver_email)
    except FileNotFoundError:
        messagebox.showinfo(title='Oops', message="You dont have any email")

# SEND EMAIL #

def send_email():
    sender = sender_email_input.get()
    receiver = receiver_email_input.get()
    subject = subject_input.get("1.0", "end-1c")
    message = message_entry.get("1.0", "end-1c")
    print(sender, receiver, subject, message)

    # CHECK IF FIELDS IS EMPTY CREATE AN ALERT #
    if len(sender) == 0 or len(receiver) == 0 or len(subject) == 0 or len(message) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty")
        
    # CHECK TO SEE EVERYTHING IS OK OR NOT #
    else:
        is_ok = messagebox.askokcancel(title="Send Email", message=f"Are you sure you want to send message from {sender}"
                                                                   f" to {receiver}")

        if is_ok:
            email_password = simpledialog.askstring(title='Enter Your Email Password', prompt="Please enter you THIRD P"
                                    "ARTY password (you can create a password in app password on your manage email)")

            if len(email_password) == 0:
                messagebox.showinfo(title="Oops", message="Please Enter a Valid Password")
            # SENDING EMAIL WITH SMTPLIB #
            else:
                global everything_is_ok
                try:

                    # SENDING EMAIL #
                     with smtplib.SMTP('smtp.gmail.com', 587) as connection:
                        connection.starttls()
                        connection.login(sender, email_password)
                        connection.sendmail(from_addr=sender, to_addrs=receiver, msg=f"Subject:{subject}\n\n {message}\n")
                        messagebox.showinfo(title="Message Sent", message="Your Message Was Successfully Sent")
                        
                        # CLEAR ENTRIES AFTER SENDING EMAIL #
                        sender_email_input.delete(0, END)
                        receiver_email_input.delete(0, END)
                        subject_input.delete("1.0", "end-1c")
                        message_entry.delete("1.0", "end-1c")
                     everything_is_ok = True
                    
                # CHECK IF WE GET ERROR WHILE SENDING EMAIL #
                except smtplib.SMTPAuthenticationError:
                    print(smtplib.SMTPAuthenticationError)
                    messagebox.showinfo(title="Oops", message="Please Enter a Valid Email/Password")
                    
                # SAVING DATAS #
                if everything_is_ok:
                    # CREATE EMAIL DICT #
                    emails_dict = {
                        'sender_email': sender,
                        'receiver_email': receiver
                    }
                    
                    # SAVING EMAILS IN JSON FILE #
                    try:
                        with open('email.json', 'r') as data_value:
                            data = json.load(data_value)
                    except FileNotFoundError:
                        with open('email.json', 'w') as data_value:
                            json.dump(emails_dict, data_value)
                    else:
                        data.update(emails_dict)
                        with open('email.json', 'w') as data_value:
                            json.dump(emails_dict, data_value)


# UI CONFIGURATION #
window = Tk()
window.title("Email Sender")
window.config(padx=50, pady=50)

window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=2)


# MAIL LOGO
mail_logo = Canvas(width=200, height=200)
mail_image = PhotoImage(file="assest/email.png")
mail_logo.create_image(100, 100, image=mail_image)
mail_logo.grid(column=1, row=0)

# EMAIL INPUT & LABEL
sender_email_label = Label(text="Enter Your Email:", font=("Helvetica", "10", 'bold'))
sender_email_label.grid(column=0, row=1)
sender_email_input = Entry(width=30, highlightcolor='#E53935', highlightthickness=2)
sender_email_input.grid(column=1, row=1, columnspan=1)
use_last_sender_email = Button(text="Use Last Sender Email", command=use_last_sender_email)
use_last_sender_email.grid(column=2, row=1)

# RECEIVER EMAIL INPUT & LABEL
receiver_email_label = Label(text='Enter Receiver Email:', font=("Helvetica", "10", 'bold'))
receiver_email_label.grid(column=0, row=2)
receiver_email_input = Entry(width=30, highlightcolor='#E53935', highlightthickness=2)
receiver_email_input.grid(column=1, row=2, columnspan=1)
use_last_receiver_email = Button(text="Use Last Receiver Email", command=use_last_receiver_email)
use_last_receiver_email.grid(column=2, row=2, pady=10)

# SUBJECT INPUT & LABEL
subject_label = Label(text="Subject:", font=("Helvetica", "10", 'bold'))
subject_label.grid(column=0, row=3)
subject_input = Text(width=40, height=1.5, highlightcolor='#E53935', highlightthickness=2)
subject_input.grid(column=1, row=3, pady=20)

# MESSAGE INPUT & LABEL
message_label = Label(text="Message", font=("Helvetica", "16", 'bold'))
message_label.grid(column=1, row=4)
message_entry = Text(window, width=40, height=10, highlightcolor='#E53935', highlightthickness=2)
message_entry.grid(column=1, row=5)

# SEND EMAIL BUTTON
send_btn = Button(text="Send Email", width=30, command=send_email)
send_btn.grid(column=1, row=6, pady=8)

window.mainloop()