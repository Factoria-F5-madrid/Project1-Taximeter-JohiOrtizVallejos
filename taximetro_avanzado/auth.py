import getpass
import json
import os
import sys
import termios
import tty

AUTH_FILE = "auth.json"

def load_user():
    if not os.path.exists(AUTH_FILE):
        return {}
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_users(users):
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
        
def create_user(username, password):
    users = load_user()
    if username in users:
        return False    # Usuario ya existe
    users[username] = password
    save_users(users)
    return True
    
def get_hidden_password(prompt="Password: "):
    print(prompt, end='', flush=True)
    pwd = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ['\n', '\r']:
                print() # newline
                break
            elif ch == '\x7f':  # Backspace
                if len(pwd) > 0:
                   pwd = pwd[:-1]
                   sys.stdout.write('\b \b')
                   sys.stdout.flush()
            else:
                pwd += ch
                sys.stdout.write('*')
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return pwd

def initial_user_creation():
    print("🔑 There are no registered users. Let's create the first user.")
    while True:
        username = input("👤 New user: ").strip()
        if not username:
            print("❌ The user cannot be empty.")
            continue
        password = get_hidden_password("🔑 New password: ")
        if not password:
            print("❌ The password cannot be empty.")
            continue
        confirm = get_hidden_password("🔑 Confirm password: ")
        if password != confirm:
            print("❌ Passwords do not match.")
            continue
        if create_user(username, password):
            print(f"✅ User '{username}' successfully created.\n")
            return
        else:
             print("❌ The user already exist. Try another name.")

def authenticate_user(max_attempts=3):
    users = load_user()
    if not users:
        initial_user_creation()
        users = load_user()
    print("🔒 Authentication required")
    for attempt in range(1, max_attempts + 1):
        username = input("👤 Usuario: ").strip()
        password = get_hidden_password("🔑Enter the password: ")
        if username in users and users[username] == password:
            print(f"✅ Welcome! {username}.\n")
            return True
        else:
            print(f"❌ Incorrect username or password, try again. Try {attempt}{max_attempts}")
    print("🚫 Access denied. Closing the program.")
    sys.exit(1)