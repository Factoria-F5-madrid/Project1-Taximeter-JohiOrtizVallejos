import csv
import time
import logging

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("taximeter.log"),
        logging.StreamHandler()
    ]
)

def calculate_fare(seconds_stopped, seconds_moving, price_stopped=0.02, price_moving=0.05):
    """
    Calcular la tarifa total en euros.
    - Stopped: 0.02 €/s
    - Moving: 0.05 €/s
    """
    fare = seconds_stopped * price_stopped + seconds_moving * price_moving
    logging.debug(f"Tarifa calculada: €{fare:.2f}")
    return fare

def update_state_time(state, state_start_time, stopped_time, moving_time):
    """
    Actualiza el tiempo total en estado detenido o en movimiento
    según el estado actual.
    """
    duration = time.perf_counter() - state_start_time
    if state == 'stopped':
        stopped_time += duration
    elif state == 'moving':
        moving_time += duration
    return stopped_time, moving_time

def print_fare_summary(stopped_time, moving_time, price_stopped, price_moving):
    """
    Imprime el resumen de tarifa y tiempos parciales
    """
    fare = calculate_fare(stopped_time, moving_time, price_stopped, price_moving)
    print(f"Stopped time: {stopped_time:.1f}s")
    print(f"Moving time: {moving_time:.1f}s")
    print(f"Current fare: €{fare:.2f}")
    logging.info(f"Resumen parcial - Stopped: {stopped_time:.1f}s, Moving: {moving_time:.1f}s, Fare: €{fare:.2f}")

