import cv2
import numpy as np
import os, re, os.path, math, operator
from functools import reduce
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict
from scipy.spatial import distance
import imutils
from imutils import contours
import sys

# adicionar aqui as funções
class code():
    def __init__(self, video_path, framesPerVector= 3, minDist= 2):
        self.scale_percent = 115  # percentagem de aumento do video - default 100%
        self.video_path = video_path
        # Lukas Kanade params
        self.lk_params_dist = dict(winSize = (30, 30),      # valores de tracking diferentes para acompanhar pontos singulares/video longitudinal
                         maxLevel = 4,
                         criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.lk_params = dict(winSize = (30, 30),
                         maxLevel = 4,
                         criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.cap = cv2.VideoCapture(video_path)                                               # começa a captura de video(por o nome do video como argumento, e coloca-lo no mesmo diretorio(para já))
        print(self.video_path)
        print((self.cap).isOpened())
        _, self.frame = self.cap.read()                                                          # no video lê a primeira frame
        self.frame = self.resize(self.frame)
        self.old_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)                            # passa a primeira frame para grayScale
        # definir/iniciar variáveis aqui
        self.vectors_factor = 3 #fator de visualização dos arrays
        self.q = 0
        self.dif = int(minDist)
        self.framesPerVector = int(framesPerVector)
        self.tmp = []
        self.tmp1 = []
        self.tmp2 = []
        self.tmp3 = []
        self.tmp4 = []
        self.tmp5 = []
        self.tmp6 = []
        self.tmp7 = []
        self.counts = defaultdict(int)
        self.cardinal_points = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.point_selected = False
        self.flag = 1
        self.flag1 = 1
        self.flag2 = 1
        self.width = (self.cap).get(cv2.CAP_PROP_FRAME_WIDTH)                                        # width do frame
        self.width = int(self.width * self.scale_percent / 100)
        self.height = (self.cap).get(cv2.CAP_PROP_FRAME_HEIGHT)                                      # height do frame
        self.height = int(self.height * self.scale_percent / 100)
        self.fps = 30.0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')                                         # define saida
        self.filename = 'video.avi'
        #out = cv2.VideoWriter(load_file(filename), fourcc, fps, (int(width), int(height))) # cria o objeto VideoWriter, comentei p não estar sp a gravar
        self.t = 0
        self.vector_points = np.array([[]], dtype=np.float32)                                # variável que contem os pontos n frames antes, para fazer os vetores
        self.vector_distance_2points = np.array([[]], dtype=np.float32)                      # variavel que contem os 2 pontos para calcular a distancia
        self.vector_distance_perpendicular_2points = np.array([[]], dtype=np.float32)        # variavel que contem os 2 pontos para calcular a distancia perpendicular
        self.old_points = np.array([[]], dtype=np.float32)
        self.new_points = np.array([[]], dtype=np.float32)
        self.origin_points = np.array([[]], dtype=np.float32)
        self.flagDistance = False
        self.flagDistancePerpendicular = False
        self.spline= np.zeros_like(self.frame)
        self.conversao = None
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.org = (int(self.width-560), int(self.height-45))
        self.org2 = (int(self.width - 560), int(self.height - 20))
        self.org3 = (int(self.width - 260), int(self.height - 30))
        self.fontScale = 1
        self.color = (0, 0, 255)
        self.color2 = (255, 0, 255)
        self.color3 = (255, 255, 255)
        self.key = None
        self.thickness = 2
        self.array_distance_first_frame = np.array([[]], dtype=np.float32)
        self.array_distance_perpendicular_first_frame = np.array([[]], dtype=np.float32)
        self.flag_hist = 1
        self.pause = True

        # Mouse Function

    def execute(self):
        #cv2.namedWindow("Frame")
        #cv2.setMouseCallback("Frame", self.select_point)                                      # quando se carrega no rato ativa a funçao select_point
        self.conversao = self.findScale(self.frame)

        if self.pause:                                                                      # este while serve para a primeira imagem ficar parada até o utilizador pressionar ('p') -> util para o utilizador selecionar os pnts

            #cv2.imshow('Frame', self.frame)

            if len(self.vector_distance_2points) == 2: # tem que estar no select_point
                self.flagDistance = False
                self.array_distance_first_frame = self.vector_distance_2points

            if len(self.vector_distance_perpendicular_2points) == 2:
                self.flagDistancePerpendicular = False
                self.array_distance_perpendicular_first_frame = self.vector_distance_perpendicular_2points

        else:

            check, self.frame = self.cap.read()                                                   # le frame a frame
            self.t += 1

            if check:
                self.frame = self.resize(self.frame)

            if not check:                                                               # entra neste if quando acaba os frames do video, abre-se outra captura para manter em loop
                print(self.counts)
                #self.counts = defaultdict(int)
                print("o")
                print(self.counts)

                # self.tmp7 = []

                cap1 = cv2.VideoCapture(self.video_path)# abrir nova captura
                if not cap1.isOpened():
                    print("Erro")
                    exit()
                _, self.frame = cap1.read()                                                # le o frame anterior
                self.old_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)                   # converte a frame para gray
                self.old_frame = self.resize(self.old_frame)
                _, self.frame1 = cap1.read()                                                 # le o frame atual
                self.frame1 = self.resize(self.frame1)
                self.gray_frame = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2GRAY)                   # converte a frame para gray
                self.cap = cap1                                                              # atualiza as variaveis
                self.frame = self.frame1
                self.old_points = self.origin_points
                self.q = 0
                self.vector_points = np.array([[]], dtype=np.float32)                        # variável que contem os pontos n frames antes, para fazer os vetores
                self.t = 0
                self.vector_distance_2points = self.array_distance_first_frame
                self.vector_distance_perpendicular_2points = self.array_distance_perpendicular_first_frame
                self.flag_hist = 0                                                          #já acabou o ciclo não desenha mais histograma

            else:
                self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            if self.point_selected is True:                                                  # Uma vez que um ponto é selecionado faz o Tracking
                if self.old_points.size != 0:
                    self.new_points, self.status, self.error = cv2.calcOpticalFlowPyrLK(self.old_frame, self.gray_frame, self.old_points, None, **self.lk_params) # tracking Luccas Kanade, Optial flow
                    if self.t == self.framesPerVector:                                                              # reset de arrays p every 10 frames
                        self.vector_points = self.old_points
                        self.t = 0                                                                # reset da variavel
                    self.draw_vectors_and_set_histogram(self.new_points, self.vectors_factor)              #atualiza as variaveis para o histograma e desenha os vetores
                    self.old_points = self.new_points                                                 # os new points são as coordenadas dos pontos apos a movimentação
                    self.spline = self.draw_spline(self.spline, self.new_points)                              #draw spline with the new points
                    self.frame = cv2.add(self.frame, self.spline)                                         # fazer o overlay do contour na main frame
                    if self.q == 0:                                                             #só faz o resampling 1 vez
                        self.track_points = self.resample_points(self.spline, self.dif)
                        self.old_points = self.track_points
                        self.vector_points = self.track_points
                        self.q = 1

                    self.spline = np.zeros_like(self.spline)                                        # reset

                if len(self.vector_distance_2points) == 2:
                    self.distanciaIntroduzida = self.hipote(self.vector_distance_2points[0][0], self.vector_distance_2points[0][1],
                                                  self.vector_distance_2points[1][0], self.vector_distance_2points[1][1])
                    self.vector_distance_2points = self.trackDistancePoints()
                    self.distanciaMM = self.distanciaIntroduzida / self.conversao  # imprime frame a frame a distancia
                    self.distanciaMM = round((self.distanciaMM)*10, 3)
                    self.flagDistance = False
                    image = cv2.putText(self.frame, "d1 = " +str(self.distanciaMM)+ " mm", self.org, self.font, self.fontScale, self.color, self.thickness, cv2.LINE_AA)

                if len(self.vector_distance_perpendicular_2points) == 2:
                    self.distanciaIntroduzidaPerpendicular = self.hipote(self.vector_distance_perpendicular_2points[0][0], self.vector_distance_perpendicular_2points[0][1],
                                                  self.vector_distance_perpendicular_2points[1][0], self.vector_distance_perpendicular_2points[1][1])
                    self.vector_distance_perpendicular_2points = self.trackDistancePointsPerpendicular()
                    self.distanciaMMPerpendicular = self.distanciaIntroduzidaPerpendicular / self.conversao  # imprime frame a frame a distancia
                    self.distanciaMMPerpendicular = round((self.distanciaMMPerpendicular)*10, 3)
                    self.flagDistancePerpendicular = False
                    image2 = cv2.putText(self.frame, "d2 = " + str(self.distanciaMMPerpendicular) + " mm", self.org2, self.font, self.fontScale, self.color2, self.thickness, cv2.LINE_AA)
                if self.new_points.size != 0:
                    self.area = self.contourArea(self.new_points)
                    self.area = round((self.area / self.conversao), 3)

                    imageArea = cv2.putText(self.frame, "area = " + str(self.area) + "mm²", self.org3, self.font, self.fontScale, self.color3, self.thickness, cv2.LINE_AA)

            self.old_frame = self.gray_frame.copy()  # a frame em que estamos passa a ser a anterior do próximo ciclo
                # comentado p nao estar sp a grvar
                # out.write(frame)    # grava o video depois dos pontos selecionados/ começa a gravar depois de premida a letra 'p' e grava continuadamente até se premida a tecla ESC
            #cv2.imshow("Frame", self.frame)



        #self.arrayMedidas = [sum(self.tmp), sum(self.tmp1), sum(self.tmp2), sum(self.tmp3), sum(self.tmp4),sum(self.tmp5), sum(self.tmp6), sum(self.tmp7)]

        #self.histogram(self.arrayMedidas, self.arrayArrows)

        # plt.show()
    def showHistogram(self):
        self.arrayMedidas = [sum(self.tmp), sum(self.tmp1), sum(self.tmp2), sum(self.tmp3), sum(self.tmp4),sum(self.tmp5), sum(self.tmp6), sum(self.tmp7)]
        self.histogram(self.arrayMedidas, self.arrayArrows)
        plt.show()


    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def resize(self, frame):
        width = int(frame.shape[1] * self.scale_percent / 100)
        height = int(frame.shape[0] * self.scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

        return frame

    def histogram(self, array1, array2):

        bars = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        y_pos = np.arange(len(bars))
        ax = plt.subplot(2, 1, 1)
        # Add title and axis names
        ax.set_title('Movement histogram')
        ax.set_ylabel('Moved distance(mm)')
        histograma = ax.bar(y_pos + 0.1, array1, width=0.4, color='steelblue', align='center', label='Distance(mm)')
        # print("check")
        # print(array2[0])
        # Create names
        plt.xticks(y_pos, bars)
        leg = ax.legend();

        bars1 = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        y_pos1 = np.arange(len(bars))
        ax1 = plt.subplot(2, 1, 2)
        ax1.set_xlabel('Cardinal Points')
        ax1.set_ylabel('Number of vectors')
        histograma1 = ax1.bar(y_pos1 + 0.1, array2, width=0.4, color='darkgray', align='center',
                              label='Number of vectors')
        # print("check")
        # print(array2[0])
        # Create names
        plt.xticks(y_pos1, bars1)
        leg1 = ax1.legend();
        return histograma, histograma1

    def hipote(self, x1, y1, x2, y2):               # teorema de pitagoras
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


    def direcao(self, x_final, x_inicial, y_final, y_inicial):
        differenceX = x_final - x_inicial
        differenceY = y_final - y_inicial
        graus = math.atan2(differenceX, differenceY)/math.pi*180
        if graus < 0:
            final_degrees = 360 + graus
        else:
            final_degrees = graus
        cardinal = ["S", "SW", "E", "NE", "N", "NW", "W", "SW", "S"]
        compass_lookup = round(final_degrees / 45)
        return cardinal[compass_lookup]

    def load_file(self, file):                                                                #      ver extensao
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

    def add_point(self, x, y):                                                             #à medida que são selecionados pontos estes são adicionados ao array
        global old_points, origin_points
        a_point = np.array([[x, y]], dtype=np.float32)                               #formata as coordenadas x,y(float32)
        self.old_points = np.append(a_point, self.old_points, axis=0)                          #faz append das coordenadas ao array
        self.origin_points = np.append(a_point, self.origin_points, axis=0)

    def add_point_distance(self, x, y):
        global vector_distance_2points
        a_point_distance = np.array([[x, y]], dtype=np.float32)
        self.vector_distance_2points = np.append(a_point_distance, self.vector_distance_2points, axis=0)  # faz append das coordenadas ao array

    def add_point_distance_perpendicular(self, x, y):
        global vector_distance_perpendicular_2points
        a_point_distance = np.array([[x, y]], dtype=np.float32)
        self.vector_distance_perpendicular_2points = np.append(a_point_distance, self.vector_distance_perpendicular_2points, axis=0)  # faz append das coordenadas ao array

    def trackDistancePoints(self):

        new_points, status, error = cv2.calcOpticalFlowPyrLK(self.old_frame, self.gray_frame,
                                                                            self.vector_distance_2points, None,
                                                                            **self.lk_params_dist)  # tracking Luccas Kanade, Optial flow

        for x, y in new_points:
            cv2.circle(self.frame, (x, y), 2, (0, 0, 255), -1)

        return new_points

    def trackDistancePointsPerpendicular(self):

        new_points, status, error = cv2.calcOpticalFlowPyrLK(self.old_frame, self.gray_frame,
                                                                            self.vector_distance_perpendicular_2points, None,
                                                                            **self.lk_params_dist)  # tracking Luccas Kanade, Optial flow

        for x, y in new_points:
            cv2.circle(self.frame, (x, y), 2, (255, 0, 255), -1)

        return new_points

    # save_video('video.avi', 20, mirror=True)   depois vejo...

    def save_video(self, outPath, fps, mirror=False):
        out = cv2.VideoWriter('abc.avi', self.fourcc, fps, (int(self.width), int(self.height)))
        while((self.cap).isOpened()):
            if(self.check==True):
                out.write(frame)

    def findScale(self, p_frame):
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

        dist = self.hipote(figuras[0][3][0][0], figuras[0][3][0][1], figuras[1][2][0][0], figuras[1][2][0][1])

        return dist

    def draw_spline(self, frame_spline, points):
        center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points),
                           [len(points)] * 2))                                                       # centro cartesiano dos pontos

        sortedp = sorted(points,                                                                     # ordenar array em  orientação horária
                         key=lambda coord: (-135 - math.degrees(
                             math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)

        poly = cv2.approxPolyDP(np.array([sortedp], dtype=np.int32), 1, True)                        # aproximação curvilinea do contorno

        contour = cv2.drawContours(frame_spline, [poly], 0, (0, 255, 0), 1)                          # desenho do contorno na "frame "contour

        return contour

    def contourArea(self, points):
        center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points),
                           [len(points)] * 2))  # centro cartesiano dos pontos

        sortedp = sorted(points,  # ordenar array em  orientação horária
                         key=lambda coord: (-135 - math.degrees(
                             math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)

        poly = cv2.approxPolyDP(np.array([sortedp], dtype=np.int32), 1, True)  # aproximação curvilinea do contorno
        area = cv2.contourArea(poly)
        #print("Area")
        #print(area)
        return area

    def draw_vectors_and_set_histogram(self, points_to_track, f1):
        global frame, vector_points, arrayArrows
        global tmp , tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7
        i = 0
        for x, y in points_to_track:
            cv2.circle(self.frame, (x, y), 1, (0, 255,), -1)
            if self.vector_points.size == points_to_track.size:
                grad_x, grad_y = x - self.vector_points[i][0], y - self.vector_points[i][1]
                val_x = int(x + (f1 * grad_x))                                              #fator
                val_y = int(y + (f1 * grad_y))
                cv2.arrowedLine(self.frame, (x, y), (val_x, val_y), (0, 255, 255), 1)      #f1 fator de aumento, para melhor visualização, ainda n foi posto

                if self.flag_hist == 1:                                                          #faz 1 so vez, depois do primeiro ciclo a variavel é atualizada
                    tamanho = self.hipote(x, y, x + grad_x, y + grad_y)
                    tamanho = tamanho / self.conversao
                    # print(tamanho)
                    exit = self.direcao(x + grad_x, x, y + grad_y,
                                   y)  # prints the direction of the cardinal points between two points!!
                    # print(exit)
                    if exit == self.cardinal_points[
                        0]:  # tamanho pixeis de cada posição 'N' ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                        self.tmp.append(tamanho)

                    if exit == self.cardinal_points[1]:  # 'NE'
                        #print("test")
                        self.tmp1.append(tamanho)

                    if exit == self.cardinal_points[2]:  # 'E'
                        self.tmp2.append(tamanho)
                        # print(tmp2)
                    if exit == self.cardinal_points[3]:  # 'SE'
                        self.tmp3.append(tamanho)
                        # print(tmp3)
                    if exit == self.cardinal_points[4]:  # 'S'
                        self.tmp4.append(tamanho)
                        # print(tmp4)
                    if exit == self.cardinal_points[5]:  # 'SW'
                        self.tmp5.append(tamanho)
                        # print(tmp5)
                    if exit == self.cardinal_points[6]:  # 'W'
                        self.tmp6.append(tamanho)
                        # print(tmp6)
                    if exit == self.cardinal_points[7]:  # 'NW'
                        self.tmp7.append(tamanho)
                        # print(tmp7)

                    for cardinal_point in self.cardinal_points:
                        # this assumes exit.count() returns an int
                        self.counts[cardinal_point] += exit.count(cardinal_point)  # counts the number of times North appears

                    # tmp.append((hipote(x,y,x+grad_x,y+grad_y)))
                    # print(tmp)
            i += 1
                # print(exit.count('N'))
                # print(hipote(x,y,x+grad_x,y+grad_y))   #  shows the distance between these two points

        for cardinal_point, count in self.counts.items():
            # print(f'{cardinal_point} appears a total of {count} times.')
            self.arrayArrows = [i for i in self.counts.values()]
            #print(arrayArrows)

    def order_points(self, A):
        # Sort A based on Y(col-2) coordinates
        sortedAc2 = A[np.argsort(A[:,1]),:]

        # Get top two and bottom two points
        top2 = sortedAc2[0:2,:]
        bottom2 = sortedAc2[2:,:]

        # Sort top2 points to have the first row as the top-left one
        sortedtop2c1 = top2[np.argsort(top2[:,0]),:]
        top_left = sortedtop2c1[0,:]

        # Use top left point as pivot & calculate sq-euclidean dist against
        # bottom2 points & thus get bottom-right, bottom-left sequentially
        sqdists = distance.cdist(top_left[None], bottom2, 'sqeuclidean')
        rest2 = bottom2[np.argsort(np.max(sqdists,0))[::-1],:]

        # Concatenate all these points for the final output
        return np.concatenate((sortedtop2c1,rest2),axis =0)

    def format_array(self, track_array):
        f_array = np.array(track_array[0], dtype = np.float32)

        for x in track_array[1:]:
            add = np.array(x, dtype = np.float32)
            f_array = np.append(add,f_array, axis = 0)
        return f_array

    def resample_points(self, spline, dif):                                               #devolve um arrray de pontos ao longo da spline com uma distancia de "dif"

        spline_gray = cv2.cvtColor(spline, cv2.COLOR_BGR2GRAY)                      # passar para gray
        mask = cv2.findContours(spline_gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)   # detetar contorno na imagem do gray frame

        points = np.unique((mask[0][0]), axis=0)                                         # sem rep
        points = self.format_array(points)
        points = self.order_points(points)

        past_elem = np.array([[]], dtype=np.float32)

        q = 0
        for z in points:
            if q == 0:
                track_points = np.array([z], dtype=np.float32)
                q = 1
            else:
                if past_elem.size == 0:
                    past_elem = z
                if np.linalg.norm(z - past_elem) > dif:
                    add = np.array([z], dtype=np.float32)
                    track_points = np.append(add, track_points, axis=0)
                    past_elem = z

        return track_points

if __name__ == '__main__':
    code("MENINO01.wmv").execute()