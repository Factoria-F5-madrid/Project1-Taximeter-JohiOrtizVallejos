# Project1-Taximeter-JohiOrtizVallejos
Primer proyecto del módulo 1 del Bootcamp de IA de la promoción 5 en Python
Este proyecto implementa un taxímetro en Python que calcula tarifas basadas en el tiempo detenido y el tiempo en movimiento.

## Estructura del proyecto

- `.gitignore`: Archivo que especifica qué archivos o carpetas deben ser ignorados por Git. Actualmente ignora el entorno virtual `.venv`.
- `taximetro.py`: Script principal que contiene la lógica del taxímetro.

## Funcionalidades

### `calculate_fare(seconds_stopped, seconds_moving)`
Esta función calcula la tarifa total en euros basada en el tiempo detenido y el tiempo en movimiento:
- **Tiempo detenido**: 0.02 €/segundo.
- **Tiempo en movimiento**: 0.05 €/segundo.
