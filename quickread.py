import tkinter as tk
from tkinter import messagebox
import mysql.connector
from transformers import BartForConditionalGeneration, BartTokenizer
import pandas as pd
from PIL import Image, ImageTk


def summ():
    # Load BART model and tokenizer
    model_name = 'facebook/bart-large-cnn'
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    def bart_summarizer(text):
        # Tokenize input text
        inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)

        # Generate summary
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=150, early_stopping=True)

        # Decode the generated summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    # Read input text from a file
    input_file_path = 'user_inputs.txt'  # Replace with your input file path
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # Generate summary using BART
    summary_output = bart_summarizer(input_text)

    # Display the generated summary
    """print("Generated Summary:")
    print(summary_output)"""
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    messagebox.showinfo("Generated Summary", summary_output)
    root.mainloop()

# Call the function to generate a summary



def storing():
    # Function to create a text file with provided text inputs
    def create_file(text_inputs):
        file_name = 'user_inputs.txt'
        with open(file_name, mode='w', encoding='utf-8') as file:
            for user_input in text_inputs:
                file.write(user_input + "\n")  # Write each input followed by a newline

        print(f"User inputs have been saved to '{file_name}'.")

    # Function to handle "Generate Output" button click event
    def generate_output():
        text = text_input.get("1.0", tk.END)
        if text.strip() == "":
            # Show an error message if no text is entered
            output.config(state=tk.NORMAL)
            output.delete("1.0", tk.END)
            output.insert(tk.END, "Error: Please enter some text.")
            output.config(state=tk.DISABLED)
        else:
            # Store input text in a text file
            create_file([text])  # Passing input text to create_file function for saving
             # Call summ function after storing inputs in the text file
            summ()

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Input to TXT")
      
    """bg_image = tk.PhotoImage(file="bckgrnd.png")
    label1 = tk.Label(root, image=bg_image)
    label1.place(x=-500, y=10, relheight=1)
    label1.image = bg_image"""

    # Define the widgets
    text_label = tk.Label(root, text="Enter Text:", font=("Times New Roman",100))
    text_label.pack()

    text_input = tk.Text(root, height=10, width=100)
    text_input.pack()

    generate_button = tk.Button(root, text="Generate Output", command=generate_output)
    generate_button.pack()

    """output_label = tk.Label(root, text="Output:")
    output_label.pack()

    output = tk.Text(root, height=10, width=40, state=tk.DISABLED)
    output.pack()"""

    root.mainloop()


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Missing_9',
            database='project'
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def execute_query(self, query, data=None):
        self.cursor.execute(query, data)
        return self.cursor

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.create_login_ui()

    def create_login_ui(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        login_label = tk.Label(self.login_frame, text="Login", font=("Times New Roman",100))
        login_label.pack( padx=30,pady=30)

        login_email_label = tk.Label(self.login_frame, text="Email")
        login_email_label.pack()
        self.login_email_entry = tk.Entry(self.login_frame,width=50)
        self.login_email_entry.pack()

        login_password_label = tk.Label(self.login_frame, text="Password")
        login_password_label.pack()
        self.login_password_entry = tk.Entry(self.login_frame, show="*",width=50)
        self.login_password_entry.pack()

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.pack()

    def login(self):
        login_email = self.login_email_entry.get()
        login_password = self.login_password_entry.get()

        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        user = self.db.execute_query(query, (login_email, login_password)).fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome!")
            # Do something after successful login
            storing()
            
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

class SignupApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.create_signup_ui()

    def create_signup_ui(self):
        self.signup_frame = tk.Frame(self.root)
        self.signup_frame.pack()

        signup_label = tk.Label(self.signup_frame, text="Signup", font=("Times New Roman",100))
        signup_label.pack(padx=15,pady=15)

        signup_email_label = tk.Label(self.signup_frame, text="Email")
        signup_email_label.pack()
        self.signup_email_entry = tk.Entry(self.signup_frame,width=50)
        self.signup_email_entry.pack()

        signup_password_label = tk.Label(self.signup_frame, text="Password")
        signup_password_label.pack()
        self.signup_password_entry = tk.Entry(self.signup_frame, show="*",width=50)
        self.signup_password_entry.pack()

        signup_button = tk.Button(self.signup_frame, text="Signup", command=self.signup)
        signup_button.pack()

    def signup(self):
        signup_email = self.signup_email_entry.get()
        signup_password = self.signup_password_entry.get()

        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        self.db.execute_query(query, (signup_email, signup_password))
        self.db.connection.commit()
        messagebox.showinfo("Signup Successful", "Signup successful. Please login.")

def main():
    root = tk.Tk()
    root.title("Login and Signup Page")
    root.geometry("500x500")
  
    bg_image = tk.PhotoImage(file="bckgrnd.png")
    label1 = tk.Label(root, image=bg_image)
    label1.place(x=-500, y=10, relheight=1)
    label1.image = bg_image
    
    login_app = LoginApp(root)
    signup_app = SignupApp(root)

    def show_login_frame():
        signup_app.signup_frame.pack_forget()
        login_app.login_frame.pack()
        
        

    def show_signup_frame():
        login_app.login_frame.pack_forget()
        signup_app.signup_frame.pack()

    login_tab_button = tk.Button(root, text="Login", command=show_login_frame)
    login_tab_button.pack(side="left")

    signup_tab_button = tk.Button(root, text="Signup", command=show_signup_frame)
    signup_tab_button.pack(side="left")

    show_login_frame()  # Show login frame by default

    root.mainloop()

if __name__ == "__main__":
    main()



    
   



