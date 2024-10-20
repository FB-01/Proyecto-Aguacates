#Librerias
import tkinter as tk
from PIL import Image, ImageTk
import imutils
import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)

lower=np.array([15,17,125])
high=np.array([70,59,231])


#Funcion escanear
def escanear():
    #Leer video
    if cap is not None:
        ret, frame = cap.read()

        frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret == True:
            #Resize
            frame_show = imutils.resize(frame_show, width=460)
            #Convertir video
            im = Image.fromarray(frame_show)

            img = ImageTk.PhotoImage(image=im)
            #Mostrar

            mask=cv2.inRange(frame,lower,high)
            imgn=cv2.bitwise_and(frame,frame,mask=mask)
    
            cv2.imshow('OBJETO ROJO',imgn)

            lblVideo.configure(image = img)
            lblVideo.image = img
            lblVideo.after(10, escanear)
           
        else:
            cap.release()

#main
def ventana_principal():
    global modelo, clsName, img_verde, img_tocado, img_arrancado, img_premad, img_mad, img_sobmad, cap, lblVideo

    #Ventana principal
    pantalla = tk.Tk()
    pantalla.title("Clasificador de Aguacates")
    pantalla.geometry("1280x720")

    #Asignación de fondo
    bgimg = tk.PhotoImage(file="bg.PNG")



    background = tk.Label(pantalla, image=bgimg, text="Inicio")
    background.place(relx=0, rely=0, relwidth=1, relheight=1)



    

    #Modelo
    #modelo = YOLO('')

    #Clases
    clsName = ['Verde', 'Tocado', 'Arrancado', 'Pre Maduro', 'Maduro', 'Sobre Maduro']

    #Informacion
    img_verde = cv2.imread("verde.PNG")
    img_tocado = cv2.imread("tocado.PNG")
    img_arrancado = cv2.imread("arrancado.PNG")
    img_premad = cv2.imread("premaduro.png")
    img_mad = cv2.imread("maduro.png")
    img_sobmad = cv2.imread("sobremaduro.png")

    #Video
    lblVideo = tk.Label(pantalla)
    lblVideo.place(x=140, y=170)

    lblVideo2 = tk.Label(pantalla)
    lblVideo2.place(x=140, y=370)




    #Camara
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    #Escaner
    escanear()

    #Loop
    pantalla.mainloop()

if __name__ == "__main__":
    ventana_principal()


