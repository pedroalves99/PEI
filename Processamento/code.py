import cv2
import numpy as np
import os, re, os.path, math, operator
from functools import reduce
import matplotlib.pyplot as plt
import pandas
from collections import Counter
from collections import defaultdict
import random
import imutils
from imutils import contours


# adicionar aqui as funções


def histogram(array1, array2):
    bars = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    y_pos = np.arange(len(bars))
    ax = plt.subplot(1, 1, 1)

    # Add title and axis names
    ax.set_title('Movement histogram')
    ax.set_xlabel('Cardinal Points')
    ax.set_ylabel('Arrows/Moved points')
    histograma = ax.bar(y_pos - 0.1, array1, width=0.4, color='steelblue', align='center', label = 'Number of arrows') and ax.bar(y_pos + 0.1, array2, width=0.4, color='darkgray', align='center', label = 'Moved distance(px)')
    # Create names
    plt.xticks(y_pos, bars)
    leg = ax.legend();
    return histograma


def hipote(x1, y1, x2, y2):               # teorema de pitagoras
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def direcao(x_final, x_inicial, y_final, y_inicial):
    differenceX = x_final - x_inicial
    differenceY = y_final - y_inicial
    graus = math.atan2(differenceX, differenceY)/math.pi*180
    if graus < 0:
        final_degrees = 360 + graus
    else:
        final_degrees = graus
    cardinal = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    compass_lookup = round(final_degrees / 45)
    return cardinal[compass_lookup]


def load_file(file):                                                                #      ver extensao
  number = []
  onlyfiles = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]  # load todos os files diretorios
  filename, file_extension = os.path.splitext(file)                                 # load do nome do ficheiro e da extensao
  alll_files = len(onlyfiles)                                                      # obter todos os ficheiros do diretorio
  split = re.compile(r'\d+')                                                     # split do numero do nome do ficheiro
  number = split.findall(filename) or ['0']                                      # obter o numero do ficheiro
  only_name = filename.replace(number[0], '')                                    # obter só o nome do ficheiro removendo o numero
  i = 0
  found = [s for s in onlyfiles if only_name in s]                               # construir array apenas com nomes de arquivos que correspondem ao only_name (do nome do arquivo)
  if len(found) == 0:                                                            # se nao encontrar nenhum retorna o próprio
      return file
  while i < len(found):                                                          # itera o array dos ficheiros encontrados e retira o numero
    number.append((split.findall(found[i]) or [0])[0])                           # adiciona para o array number o numero encontrado
    i += 1
  number = [int(i) for i in number]                                              # converte todos os numeros do array para int (cast), alguns sao strings
  maxx_number = max(number)                                                      # obtem o valor maximo
  return '{0}{1}{2}'.format(only_name, str(maxx_number + 1), file_extension)

# Mouse Function


def select_point(event, x, y, flags, params):                                    #Chamada quando se clica no video, registando as coordenadas dos pontos selecionados
    global point, point_selected, old_points, flag, origin_points, flagDistance, vector_distance_2points, flag1
    if event == cv2.EVENT_LBUTTONDOWN:                                           #quando se clica no lado esquerdo  do rato
        point_selected = True
        print("flagDistance")
        print(flagDistance)
        if not flagDistance:

            if flag == 1:                                                            #cria os arrays que vão ter as coordenadas dos pontos clicados
                old_points = np.array([[x,y]], dtype=np.float32)                     #array que vai ter as coordenadas dos pontos conforme o movimento
                origin_points = np.array([[x,y]], dtype=np.float32)                  #array que apenas vai conter as coordenadas dos pontos selecionados no inicio(útil para o loop)
                flag += 1
            else:
                add_point(x, y)

        else:
            if flag1 == 1:
                vector_distance_2points = np.array([[x,y]], dtype=np.float32) #adiciona os 2 pontos selecionados para calcular a distancia
                flag1 += 1
            else:
                add_point_distance(x, y)


        cv2.circle(p_frame, (x, y), 2, (0, 255, 0), -1)                          #sempre que é clicado na imagem, faz um circulo a volta das coord
        # print(old_points)



def add_point(x, y):                                                             #à medida que são selecionados pontos estes são adicionados ao array
    global old_points, origin_points
    a_point = np.array([[x, y]], dtype=np.float32)                               #formata as coordenadas x,y(float32)
    old_points = np.append(a_point, old_points, axis=0)                          #faz append das coordenadas ao array
    origin_points = np.append(a_point, origin_points, axis=0)

