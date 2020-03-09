import cv2

import numpy as np

vid = cv2.VideoCapture('QUARTA01.wmv')  # Abrir Video
ret, frame = vid.read()

polygon=list([])   #lista de todos os pontos selecionados!!
def mouseCallback(event, x, y, flags, param):  # Seletor de pontos quando buttao esquerdo é clicado

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x,y),5,(0,255,0),-1)
        polygon.append((x, y))


# _____________________---------------Primeiro Frame do Vídeo-----------__________________________________________-
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouseCallback)

# desenhar o circulo
while(True):
    cv2.imshow('frame', frame)

    if  cv2.waitKey(27) & 0xFF ==ord('p'):
        break

# _____________________-------------Aposta tecla 'p' premida corre o video------_____________________________________-
print(polygon)
while vid.isOpened():
    ret, frame = vid.read()

    cv2.imshow('frame', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
