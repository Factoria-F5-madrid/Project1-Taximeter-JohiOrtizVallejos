import time

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Calcular la tarifa total en euros.
    - Stopped: 0.02 €/s
    - Moving: 0.05 €/s
    """
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    return fare

def update_state_time(state, state_start_time, stopped_time, moving_time):
    """
    Actualiza el tiempo total en estado detenido o en movimiento
    según el estado actual.
    """
    duration = time.perf_counter() - state_start_time
    if state == 'stoped':
        stopped_time += duration
    elif state == 'moving':
        moving_time += duration
    return stopped_time, moving_time

def print_fare_summary(stopped_time, moving_time):
    """
    Imprime el resumen de tarifa y tiempos parciales
    """
    fare = calculate_fare(stopped_time, moving_time)
    print(f"Stopped time: {stopped_time:.1f}s")
    print(f"Moving time: {moving_time:.1f}s")
    print(f"Current fare: €{fare:.2f}")

def taximeter():
    """
    Función para manejar y mosttrar las opciones del taximetro.
    """
    print("Welcome to the F5 Taximeter!")
    print("Available commands: 'start', 'stop', 'move', 'finish', 'exit'\n")

    trip_active = None
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None    # 'stopped'' o 'moving'
    state_start_time = 0

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if trip_active:
                print("Error: A trip is already in progress.")
                continue
            trip_active = True
            start_time = time.perf_counter()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'    # Iniciamos en estado 'stopped'
            state_start_time = time.perf_counter()
            print("Trip started. Initial state: 'stopped'.")
        
        elif command == "stop":
            if not trip_active:
                print("Error: No active trip.")
                continue
            
            if state == 'stopped':
                print("Already stopped.")
                current_duration = time.perf_counter() - state_start_time
                temp_stopped_time = stopped_time + current_fare
                fare = calculate_fare(temp_stopped_time, moving_time)
                print("Already stopped.")
                print(f"Time elapsed in current state: {current_duration:.1f}s")
                print(f"Current fare is: €{fare:.2f}")
                continue

            # Cambiar de 'moving' a 'stopped'
            moving_time = time.perf_counter() - state_start_time
            state = 'stopped'
            state_start_time = time.perf_counter()            
            print("State changed to 'stopped`'.")
            print_fare_summary(stopped_time, moving_time)

            current_fare = calculate_fare(stopped_time, moving_time)
            print(f"State change to 'stoppped'.")
            print(f"Total moving time so far: {moving_time:.1f}s")
            print(f"Current fare: €{current_fare:.2f}")

        elif command == 'move':
            if not trip_active:
                print("Error: Mo active trip.")
                continue
            
            # Calcula la tarifa si ya estás en movimiento
            if state == 'moving':
                current_duration = time.perf_counter() - state_start_time
                temp_moving_time = moving_time + current_duration
                fare = calculate_fare(stopped_time, temp_moving_time)
                print("Already moving.")
                print(f"Time elapsed in current state: {current_duration:.1f}s")
                print(f"Total moving time so far: {temp_moving_time:.1f}s")            
                print(f"Current fare is: €{fare:.2f}")
                continue
            
            # Lógica para cambiar de 'stopped' a 'moving'
            stopped_time += time.perf_counter() - state_start_time
            state = 'moving'
            state_start_time = time.perf_counter()
            print("State changed to 'moving'.")
            print_fare_summary(stopped_time, moving_time)

        elif command == "finish":
            if not trip_active:
                print("Error: No active trip to finish.")
                continue
            
            # Actualiza el último estado antes de terminar
            if state:
                if state == 'stopped':
                    stopped_time += time.perf_counter() - state_start_time
                else:
                    moving_time += time.perf_counter() - state_start_time

            total_duration = time.perf_counter() - start_time
            total_fare = calculate_fare(stopped_time, moving_time)

            # Calcula la tarifa total y muestra el resumen del viaje
            print(f"\n--- Trip Summary ---")
            print(f"Total Trip Duration: {total_duration:.2f}seconds")
            print(f"Stopped time: {stopped_time:.1f} seconds")
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}")
            print("----------------------\n")

            # Reset las variables para el próximo viaje
            trip_active = False
            state = None

        elif command == 'exit':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Unknown command. Use: start, stop, move, finish, or exit")

if __name__ == "__main__":
    taximeter()