def add_point_distance(x, y):
    global vector_distance_2points
    a_point_distance = np.array([[x, y]], dtype=np.float32)
    vector_distance_2points = np.append(a_point_distance, vector_distance_2points, axis=0)  # faz append das coordenadas ao array

# save_video('video.avi', 20, mirror=True)   depois vejo...


def save_video(outPath, fps, mirror=False):
    out = cv2.VideoWriter('abc.avi', fourcc, fps, (int(width), int(height)))
    while(cap.isOpened()):
        if(check==True):
            out.write(frame)

def distanceBetween2points(p_frame):
    global old_points
    contour1 = np.zeros_like(p_frame)
    gray_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_frame, 127, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)

    cnts = cnts[-2:]
    i = 0
    figuras = []

    for x in cnts[-2:]:
        i += 1
        cv2.drawContours(contour1, x, -1, (0, 255, 0), 3)
        # print(i, x)
        figuras.append(x)

    dist = hipote(figuras[0][3][0][0], figuras[0][3][0][1], figuras[1][2][0][0], figuras[1][2][0][1])

    return dist

# Lukas Kanade params
lk_params = dict(winSize = (15, 15),
                 maxLevel = 2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

video_path = "QUARTA04.wmv"
cap = cv2.VideoCapture(video_path)                                               # começa a captura de video(por o nome do video como argumento, e coloca-lo no mesmo diretorio(para já))

if not cap.isOpened():
    print("Erro")
    exit()

_, p_frame = cap.read()                                                          # no video lê a primeira frame
old_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)                            # passa a primeira frame para grayScale


# definir/iniciar variáveis aqui
tmp = []
tmp1 = []
tmp2 = []
tmp3 = []
tmp4 = []
tmp5 = []
tmp6 = []
tmp7 = []
counts = defaultdict(int)
cardinal_points = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
point_selected = False
flag = 1
flag1 = 1
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)                                        # width do frame
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)                                      # height do frame
fps = 30.0
fourcc = cv2.VideoWriter_fourcc(*'XVID')                                         # define saida
filename = 'video.avi'
# out = cv2.VideoWriter(load_file(filename), fourcc, fps, (int(width), int(height))) # cria o objeto VideoWriter, comentei p não estar sp a gravar
t = 0
vector_points = np.array([[]], dtype=np.float32)                                # variável que contem os pontos n frames antes, para fazer os vetores
vector_distance_2points = np.array([[]], dtype=np.float32)                      # variavel que contem os 2 pontos para calcular a distancia
old_points = np.array([[]], dtype=np.float32)
new_points = np.array([[]], dtype=np.float32)
origin_points = np.array([[]], dtype=np.float32)
flagDistance = False

contour = np.zeros_like(p_frame)
conversao = None
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)                                      # quando se carrega no rato ativa a funçao select_point



while True:                                                                      # este while serve para a primeira imagem ficar parada até o utilizador pressionar ('p') -> util para o utilizador selecionar os pnts
    cv2.imshow('Frame', p_frame)

    if cv2.waitKey(27) & 0xFF == ord('p'):
        break

    # cof cof
    if cv2.waitKey(27) & 0xFF == ord('d'):
        flagDistance = True
        conversao = distanceBetween2points(p_frame)
        print(flagDistance)


