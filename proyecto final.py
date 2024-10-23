from tkinter import *
from PIL import Image, ImageTk
import imutils
import cv2
import numpy as np
import math
import tkinter as tk
import cv2
import numpy as np

# Función para detectar el estado de madurez del aguacate
def detect_ripe_state(frame):
    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir los rangos de colores para los 4 estados de madurez
    # Estado 1: Verde (No Maduro)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    # Estado 2: Verde oscuro (Maduro Temprano)
    lower_dark_green = np.array([25, 40, 40])
    upper_dark_green = np.array([40, 255, 255])

    # Estado 3: Marrón/Negro (Maduro)
    lower_brown_black = np.array([10, 40, 40])
    upper_brown_black = np.array([25, 255, 255])

    # Estado 4: Negro intenso (Pasado de maduro)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([10, 255, 255])

    # Crear máscaras para cada estado de madurez
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_dark_green = cv2.inRange(hsv, lower_dark_green, upper_dark_green)
    mask_brown_black = cv2.inRange(hsv, lower_brown_black, upper_brown_black)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # Aplicar las máscaras al frame original para obtener la segmentación
    segmented = cv2.bitwise_and(frame, frame, mask=mask_green + mask_dark_green + mask_brown_black + mask_black)

    # Calcular la cantidad de píxeles no negros en cada máscara
    green_pixels = cv2.countNonZero(mask_green)
    dark_green_pixels = cv2.countNonZero(mask_dark_green)
    brown_black_pixels = cv2.countNonZero(mask_brown_black)
    black_pixels = cv2.countNonZero(mask_black)

    # Determinar el estado de madurez en función de los píxeles detectados
    if green_pixels > max(dark_green_pixels, brown_black_pixels, black_pixels):
        state = "Verde"
    elif dark_green_pixels > max(green_pixels, brown_black_pixels, black_pixels):
        state = "Pre maduro"
    elif brown_black_pixels > max(green_pixels, dark_green_pixels, black_pixels):
        state = "Maduro"
    else:
        state = "Sobre Maduro"

    return segmented, state

# Función principal
def main():
    # Inicializar la cámara
    cap = cv2.VideoCapture(1)


    while True:
        # Capturar frame por frame

        pantalla = tk.Tk()
        pantalla.title("Clasificador de Aguacates")
        pantalla.geometry("1280x720")

        ret, frame = cap.read()
        if not ret:
            break

        # Detectar el estado de madurez en el frame
        segmented_image, state = detect_ripe_state(frame)

        # Mostrar el texto del estado de madurez en el frame segmentado
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(segmented_image, f"Estado: {state}", (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Mostrar la imagen original y la imagen segmentada con el estado de madurez
        cv2.imshow('Imagen Original', frame)
        cv2.imshow('Deteccion de Madurez de Aguacate', segmented_image)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
