import cv2
import numpy as np
cap = cv2.VideoCapture('MENINO01.wmv') #começa a captura de video(por o nome do video como argumento, e coloca-lo no mesmo diretorio)

if not cap.isOpened():
    print("Erro")
    exit()

_, p_frame = cap.read() #no video lê a primeira frame
old_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY) #passa a primeira frame para grayScale

#Lukas Kanade params
lk_params = dict(winSize = (15, 15),
                 maxLevel = 4,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

point_selected = False
flag = 1
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # width do frame
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # height do frame
fps = 30.0
fourcc = cv2.VideoWriter_fourcc(*'XVID')    # define saida

# Mouse Function
def addPoint(x, y):# À medida que são selecionados pontos estes são adicionados ao array
    global old_points, origin_points
    a_point = np.array([[x, y]], dtype=np.float32) # formata as coordenadas x,y(float32)
    old_points = np.append(a_point, old_points, axis=0)#faz append das coordenadas ao array
    origin_points = np.append(a_point, origin_points, axis=0)

def select_point(event, x, y, flags, params): #Chamada quando se clica no video, registando as coordenadas dos pontos selecionados
    global point, point_selected, old_points, flag, origin_points
    if event == cv2.EVENT_LBUTTONDOWN:#quando se clica no lado esquerdo  do rato
        point_selected = True
        if flag == 1: #cria os arrays que vão ter as coordenadas dos pontos clicados
            old_points = np.array([[x,y]], dtype=np.float32) #array que vai ter as coordenadas dos pontos conforme o movimento
            origin_points = np.array([[x,y]], dtype=np.float32)#array que apenas vai conter as coordenadas dos pontos selecionados no inicio(útil para o loop)
            flag+=1
        else: addPoint(x,y)
        cv2.circle(p_frame, (x, y), 5, (0, 255, 0), -1) #sempre que é clicado na imagem, faz um circulo a volta das coord
        #print(old_points)

# save_video('video.avi', 20, mirror=True)   depois vejo...
def save_video(outPath, fps, mirror=False):
    out = cv2.VideoWriter('abc.avi', fourcc, fps, (int(width), int(height)))
    while(cap.isOpened()):
        if(check==True):
            out.write(frame)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point) #quando se carrega no rato ativa a funçao select_point


out = cv2.VideoWriter('video.avi', fourcc, fps, (int(width), int(height))) # e cria o ojeto VideoWriter para o primeiro while
while True:# Este while serve para a primeira imagem ficar parada até o utilizador pressionar ('p') -> util para o utilizador selecionar os pnts
    cv2.imshow('Frame', p_frame)

    if cv2.waitKey(27) & 0xFF == ord('p'):
            break

out = cv2.VideoWriter('video.avi', fourcc, fps, (int(width), int(height))) # # e cria o objeto VideoWriter para o segundo while
while True:

    check ,frame = cap.read() #le frame a frame

    if not check:# entra neste if quando acaba os frames do video, abre-se outra captura para manter em loop

        cap1 = cv2.VideoCapture('MENINO01.wmv')#abrir nova captura

        if not cap1.isOpened():
            print("Erro")
            exit()

        _, p_frame = cap1.read()  #le o frame anterior
        old_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)#converte a frame para gray

        _, frame1 = cap1.read() #le o frame atual
        gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)#converte a frame para gray
        cap = cap1 #atualiza as variaveis
        frame = frame1
        old_points = origin_points


    else:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if point_selected is True: #Uma vez que um ponto é selecionado faz o Tracking

        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, gray_frame, old_points, None, **lk_params) #tracking Luccas Kanade, Optial flow
        old_frame = gray_frame.copy()#a frame em que eatamos passa a ser a anterior do próximo ciclo

        old_points = new_points #os new points são as coordenadas dos pontos apos a movimentação

        for x,y in new_points:#por todos s novos pontos desenha um circulo verde à volta
            cv2.circle(frame, (x,y), 5, (0,255,0), 2)

    out.write(frame)    # grava o video depois dos pontos selecionados/ começa a gravar depois de premida a letra 'p' e grava continuadamente até se premida a tecla ESC
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(20)

    if key == 27: #ESC
        break
        close += 1


cap.release()
cv2.destroyAllWindows()