while True:

    check, frame = cap.read()                                                   # le frame a frame
    t += 1

    if not check:                                                               # entra neste if quando acaba os frames do video, abre-se outra captura para manter em loop

        cap1 = cv2.VideoCapture(video_path)# abrir nova captura

        if not cap1.isOpened():
            print("Erro")
            exit()

        _, p_frame = cap1.read()                                                # le o frame anterior
        old_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)                   # converte a frame para gray

        _, frame1 = cap1.read()                                                 # le o frame atual
        gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)                   # converte a frame para gray
        cap = cap1                                                              # atualiza as variaveis
        frame = frame1
        old_points = origin_points
        vector_points = np.array([[]], dtype=np.float32)                        # variável que contem os pontos n frames antes, para fazer os vetores
    else:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if point_selected is True:                                                  # Uma vez que um ponto é selecionado faz o Tracking

        if old_points.size != 0:
            new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, gray_frame, old_points, None, **lk_params) # tracking Luccas Kanade, Optial flow
            old_frame = gray_frame.copy()                                           # a frame em que estamos passa a ser a anterior do próximo ciclo

            i = 0
            for x,y in new_points:
                cv2.circle(frame, (x, y), 2, (0, 255, ), 1)

                if vector_points.size != 0:
                    grad_x, grad_y = x-vector_points[i][0], y-vector_points[i][1]
                    cv2.arrowedLine(frame, (x,y),(x+grad_x, y+grad_y) , (0,255,255), 1)
                    tamanho = hipote(x, y, x + grad_x, y + grad_y)
                    # print(tamanho)
                    exit = direcao(x + grad_x, x, y + grad_y,y)  # prints the direction of the cardinal points between two points!!
                    # print(exit)
                    if exit == cardinal_points[0]:  # tamanho pixeis de cada posição 'N' ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                        tmp.append(tamanho)
                        # print(tmp)
                    if exit == cardinal_points[1]: # 'NE'
                        tmp1.append(tamanho)
                        # print(tmp1)
                    if exit == cardinal_points[2]: # 'E'
                        tmp2.append(tamanho)
                        # print(tmp2)
                    if exit == cardinal_points[3]: # 'SE'
                        tmp3.append(tamanho)
                        # print(tmp3)
                    if exit == cardinal_points[4]: # 'S'
                        tmp4.append(tamanho)
                        # print(tmp4)
                    if exit == cardinal_points[5]: # 'SW'
                        tmp5.append(tamanho)
                        # print(tmp5)
                    if exit == cardinal_points[6]: # 'W'
                        tmp6.append(tamanho)
                        # print(tmp6)
                    if exit == cardinal_points[7]: # 'NW'
                        tmp7.append(tamanho)
                        # print(tmp7)

                    for cardinal_point in cardinal_points:
                        # this assumes exit.count() returns an int
                        counts[cardinal_point] += exit.count(cardinal_point)  # counts the number of times North appears

                        # tmp.append((hipote(x,y,x+grad_x,y+grad_y)))
                        # print(tmp)

                    # print(exit.count('N'))
                    # print(hipote(x,y,x+grad_x,y+grad_y))   #  shows the distance between these two points

                i += 1

            for cardinal_point, count in counts.items():
                # print(f'{cardinal_point} appears a total of {count} times.')
                arrayArrows = [i for i in counts.values()]
                # print(arrayArrows)

            if t == 10:                                                             # reset de arrays every 10 frames
                vector_points = old_points
                t = 0                                                               # reset da variavel

            old_points = new_points                                                 # os new points são as coordenadas dos pontos apos a movimentação



            center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), new_points), [len(new_points)] * 2))   #centro cartesiano dos pontos

            sortedp = sorted(new_points,                                             # ordenar array em  orientação horária
                   key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)

            poly = cv2.approxPolyDP(np.array([sortedp],dtype=np.int32),1,True)        # aproximação curvilinea do contorno

            contour = cv2.drawContours(contour,[poly],0,(0,255,0),1)                # desenho do contorno na "frame "contour

            contour_gray = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)                # passar para gray
            # cv2.imshow("counter_gray", contour_gray)                       # descomentar para ver a gray frame do contorno
            mask=cv2.findContours(contour_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # detetar contorno na imagem do gray frame
            # cv2.drawContours(contour_gray, mask[i], 0, (255, 0, 0), 1)             # mask[0] é o contorno necessário
            cv2.drawContours(contour, mask[0],0, (0, 255, 0), 1)                  # desenha contorno de mask[0]
            frame = cv2.add(frame, contour)                                         # fazer o overlay do contour na main frame
            # print("pontosSpline:",mask[0])
            cv2.imshow("Frame", frame)
            contour = np.zeros_like(contour)                                        # reset

        # comentado p nao estar sp a grvar
        # out.write(frame)    # grava o video depois dos pontos selecionados/ começa a gravar depois de premida a letra 'p' e grava continuadamente até se premida a tecla ESC


        if flagDistance:
            distanciaIntroduzida = hipote(vector_distance_2points[0][0], vector_distance_2points[0][1],
                                          vector_distance_2points[1][0], vector_distance_2points[1][1])

        if conversao is not None:
            distanciaCM = distanciaIntroduzida / conversao  # imprime frame a frame a distancia
            print(distanciaCM)

    key = cv2.waitKey(27)

    if key == 27: # ESC
        break
        close += 1

arrayMedidas = [sum(tmp), sum(tmp1), sum(tmp2), sum(tmp3), sum(tmp4), sum(tmp5), sum(tmp6), sum(tmp7)]

histogram(arrayArrows, arrayMedidas)
plt.show()



cap.release()
cv2.destroyAllWindows()