def taximeter():
    """
    Función para manejar y mosttrar las opciones del taximetro.
    """
    print("Welcome to the F5 Taximeter!")
    print("Available commands: 'start', 'stop', 'move', 'finish', 'setprices', 'exit'\n")
    logging.info("Programa iniciado")
    
    try:
        price_stopped = float(input("Set price per second while stopped (default: 0.02): ") or 0.02)
        price_moving = float(input("Set price per second while moving (default: 0.05): ") or 0.05)
    except ValueError:
        print("Invalid input. Using default prices.")
        price_stopped = 0.02
        price_moving = 0.05
        
    current_fare = "dia"   # variable para registar la tarifa actual
        
    logging.info(f"Precios configurados - Parado: €{price_stopped}/s, Moviendo: €{price_moving}/s")

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
                logging.warning("Intento de iniciar un trayecto ya activo")
                continue
            trip_active = True
            start_time = time.perf_counter()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'    # Iniciamos en estado 'stopped'
            state_start_time = time.perf_counter()
            print("Trip started. Initial state: 'stopped'.")
            logging.info("Trayacto iniciado")
        
        elif command == "stop":
            if not trip_active:
                print("Error: No active trip.")
                logging.warning("Comando 'stop' sin trayecto activo")
                continue
            
            if state == 'stopped':
                current_duration = time.perf_counter() - state_start_time
                temp_stopped_time = stopped_time + current_duration
                fare = calculate_fare(temp_stopped_time, moving_time, price_stopped, price_moving)
                print("Already stopped.")
                print(f"Time elapsed in current state: {current_duration:.1f}s")
                print(f"Current fare is: €{fare:.2f}")
                logging.info(f"Ya detenido - +{current_duration:-1f}s, Tarifa actual €{fare:.2f}")
                continue

            # Cambiar de 'moving' a 'stopped'
            stopped_time, moving_time = update_state_time(state, state_start_time, stopped_time, moving_time)
            state = 'stopped'
            state_start_time = time.perf_counter()         
            print("State changed to 'stopped`'.")
            logging.info(f"Cambio a 'stopped'. Total moving: {moving_time:.1f}s")
            print_fare_summary(stopped_time, moving_time, price_stopped, price_moving)

        elif command == 'move':
            if not trip_active:
                print("Error: No active trip.")
                logging.warning("Comando 'move' sin trayecto activo")
                continue
            
            # Calcula la tarifa si ya estás en movimiento
            if state == 'moving':
                current_duration = time.perf_counter() - state_start_time
                temp_moving_time = moving_time + current_duration
                fare = calculate_fare(stopped_time, temp_moving_time, price_stopped, price_moving)
                print("Already moving.")
                print(f"Time elapsed in current state: {current_duration:.1f}s")
                print(f"Total moving time so far: {temp_moving_time:.1f}s")            
                print(f"Current fare is: €{fare:.2f}")
                logging.info(f"Ya en movimiento - +{current_duration:.1f}s, tarifa actual €{fare:.2f}")
                continue
            
            # Lógica para cambiar de 'stopped' a 'moving'
            stopped_time, moving_time = update_state_time(state, state_start_time, stopped_time, moving_time)
            state = 'moving'
            state_start_time = time.perf_counter()
            print("State changed to 'moving'.")
            logging.info(f"Cambio a 'moving'. Total stopped: {stopped_time:.1f}s")
            print_fare_summary(stopped_time, moving_time, price_stopped, price_moving)

        elif command == "finish":
            if not trip_active:
                print("Error: No active trip to finish.")
                logging.warning("Comando 'finish' sin trayecto activo")
                continue
            
           # Añadir tiempo del último estado antes de finalizar
            stopped_time, moving_time = update_state_time(state, state_start_time, stopped_time, moving_time)
            total_duration = time.perf_counter() - start_time
            total_fare = calculate_fare(stopped_time, moving_time, price_stopped, price_moving)

            # Calcula la tarifa total y muestra el resumen del viaje
            print(f"\n--- Trip Summary ---")
            print(f"Total Trip Duration: {total_duration:.2f}seconds")
            print(f"Stopped time: {stopped_time:.1f} seconds")
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}")
            print("----------------------\n")
            
            logging.info(f"Trayecto finalizado - Duración: {total_duration:.2f}s, Stopped: {stopped_time:.1f}s, Moving: {moving_time:.1f}s, Tarifa: €{total_fare:.2f}")

            # Guardar historial en CSV incluyendo precios.
            with open("trip_history.csv", "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if csvfile.tell() == 0:
                    writer.writerow(["fecha", "duracion_total", "tiempo_parado", "tiempo_moviendo",
                                     "tarifa_total", "precio_parado", "precio_moviendo", "tarifa"])
                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{total_duration:.2f}",
                    f"{stopped_time:.1f}",
                    f"{moving_time:.1f}",
                    f"{total_fare:.2f}",
                    f"{price_stopped:.2f}",
                    f"{price_moving:.2f}",
                    current_fare
                ])
            
            # Reset las variables para el próximo viaje
            trip_active = False
            state = None

        elif command == 'setprices':
            print("Configurar precios actuales:")
            print(" - Introduce 'noche' para tarifa nocturna")
            print(" - Introduce 'dia' para volver a tarifa diurna")
            print(" - O escribe los precios manualmente\n")
            
            user_input = input("¿Modo ('noche', 'dia') o precio manual? ").strip().lower()
            
            if user_input == "noche":
                price_stopped *= 2
                price_moving *= 2
                current_fare = "noche"
                print(f"Tarifa nocturna activada: parado €{price_stopped:.2f}/s, movienddo €{price_moving:.2f}/s")
                logging.info("Tarifa nocturna activada")
            elif user_input == 'dia':
                price_stopped = 0.02
                price_moving = 0.05
                current_fare = "dia"
                print(f"Tarifa diurna activada: parado €{price_stopped:.2f}/s, moviendo €{price_moving:.2f}/s")
                logging.info("Tarifa diurna activada")
            else:
                try:
                    new_stopped = input(f"New price second while stopped (current: {price_stopped:.2f}): ")
                    new_moving = input(f"New price per second while moving (current: {price_moving:.2f}): ")
                    
                    if new_stopped:
                        price_stopped = float(new_stopped)
                    if new_moving:
                        price_moving = float(new_moving)                        
                    print(f"Precios actualizados: stopped €{price_stopped:.2f}/s, moving €{price_moving:.2f}/s")
                    logging.info(f"Precios actualizados - Parado: €{price_stopped}/s, Moviendo: €{price_moving}")
                except ValueError:
                    print("Error, introduzca un valor válido.")
                    logging.warning("Intento fallido al actualizar precios")

        elif command == 'exit':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Unknown command. Use: start, stop, move, finish, or exit")
            logging.error(f"Comando desconocido: {command}")

if __name__ == "__main__":
    taximeter()