######### Importación de Librerias
import cv2
import os
import cvzone
from cvzone.ClassificationModule import Classifier
from time import sleep
import serial

cad = 0
paso = 0
cuenta = 0
step = 0

######### Arduino
dev = serial.Serial('/dev/cu.usbserial-1420',9600)
print('Conexión exitosa. Listo para ejecutar......')

######### Importamos las imagenes representativas
imgWasteList = []
pathFolderWaste = "Resources/Icons"
pathList = os.listdir(pathFolderWaste)
for path in pathList:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste,path),cv2.IMREAD_UNCHANGED))


######### Apertura de Camara y modelos de clasificación Keras
cap = cv2.VideoCapture(0)
classifier = Classifier('Resources/Model/keras_model.h5','Resources/Model/labels.txt')

while True:
    while step == 0:
        print('Paso 0 - Esperando Respuesta de sensor de presencia.')
        cad = dev.readline().decode('ascii')
        cad = int(cad)
        if (cad == 1):
            step = 1
            cad = 0

    while step == 1:
        if paso == 0: # Captura de imagen
            _ , img = cap.read()
            img = cv2.imwrite('img.png',img)
            paso = 1

        if paso == 1:
            img = cv2.imread('img.png')
            print('Leida')
            imgResize = cv2.resize(img,(422,241))
            imgBackground = cv2.imread('Resources/Model/FONDO.png')
            paso = 2

        if paso == 2:
            predection = classifier.getPrediction(img)
            classID = predection[1]
            print(classID)
            paso = 3

        if paso == 3:
            if classID != 0:
                imgBackground = cvzone.overlayPNG(imgBackground,imgWasteList[classID],(557,142))
                predection = None
                if classID == 1:
                    #imgBackground = cvzone.overlayPNG(imgBackground,imgWasteList[classID],(557,142))
                    print('Plastico')
                    dev.write(b'9')
                    print('Hecho, motor 1 arrancado...')
                    cad = 0
                    paso = 5
                    cuenta = 0
                    step = 0

                if classID == 2:
                    #imgBackground = cvzone.overlayPNG(imgBackground,imgWasteList[classID],(557,142))
                    print('Orgánico')
                    dev.write(b'8')
                    print('Hecho, motor 2 arrancado...')
                    cad = 0
                    paso = 5
                    cuenta = 0
                    step = 0
                if classID == 3:
                    #imgBackground = cvzone.overlayPNG(imgBackground,imgWasteList[classID],(557,142))
                    print('Metal')
                    dev.write(b'7')
                    print('Hecho, motor 3 arrancado...')
                    cad = 0
                    paso = 5
                    cuenta = 0
                    step = 0
                if classID == 4:
                    #imgBackground = cvzone.overlayPNG(imgBackground,imgWasteList[classID],(557,142))
                    print('Baterias')
                    dev.write(b'6')
                    print('Hecho, motor 4 arrancado...')
                    cad = 0
                    paso = 5
                    cuenta = 0
                    step = 0
            else:
                print('NO OBJECT DETECTED')
                print('La cuenta es de ::::::   ',cuenta)
                cuenta += 1
                paso = 4
                if cuenta >= 25:
                    step = 0
                    cuenta = 0 
                    cad = 0

        if paso == 4:
            imgBackground[153:153 + 241, 36:36 + 422] = imgResize
            cv2.imshow('Image',img)
            cv2.imshow('Salida',imgBackground)
            paso = 0

        if paso == 5:
            imgBackground[153:153 + 241, 36:36 + 422] = imgResize
            cv2.imshow('Image',img)
            cv2.imshow('Salida',imgBackground)
            step = 0
            paso = 0

    if cv2.waitKey(1) == 27:
        print('Program Finished')
        break