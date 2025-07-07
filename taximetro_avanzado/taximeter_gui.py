import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button, Text, Scrollbar, END
from taximeter_cli import Taximeter
import auth

class LoginWindow(simpledialog.Dialog):
    def body(self, master):
        Label(master, text="User:").grid(row=0)
        Label(master, text="Password:").grid(row=1)
        
        self.username_entry = Entry(master)
        self.password_entry = Entry(master, show="*")
        
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        return self.username_entry
    
    def apply(self):
        self.result = (
            self.username_entry.get(),
            self.password_entry.get()
        )
        
        
def authenticate_gui():
    while True:
        dialog = LoginWindow(None, title="Login Taximeter")
        if dialog.result is None:
            return False
        username, password = dialog.result
        users = auth.load_user()
        if username in users and users[username] == password:
            messagebox.showinfo("Login", f"Welcome! {username}")
            return True
        else:
            messagebox.showerror("Login", "Incorrect username or password.")


class PricesWindow(Toplevel):
    def __init__(self, master, taximeter):
        super().__init__(master)
        self.taximeter = taximeter
        self.title("Configure prices")
        Label(self, text="Stopped Price (€/s):").grid(row=0, column=0)
        Label(self, text="Moving Price (€/s):").grid(row=1, column=0)
        self.stopped_entry = Entry(self)
        self.moving_entry = Entry(self)
        self.stopped_entry.insert(0, str(self.taximeter.price_stopped))
        self.moving_entry.insert(0, str(self.taximeter.price_moving))
        self.stopped_entry.grid(row=0, column=1)
        self.moving_entry.grid(row=1, column=1)
        Button(self, text="Save", command=self.save_prices).grid(row=2, column=0, columnspan=2)
        
    def save_prices(self):
        try:
            stopped = float(self.stopped_entry.get())
            moving = float(self.moving_entry.get())
            self.taximeter.price_stopped = stopped
            self.taximeter.price_moving = moving
            messagebox.showinfo("Prices", "Prices updated correctly.")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values.")
            
class DevWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Dev Menu")
        Button(self, text="Create User", command=self.create_user).pack(pady=5)
        self.log_text = None
        
    def create_user(self):
        username = simpledialog.askstring("Create User", "New User:")
        if username:
            password = simpledialog.askstring("Create User", "Password:", show="*")
            if password:
                if auth.create_user(username, password):
                    messagebox.showinfo("Create User", f"Usuario '{username}' create")
                else:
                    messagebox.showerror("Create User", "The user already exists.")
                    
    def show_logs(self):
        if self.log_text:
            self.log_text.destroy()
        self.log_text = Text(self, width=60, height=20)
        self.log_text.pack()
        try:
            with open("taximeter.log", "r", encoding="utf-8") as f:
                self.log_text.insert(END, f.read())
        except FileNotFoundError:
            self.log_text.insert(END, "There are no logs.")    

class TaximeterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("F5 Taximeter")
        self.taximeter = Taximeter()

        if not authenticate_gui():
            root.destroy()
            return

        self.status_label = tk.Label(root, text="Welcome to the F5 Taximeter!")
        self.status_label.pack(pady=10)

        buttons = [
            ("Start", self.start_trip),
            ("Stop", self.stop_trip),
            ("Move", self.move_trip),
            ("Finish", self.finish_trip),
            ("Set Prices", self.set_prices),
            ("Dev", self.dev_menu),
            ("Exit", self.exit_app)
        ]

        for (text, command) in buttons:
            btn = tk.Button(root, text=text, width=15, command=command)
            btn.pack(pady=5)

        self.log_box = Text(root, width=60, height=10, state="disabled")
        self.log_box.pack(pady=10)

    def update_status(self, msg):
        self.status_label.config(text=msg.splitlines()[0])  # primer línea arriba
        self.log_box.config(state="normal")
        self.log_box.insert(END, msg + "\n")
        self.log_box.config(state="disabled")
        self.log_box.see(END)

    def start_trip(self):
        msg = self.taximeter.start_trip()
        self.update_status(msg)

    def stop_trip(self):
        msg = self.taximeter.stop()
        self.update_status(msg)

    def move_trip(self):
        msg = self.taximeter.move()
        self.update_status(msg)

    def finish_trip(self):
        msg = self.taximeter.finish_trip()
        self.update_status(msg)

    def set_prices(self):
        window = Toplevel(self.root)
        window.title("Set Prices")
        window.geometry("300x200")

        Label(window, text="Select mode:").pack(pady=5)

        def apply_mode(mode):
            msg = self.taximeter.set_prices(mode)
            self.update_status(msg)
            window.destroy()

        def set_manual_prices():
            try:
                s = simpledialog.askstring("Manual", "Stopped €/s:")
                m = simpledialog.askstring("Manual", "Moving €/s:")
                if s:
                    self.taximeter.price_stopped = float(s)
                if m:
                    self.taximeter.price_moving = float(m)
                self.taximeter.current_fare = "manual"
                self.update_status("Manual prices applied.")
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter valid numeric values.")

        Button(window, text="Day rate", width=20, command=lambda: apply_mode("day")).pack(pady=5)
        Button(window, text="Night rate", width=20, command=lambda: apply_mode("night")).pack(pady=5)
        Button(window, text="Manual", width=20, command=set_manual_prices).pack(pady=5)

    def dev_menu(self):
        window = Toplevel(self.root)
        window.title("Dev Tools")
        window.geometry("400x400")
        Label(window, text="Developer Tools", font=("Helvetica", 14, "bold")).pack(pady=10)

        def create_user():
            username = simpledialog.askstring("Create User", "Enter username:")
            if username:
                password = simpledialog.askstring("Create User", "Enter password:", show="*")
                if password:
                    if auth.create_user(username, password):
                        messagebox.showinfo("User Created", f"User '{username}' created.")
                    else:
                        messagebox.showerror("Error", f"User '{username}' already exists.")

        def show_logs():
            try:
                with open("taximeter.log", "r", encoding="utf-8") as f:
                    logs = f.read()
            except FileNotFoundError:
                logs = "No logs found."

            log_window = Toplevel(window)
            log_window.title("Taximeter Logs")
            text_box = Text(log_window, wrap="word", width=60, height=20)
            text_box.pack(padx=10, pady=10, fill="both", expand=True)

            scroll = Scrollbar(text_box)
            scroll.pack(side="right", fill="y")
            text_box.config(yscrollcommand=scroll.set)
            scroll.config(command=text_box.yview)

            text_box.insert("1.0", logs)
            text_box.config(state="disabled")

        Button(window, text="Create New User", command=create_user).pack(pady=5)
        Button(window, text="View Log File", command=show_logs).pack(pady=5)

    def exit_app(self):
        self.root.destroy()
        