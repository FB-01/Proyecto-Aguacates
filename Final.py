from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import imutils
import cv2

def clean():
    lblimg.config(image='')

def images(img):
    img = img

    # Img Detect
    img = np.array(img, dtype="uint8")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = Image.fromarray(img)

    img_ = ImageTk.PhotoImage(image=img)
    lblimg.configure(image=img_)
    lblimg.image = img_

def actualizar_video():
    global cap, lblVideo, lblVideo2
    global img_verde, img_premad, img_mad, img_sobmad, pantalla
    global lblimg

    # Interfaz
    lblimg = Label(pantalla)
    lblimg.place(x=138, y=545)

    # Leer VideoCaptura
    ret, frame = cap.read()
    if ret:
        # Convertir el frame a HSV
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Redimensionar para mostrar
        frame_show = imutils.resize(frame, width=461)
        frame_hsv_resized = imutils.resize(frame_hsv, width=461)

        # Definición de los 4 Estándares del Estado de Madurez
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])

        lower_dark_green = np.array([25, 40, 40])
        upper_dark_green = np.array([40, 255, 255])

        lower_brown_black = np.array([10, 40, 40])
        upper_brown_black = np.array([25, 255, 255])

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([10, 255, 255])

        # Crear máscaras para cada estado de madurez
        mask_green = cv2.inRange(frame_hsv, lower_green, upper_green)
        mask_dark_green = cv2.inRange(frame_hsv, lower_dark_green, upper_dark_green)
        mask_brown_black = cv2.inRange(frame_hsv, lower_brown_black, upper_brown_black)
        mask_black = cv2.inRange(frame_hsv, lower_black, upper_black)

        # Calcular la cantidad de píxeles no negros en cada máscara
        green_pixels = cv2.countNonZero(mask_green)
        dark_green_pixels = cv2.countNonZero(mask_dark_green)
        brown_black_pixels = cv2.countNonZero(mask_brown_black)
        black_pixels = cv2.countNonZero(mask_black)

        # Determinar el estado de madurez
        if green_pixels > max(dark_green_pixels, brown_black_pixels, black_pixels):
            state = "Verde"
            images(img_verde)
        elif dark_green_pixels > max(green_pixels, brown_black_pixels, black_pixels):
            state = "Pre Maduro"
            images(img_premad)
        elif brown_black_pixels > max(green_pixels, dark_green_pixels, black_pixels):
            state = "Maduro"
            images(img_mad)
        elif black_pixels >= black_pixels:
            state = "Sobre Maduro"
            images(img_sobmad)
        else:
            clean()

        # Aplicar las máscaras al frame original para obtener la segmentación
        segmented_image = cv2.bitwise_and(frame, frame, mask=mask_green + mask_dark_green + mask_brown_black + mask_black)

        # Mostrar el texto del estado de madurez en el frame segmentado
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"Estado: {state}"
        (text_width, text_height), baseline = cv2.getTextSize(text, font, 0.5, 2)

        # Ajustar la posición
        text_x = 50
        text_y = 50 + text_height

        cv2.putText(segmented_image, text, (text_x, text_y), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Redimensionar la imagen segmentada para mostrar
        segmented_image_resized = imutils.resize(segmented_image, width=461)

        # Convertimos el video a formato adecuado para Tkinter
        img = Image.fromarray(cv2.cvtColor(frame_show, cv2.COLOR_BGR2RGB))
        img_hsv = Image.fromarray(cv2.cvtColor(segmented_image_resized, cv2.COLOR_BGR2RGB))

        # Actualizar etiquetas con las imágenes
        lblVideo.img = ImageTk.PhotoImage(image=img)
        lblVideo.configure(image=lblVideo.img)

        lblVideo2.img = ImageTk.PhotoImage(image=img_hsv)
        lblVideo2.configure(image=lblVideo2.img)

        # Llamar a la función nuevamente después de 10 ms
        lblVideo.after(10, actualizar_video)

def pantalla_principal():
    global cap, lblVideo, lblVideo2, pantalla, img_verde, img_premad, img_mad, img_sobmad

    # Ventana principal
    pantalla = Tk()
    pantalla.title("Guac-AI")
    pantalla.geometry("1280x720")

    # Asignación de fondo
    bgimg = PhotoImage(file="bg.PNG")
    background = Label(pantalla, image=bgimg, text="Inicio")
    background.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Video
    lblVideo = Label(pantalla)
    lblVideo.place(x=140, y=170)  # Pantalla original
    lblVideo2 = Label(pantalla)
    lblVideo2.place(x=675, y=170)  # Pantalla HSV

    # Informacion
    img_verde = cv2.imread("verde.PNG")
    img_premad = cv2.imread("premaduro.png")
    img_mad = cv2.imread("maduro.png")
    img_sobmad = cv2.imread("sobremaduro.png")

    # Camara
    global cap
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    # Iniciar la actualización de video
    actualizar_video()
    pantalla.mainloop()

if __name__ == "__main__":
    pantalla_principal()