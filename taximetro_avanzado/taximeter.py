import time
import csv
import logging
import auth

class Taximeter:
    def __init__(self):
        from config import DEFAULT_PRICE_STOPPED, DEFAULT_PRICE_MOVING
        self.price_stopped = DEFAULT_PRICE_STOPPED
        self.price_moving = DEFAULT_PRICE_MOVING
        self.current_fare = "day"
        self.reset_trip()
        
    def reset_trip(self):
        self.trip_active = False
        self.start_time = 0
        self.stopped_time = 0
        self.moving_time = 0
        self.state = None
        self.state_start_time = 0
        
    def show_logs(self):
        print("\n--- 📋 Log History (taximeter.log) 📋 ---")
        try:
            with open("taximeter.log", "r", encoding="utf-8") as logfile:
                logs = logfile.read()
                print(logs if logs else "❌ Log file is empty.")
        except FileNotFoundError:
            print("❌ Log file not found.")
        print("----------------------------------\n")
    
    def create_user_promp(self):
        print("\n--- 👤 Create New User ---")
        username = input("Enter new username: ").strip()
        password = input("Enter new password: ").strip()
        if not username or not password:
            print("❌ Username and password cannot be empty.")
            return
        if auth.create_user(username, password):
            print(f"✅ User '{username}' created successfully.")
        else:
            print(f"❌ User '{username}' already exists.")
        print("--------------------------\n")
        
    def dev_menu(self):
        while True:
             print("\n--- 🛠️ Dev Menu ---")
             print("1. 👤 Create user\n")
             print("2. 📋 Show log\n")
             print("3. 🔙 Back\n")
             choice = input("Choose an option (1-3: )").strip()
             if choice == "1":
                 self.create_user_promp()
             elif choice == "2":
                 self.show_logs()
             elif choice == "3":
                 break
             else:
                 print("❌ Invalid option. Please choose 1, 2, or 3.")
    
    def calculate_fare(self):
        return self.stopped_time * self.price_stopped + self.moving_time * self.price_moving
    
    def update_state_time(self):
        duration = time.perf_counter() - self.state_start_time
        if self.state == 'stopped':
            self.stopped_time += duration
        elif self.state == 'moving':
            self.moving_time += duration
            
    def print_welcome_message(self):
        message = "🚕 Welcome to the F5 taximeter!🚕   "
        box_width = len(message) + 6  # 2 espacios de margen a cada lado + 2 astericos

        print("\n" + "*" * box_width)
        print("*" + " " * (box_width - 2) + "*")
        print(f"* {message.center(box_width - 8)} *")
        print("*" + " " * (box_width - 2) + "*")
        print("*" * box_width + "\n")
        print("🚖 start\n")
        print("🛑 stop\n")
        print("🟢 move\n")
        print("📍 finish\n")
        print("💸 setprices\n")
        print("📋 dev\n")
        print("❌ exit\n")

    def print_fare_summary(self):
        self._print_summary_header("Partial summary")
    
    def print_total_summary(self, total_duration):
        self._print_summary_header("Trip Summary", total_duration)
    
    def _print_summary_header(self, title, total_duration=None):
        fare = self.calculate_fare()
        print(f"\n--- {title} ---")
        if total_duration is not None:
            print(f"🕓 Total Trip Duration: {total_duration:.2f}s")
        print(f"🚨 Stopped time: {self.stopped_time:.1f}s")
        print(f"🚕 Moving time: {self.moving_time:.1f}s")
        print(f"💶 Total fare: €{fare:.2f}")
        print("----------------------\n")
        logging.info(f"{title} - Stopped: {self.stopped_time:.1f}s, Moving: {self.moving_time:.1f}s, Fare: €{fare:.2f}")
        
    def _print_summary_moving(self, duration, temp_moving_time, fare):
        print("🚕 Already moving.")
        print(f"🕓 Time elapsed in current state: {duration:.1f}s")
        print(f"🕓 Total moving time so far: {temp_moving_time:.1f}s")
        print(f"💶 Current fare is: €{fare:.2f}")
    
    def _print_summary_stopped(self, duration, temp_stopped_time, fare):
        print("🚨 Already stoppped.")
        print(f"🕓 Time elapsed in current state: {duration:.1f}s")
        print(f"🚕 Total moving time so far: {temp_stopped_time:.1f}s")
        print(f"💶 Current fare is: €{fare:.2f}")
        
    def start_trip(self):
        self.reset_trip()
        self.trip_active = True
        self.state = 'stopped'
        self.start_time = time.perf_counter()
        self.state_start_time = time.perf_counter()
        print("🚕 Trip started. Initial state: 'stopped'.")
        logging.info("Trip started")
        
    def stop(self):
        duration = time.perf_counter() - self.state_start_time
        temp_stopped_time = self.stopped_time + duration
        fare = temp_stopped_time * self.price_stopped + self.moving_time * self.price_moving
        
        if self.state == 'stopped':
            self._print_summary_stopped(duration, temp_stopped_time, fare)
        else:
            self.update_state_time()
            self.state = 'stopped'
            self.state_start_time = time.perf_counter()
            print("🛑 State changed to 'stopped'.")
            self.print_fare_summary()                
        
    def move(self):
        duration = time.perf_counter() - self.state_start_time
        temp_moving_time = self.moving_time + duration
        fare = self.stopped_time * self.price_stopped + temp_moving_time * self.price_moving
        
        if self.state == 'moving':
            self._print_summary_moving(duration, temp_moving_time, fare)
        else:
            self.update_state_time()
            self.state = 'moving'
            self.state_start_time = time.perf_counter()
            print("🛑 State changed to 'moving'.")
            self.print_fare_summary()                
        
    def finish_trip(self):
        self.update_state_time()
        total_duration = time.perf_counter() - self.start_time
        total_fare = self.calculate_fare()
        
        self.print_total_summary(total_duration)
        
        with open("trip_history.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(["date", "total_duration", "time_stopped", "time_moving",
                                 "total_rate", "stop_price", "moving_price", "fare"])
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                f"{total_duration:.2f}",
                f"{self.stopped_time:.1f}",
                f"{self.moving_time:.1f}",
                f"{total_fare:.2f}",
                f"{self.price_stopped:.2f}",
                f"{self.price_moving:.2f}",
                self.current_fare
            ])
            
        logging.info(f"Completed route - Duration: {total_duration:.2f}s, Stopped: {self.stopped_time:.1f}s, Moving: {self.moving_time:.1f}s, Fare: €{total_fare:.2f}")
        self.reset_trip()
        
    def set_prices(self):
        print("💶  Set current prices:")
        print(" - 🌚  Enter 'night' for night rate")
        print(" - 🌞  Enter 'day' to return to day rate")
        print(" - 🫳  Or press enter to write the prices manually\n")
        
        user_input = input("Mode (🌚 'night', 🌞 'day') or 🫳 manual pricing?").strip().lower()
        
        if user_input == "night":
            self.price_stopped = 0.02 * 2
            self.price_moving = 0.05 * 2
            self.current_fare = "night"
            print(f"🌚 Night rate activated: stopped €{self.price_stopped:.2f}/s, moving €{self.price_moving:.2f}/s")
        elif user_input == "day":
            self.price_stopped = 0.02
            self.price_moving = 0.05
            self.current_fare = "day"
            print(f"🌞 Day rate activated: stopped €{self.price_stopped:.2f}/s, moving €{self.price_moving:.2f}/S")
        else:
            try:
                new_stopped = input(f"New price per second stopped (current: {self.price_stopped:.2f}): ").strip()
                new_moving = input(f"New price per second moving (current: {self.price_moving:.2f}): ").strip()
                if new_stopped:
                    self.price_stopped = float(new_stopped)
                if new_moving:
                    self.price_moving = float(new_moving)
                print(f"💶 Prices updated: stopped €{self.price_stopped:.2f}/s, moving €{self.price_moving:.2f}/s")
            except ValueError:
                print("❌ Error, please enter a valid value.")
                
    def run(self):
        self.print_welcome_message()

        def _start():
            if self.trip_active:
                print("❌ Error: A trip is already in progress.")
                return
            self.start_trip()

        def _stop():
            if not self.trip_active:
                print("❌ Error: No active trip.")
                return
            self.stop()

        def _move():
            if not self.trip_active:
                print("❌ Error: No active trip")
                return
            self.move()

        def _finish():
            if not self.trip_active:
                print("❌ Error: No active trip to finish.")
                return
            self.finish_trip()
            self.print_welcome_message()

        def _setprices():
            self.set_prices()
            self.print_welcome_message()

        def _dev():
            self.dev_menu()
            self.print_welcome_message()

        def _exit():
            print("👋 Exiting the program. Goodbye!")
            raise SystemExit

        commands = {
            "start": _start,
            "stop": _stop,
            "move": _move,
            "finish": _finish,
            "setprices": _setprices,
            "dev": _dev,
            "exit": _exit
        }

        while True:
            command = input("> ").strip().lower()
            if command in commands:
                try:
                    commands[command]()
                except SystemExit:
                    break
            else:
                print("❌ Unknown command. Use: 🚖 start, 🛑 stop, 🟢 move, 📍 finish, 💸 setprices, or ❌ exit")
