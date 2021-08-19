from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import pyperclip

DATA_FILE = "data.json"
EMAIL_KEY_NAME = "Email/Username"
PASSWORD_KEY_NAME = "Password"

BLUE = "#264653"
GREEN = "#2a9d8f"
YELLOW = "#e9c46a"
ORANGE = "#f4a261"
RED = "#e76f51"
FONT = ("Courier", 12, "bold")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for i in range(randint(8, 10))]
    password_list += [choice(symbols) for i in range(randint(2, 4))]
    password_list += [choice(numbers) for i in range(randint(2, 4))]
    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SEARCH DATA ------------------------------- #
def find_password():
    website_string = website_entry.get()

    try:
        with open(DATA_FILE, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message=f"{DATA_FILE} not found.\n\n"
                                                    f"Just ADD some data Xtreme! 😉")
    else:
        if website_string not in data:
            messagebox.showinfo(title="Search Result", message=f"No details for {website_string} exist.")
        else:
            email_string = data[website_string][EMAIL_KEY_NAME]
            password_string = data[website_string][PASSWORD_KEY_NAME]
            messagebox.showinfo(title="Search Result Xtreme!", message=f"Website: {website_string}\n"
                                                                       f"Email/Username: {email_string}\n"
                                                                       f"Password: {password_string}\n\n"
                                                                       f"Password copied to clipboard Xtreme! 😉")
            pyperclip.copy(password_string)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_string = website_entry.get()
    email_string = email_entry.get()
    password_string = password_entry.get()

    if len(website_string) == 0 or len(email_string) == 0 or len(password_string) == 0:
        messagebox.showinfo(title="Empty Field(s)", message="Please answer all fields!")
    else:
        data_dict = {
            website_string: {
                EMAIL_KEY_NAME: email_string,
                PASSWORD_KEY_NAME: password_string
            }
        }

        is_ok = messagebox.askokcancel(title="Confirm Data",
                                       message=f"Website: {website_string}\n"
                                               f"Email/Username: {email_string}\n"
                                               f"Password: {password_string}\n\n"
                                               f"Is it OK to save?")
        if is_ok:
            try:
                with open(DATA_FILE, "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(DATA_FILE, "w") as data_file:
                    # Saving updated data
                    json.dump(data_dict, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(data_dict)

                with open(DATA_FILE, "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Leo's PassLock Xtreme!")
window.config(padx=25, pady=25, bg=BLUE)

# Canvas
canvas = Canvas(width=200, height=200, bg=BLUE, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3)

# Labels
website_label = Label(text="Website:", bg=BLUE, fg=YELLOW)
website_label.grid(row=1, column=0, padx=5, sticky="E")

email_label = Label(text="Email/Username:", bg=BLUE, fg=YELLOW)
email_label.grid(row=2, column=0, padx=5, sticky="E")

password_label = Label(text="Password:", bg=BLUE, fg=YELLOW)
password_label.grid(row=3, column=0, padx=5, sticky="E")

# Entries
website_entry = Entry(bg=YELLOW)
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()

email_entry = Entry(bg=YELLOW)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

password_entry = Entry(bg=YELLOW)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
generate_pw_button = Button(text="Generate Password", font=FONT, bg=GREEN, fg=BLUE, highlightthickness=0,
                            command=generate_password)
generate_pw_button.grid(row=3, column=2, sticky="EW", pady=5, padx=(5, 0))

search_button = Button(text="Search", font=FONT, bg=GREEN, fg=BLUE, highlightthickness=0,
                       command=find_password)
search_button.grid(row=1, column=2, sticky="EW", pady=5, padx=(5, 0))

add_button = Button(text="Add!", font=FONT, bg=RED, fg=BLUE, highlightthickness=0, command=save)
add_button.grid(row=4, column=1, sticky="EW", columnspan=2, pady=5)

# Window Loop
window.mainloop()
