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
    def __init__(self, video_path, framesPerVector=3, minDist=2, scale=115):
        self.scale_percent = scale  # percentagem de aumento do video - default 100%
        self.video_path = video_path
        # Lukas Kanade params
        self.lk_params_dist = dict(winSize=(25, 25),
                                   # valores de tracking diferentes para acompanhar pontos singulares/video longitudinal
                                   maxLevel=4,
                                   criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.lk_params = dict(winSize=(25, 25),
                              maxLevel=4,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.cap = cv2.VideoCapture(
            video_path)  # começa a captura de video(por o nome do video como argumento, e coloca-lo no mesmo diretorio(para já))
        print(self.video_path)
        print((self.cap).isOpened())
        _, self.frame = self.cap.read()  # no video lê a primeira frame
        self.frame = self.resize(self.frame)
        self.old_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # passa a primeira frame para grayScale
        # definir/iniciar variáveis aqui
        self.num_frames = 0
        self.vectors_factor = 2  # fator de visualização dos arrays
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
        self.c_tmp = []
        self.c_tmp1 = []
        self.c_tmp2 = []
        self.c_tmp3 = []
        self.c_tmp4 = []
        self.c_tmp5 = []
        self.c_tmp6 = []
        self.c_tmp7 = []
        self.r_tmp = []
        self.r_tmp1 = []
        self.r_tmp2 = []
        self.r_tmp3 = []
        self.r_tmp4 = []
        self.r_tmp5 = []
        self.r_tmp6 = []
        self.r_tmp7 = []


        self.counts = defaultdict(int)
        self.cardinal_points = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.point_selected = False
        self.flag = 1
        self.flag1 = 1
        self.flag2 = 1
        self.flagRef = 1
        self.hasRef =False
        self.flag_c = 0
        self.width = (self.cap).get(cv2.CAP_PROP_FRAME_WIDTH)  # width do frame
        self.width = int(self.width * self.scale_percent / 100)
        self.height = (self.cap).get(cv2.CAP_PROP_FRAME_HEIGHT)  # height do frame
        self.height = int(self.height * self.scale_percent / 100)
        self.fps = 30.0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  # define saida
        # out = cv2.VideoWriter(load_file(filename), fourcc, fps, (int(width), int(height))) # cria o objeto VideoWriter, comentei p não estar sp a gravar
        self.t = 0
        self.x = 0
        self.vector_points = np.array([[]],
                                      dtype=np.float32)  # variável que contem os pontos n frames antes, para fazer os vetores
        self.vector_distance_2points = np.array([[]],
                                                dtype=np.float32)  # variavel que contem os 2 pontos para calcular a distancia
        self.vector_distance_perpendicular_2points = np.array([[]],
                                                              dtype=np.float32)  # variavel que contem os 2 pontos para calcular a distancia perpendicular
        self.old_points = np.array([[]], dtype=np.float32)
        self.new_points = np.array([[]], dtype=np.float32)
        self.origin_points = np.array([[]], dtype=np.float32)
        self.ref_points = np.array([[]], dtype=np.float32)
        self.more_points = np.array([], dtype=np.int32)
        self.more_Refpoints = np.array([], dtype=np.int32)
        self.newref_points = np.array([[]], dtype=np.float32)
        self.flagDistance = False
        self.flagDistancePerpendicular = False
        self.flagRef = False
        self.spline = np.zeros_like(self.frame)
        self.Refspline = np.zeros_like(self.frame)
        self.conversao = None
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.org = (int(self.width - 560), int(self.height - 45))
        self.org2 = (int(self.width - 560), int(self.height - 20))
        self.org3 = (int(self.width - 260), int(self.height - 45))
        self.org4 = (int(self.width - 260), int(self.height - 20))
        self.fontScale = 1
        self.color = (0, 0, 255)
        self.color2 = (255, 0, 255)
        self.color3 = (0, 255, 0)
        self.color4 = (255, 255, 255)
        self.key = None
        self.thickness = 2
        self.array_distance_first_frame = np.array([[]], dtype=np.float32)
        self.array_distance_perpendicular_first_frame = np.array([[]], dtype=np.float32)
        self.ref_points_first_frame = np.array([[]], dtype=np.float32)
        self.flag_hist = 1
        self.pause = True
        self.center = None
        self.centerRef = None
        self.centroideAnterior = None
        self.vector_scale = np.array([[]],dtype=np.float32)  # variavel que contem os 2 pontos para calcular a escala
        self.vector_points_ref = np.array([[]],dtype=np.float32)
        self.manualScaleFlag = False #flag ativada quando nao encontra a escala
        self.doScale = True
        self.okClicked = False
        self.q1 = 0
        self.area_initial = 0
        self.distanceBetweenCentroideX = 0
        self.distanceBetweenCentroideY = 0
        self.distanceBetweenCentroideRefX = 0
        self.distanceBetweenCentroideRefY = 0
        self.flagDistanceCoordenadasCentroide = False
        self.stopDistanceCoordenadasCentroide = False
        self.stopCountFrames = False
        self.arraycentroideX = []
        self.arraycentroideY = []
        self.arraycentroideRefX = []
        self.arraycentroideRefY = []
        self.total_frames = 0
        self.set_frame = 0
        self.record = []
        self.recorded_frames = np.array([[]],dtype=np.float32)
        self.show_record = False
        self.array_dislocation = []
        self.array_cm = []
        self.array_dislocation_ref = []
        self.array_area = []
        self.array_frame_num = []
        self.arrayx = np.array([[]], dtype=np.float32)
        self.array2 = np.array([[]], dtype=np.float32)

        # Mouse Function

    def record_video(self, frame):
        self.record.append(frame)

    def execute(self):
        # cv2.namedWindow("Frame")
        # cv2.setMouseCallback("Frame", self.select_point)                                      # quando se carrega no rato ativa a funçao select_point

        if self.doScale:
            if not self.manualScaleFlag:
                try:
                    self.conversao = self.findScale(self.frame)
                except IndexError:
                    self.manualScaleFlag = True
            elif self.vector_scale.size > 2:
                self.conversao = self.findScaleManually(self.vector_scale)
                self.doScale = False

        if len(self.vector_distance_2points) == 2 and self.flagDistance:  # tem que estar no select_point
            self.flagDistance = False
            self.array_distance_first_frame = self.vector_distance_2points

        if len(self.vector_distance_perpendicular_2points) == 2 and self.flagDistancePerpendicular:
            self.flagDistancePerpendicular = False
            self.array_distance_perpendicular_first_frame = self.vector_distance_perpendicular_2points

        if self.pause:  # este while serve para a primeira imagem ficar parada até o utilizador pressionar ('p') -> util para o utilizador selecionar os pnts

            if self.flag_c == 0:
                 capp =  cv2.VideoCapture(self.video_path)
                 while capp.isOpened():
                     ret, frame = capp.read()
                     if not ret:
                         break
                     self.total_frames += 1
                 self.flag_c = 1


            if len(self.vector_scale) == 2:
                self.manualScaleFlag = False


        elif not self.show_record:

             ### RECORD
            self.show_record = False
            self.record_video(self.frame)


            if not self.stopCountFrames:
                self.num_frames +=1


            check, self.frame = self.cap.read()  # le frame a frame
            self.t += 1

            if check:
                self.frame = self.resize(self.frame)

            if not check:  # entra neste if quando acaba os frames do video, abre-se outra captura para manter em loop

                self.doScale = True
                # self.tmp7 = []
                self.stopDistanceCoordenadasCentroide = True
                self.stopCountFrames = True
                cap1 = cv2.VideoCapture(self.video_path)  # abrir nova captura
                cap1.set(cv2.CAP_PROP_POS_FRAMES, self.set_frame)
                if not cap1.isOpened():
                    #print("Erro")
                    exit()
                _, self.frame = cap1.read()  # le o frame anterior
                self.old_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # converte a frame para gray
                self.old_frame = self.resize(self.old_frame)
                _, self.frame1 = cap1.read()  # le o frame atual
                self.frame1 = self.resize(self.frame1)
                self.gray_frame = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2GRAY)  # converte a frame para gray
                self.cap = cap1  # atualiza as variaveis
                self.frame = self.frame1
                self.old_points = self.origin_points
                self.ref_points
                self.q = 0
                self.q1 = 0
                self.vector_points = np.array([[]],
                                              dtype=np.float32)  # variável que contem os pontos n frames antes, para fazer os vetores
                self.vector_points_ref = np.array([[]],
                                              dtype=np.float32)
                self.t = 0
                self.x = 0
                self.vector_distance_2points = self.array_distance_first_frame
                self.vector_distance_perpendicular_2points = self.array_distance_perpendicular_first_frame
                self.ref_points = self.ref_points_first_frame
                self.flag_hist = 0  # já acabou o ciclo não desenha mais histograma
                self.center = None
                self.centerRef = None
                self.centroideAnterior = None
                self.centroideAnteriorRef = None



            else:
                self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            if self.point_selected is True:  # Uma vez que um ponto é selecionado faz o Tracking
                if self.ref_points.size != 0:  # second contour
                    self.newref_points, self.refstatus, self.referror = cv2.calcOpticalFlowPyrLK(self.old_frame,
                                                                                                 self.gray_frame,
                                                                                                 self.ref_points, None,
                                                                                                 **self.lk_params)
                    self.draw_reference_vectors(self.newref_points, self.vectors_factor)

                    self.ref_points = self.newref_points
                    # draw spline with the new pointscofcof
                    self.Refspline = self.draw_Refspline(self.Refspline, self.newref_points)



                    self.frame = cv2.add(self.frame, self.Refspline)

                    if self.q1 == 0:

                        self.q1 = 1

                if self.old_points.size != 0:  # 1st contour

                    self.new_points, self.status, self.error = cv2.calcOpticalFlowPyrLK(self.old_frame, self.gray_frame,
                                                                                        self.old_points, None,
                                                                                        **self.lk_params)  # tracking Luccas Kanade, Optial flow
                    self.draw_vectors_and_set_histogram(self.new_points,
                                                        self.vectors_factor)  # atualiza as variaveis para o histograma e desenha os vetores


                    self.center = self.centroide(self.new_points)
                    if self.hasRef:
            
                        self.centerRef = self.centroide(self.newref_points)

                        cv2.circle(self.frame, (int(self.centerRef[0]), int(self.centerRef[1])), 2, (255, 255, 0), -1)
                    self.draw_center_vectors(self.vectors_factor)  # fazer o hist

                    self.old_points = self.new_points  # os new points são as coordenadas dos pontos apos a movimentação
                    self.spline = self.draw_spline(self.spline, self.new_points)

                    cv2.circle(self.frame, (int(self.center[0]), int(self.center[1])), 2, (0, 255, 0), -1)


                    if self.flagDistanceCoordenadasCentroide and not self.stopDistanceCoordenadasCentroide and self.hasRef: #para calcular o grafico x,y dos centroides

                        self.distanceBetweenCentroideX = self.centroideAnterior[0] - self.center[0]
                        self.distanceBetweenCentroideX = self.distanceBetweenCentroideX / self.conversao*10
                        self.arraycentroideX.append(round(self.distanceBetweenCentroideX,3))
                        self.distanceBetweenCentroideY = self.centroideAnterior[1] - self.center[1]
                        self.distanceBetweenCentroideY = self.distanceBetweenCentroideY / self.conversao*10
                        self.arraycentroideY.append(round(self.distanceBetweenCentroideY,3))

                        self.distanceBetweenCentroideRefX = self.centroideAnteriorRef[0] - self.centerRef[0]
                        self.distanceBetweenCentroideRefX = self.distanceBetweenCentroideRefX / self.conversao*10
                        self.arraycentroideRefX.append(round(self.distanceBetweenCentroideRefX,3))
                        self.distanceBetweenCentroideRefY = self.centroideAnteriorRef[1] - self.centerRef[1]
                        self.distanceBetweenCentroideRefY = self.distanceBetweenCentroideRefY / self.conversao*10
                        self.arraycentroideRefY.append(round(self.distanceBetweenCentroideRefY,3))


                    self.frame = cv2.add(self.frame, self.spline)  # fazer o overlay do contour na main frame

                    if self.q == 0:  # só faz o resampling 1 vez
                        if self.old_points.size != 0:

                            self.q = 1


                if len(self.vector_distance_2points) == 2:
                    self.distanciaIntroduzida = self.hipote(self.vector_distance_2points[0][0],
                                                            self.vector_distance_2points[0][1],
                                                            self.vector_distance_2points[1][0],
                                                            self.vector_distance_2points[1][1])
                    self.vector_distance_2points = self.trackDistancePoints()
                    self.distanciaMM = self.distanciaIntroduzida / self.conversao  # imprime frame a frame a distancia
                    self.distanciaMM = round((self.distanciaMM) * 10, 3)
                    self.flagDistance = False
                    image = cv2.putText(self.frame, "d1 = " + str(self.distanciaMM) + " mm", self.org, self.font,
                                        self.fontScale, self.color, self.thickness, cv2.LINE_AA)

                if len(self.vector_distance_perpendicular_2points) == 2:
                    self.distanciaIntroduzidaPerpendicular = self.hipote(
                        self.vector_distance_perpendicular_2points[0][0],
                        self.vector_distance_perpendicular_2points[0][1],
                        self.vector_distance_perpendicular_2points[1][0],
                        self.vector_distance_perpendicular_2points[1][1])
                    self.vector_distance_perpendicular_2points = self.trackDistancePointsPerpendicular()
                    self.distanciaMMPerpendicular = self.distanciaIntroduzidaPerpendicular / self.conversao  # imprime frame a frame a distancia
                    self.distanciaMMPerpendicular = round((self.distanciaMMPerpendicular) * 10, 3)
                    self.flagDistancePerpendicular = False
                    image2 = cv2.putText(self.frame, "d2 = " + str(self.distanciaMMPerpendicular) + " mm", self.org2,
                                         self.font, self.fontScale, self.color2, self.thickness, cv2.LINE_AA)

                if self.new_points.size != 0:
                    self.area = self.contourArea(self.new_points)
                    self.area = round((self.area / self.conversao), 3)

                    imageArea = cv2.putText(self.frame, "area = " + str(self.area) + "mm2", self.org3, self.font,
                                            self.fontScale, self.color3, self.thickness, cv2.LINE_AA)

                if self.q == 1:
                    self.area_initial = self.area

                    self.array_dislocation.append(self.arrayx)
                    self.array_cm.append(self.arrayMedidasCentroide)
                    self.array_dislocation_ref.append(self.array2)
                    self.array_area.append(self.area)
                    self.array_frame_num.append(self.num_frames)

                    self.q += 1
                if self.newref_points.size != 0:
                    self.ref_area = self.contourArea(self.newref_points)
                    self.ref_area = round((self.ref_area / self.conversao), 3)

                    imageAreaRef = cv2.putText(self.frame, "area = " + str(self.ref_area) + "mm2", self.org4, self.font,
                                               self.fontScale, self.color4, self.thickness, cv2.LINE_AA)

                if self.t == self.framesPerVector:  # reset de arrays p every 10 frames
                    self.vector_points = self.old_points
                    self.flagDistanceCoordenadasCentroide = True
                    self.centroideAnterior = self.center
                    self.centroideAnteriorRef = self.centerRef
                    self.vector_points_ref = self.ref_points
                    self.calcHistogram()
                    if self.flagRef:
                        self.calcRefHistogram()
                    else: self.array2 = np.array([[]], dtype=np.float32)


                    self.array_dislocation.append(self.arrayx)
                    self.array_cm.append(self.arrayMedidasCentroide)
                    self.array_dislocation_ref.append(self.array2)
                    self.array_area.append(self.area)
                    self.array_frame_num.append(self.num_frames)

                    self.t = 0  # reset da variavel

                self.spline = np.zeros_like(self.spline)  # reset
                self.Refspline = np.zeros_like(self.Refspline)

            self.old_frame = self.gray_frame.copy()  # a frame em que estamos passa a ser a anterior do próximo ciclo


            # comentado p nao estar sp a grvar
            # out.write(frame)    # grava o video depois dos pontos selecionados/ começa a gravar depois de premida a letra 'p' e grava continuadamente até se premida a tecla ESC
            # cv2.imshow("Frame", self.frame)

        self.arrayMedidas = [sum(self.tmp), sum(self.tmp1), sum(self.tmp2), sum(self.tmp3), sum(self.tmp4),
                             sum(self.tmp5), sum(self.tmp6), sum(self.tmp7)]

        self.arrayMedidasCentroide = [sum(self.c_tmp), sum(self.c_tmp1), sum(self.c_tmp2), sum(self.c_tmp3),
                                      sum(self.c_tmp4), sum(self.c_tmp5), sum(self.c_tmp6), sum(self.c_tmp7)]

        self.arrayMedidasReference = [sum(self.r_tmp), sum(self.r_tmp1), sum(self.r_tmp2), sum(self.r_tmp3),
                                      sum(self.r_tmp4), sum(self.r_tmp5), sum(self.r_tmp6), sum(self.r_tmp7)]

        # self.histogram(self.arrayMedidas, self.arrayArrows)


    def showGraph(self):

        self.linegraphic(self.arraycentroideX, self.arraycentroideY, self.arraycentroideRefX, self.arraycentroideRefY)

        plt.show()



    def calcHistogram(self):
        self.arrayMedidas = [sum(self.tmp), sum(self.tmp1), sum(self.tmp2), sum(self.tmp3), sum(self.tmp4),
                             sum(self.tmp5), sum(self.tmp6), sum(self.tmp7)]
        self.arrayx = np.true_divide(self.arrayMedidas, len(self.old_points))

        self.arrayMedidasCentroide = [sum(self.c_tmp), sum(self.c_tmp1), sum(self.c_tmp2), sum(self.c_tmp3),
                                      sum(self.c_tmp4), sum(self.c_tmp5), sum(self.c_tmp6), sum(self.c_tmp7)]

    def showHistogram(self):
        self.histogram(self.arrayx, self.newArrows, self.arrayMedidasCentroide)
        plt.show()

    def calcRefHistogram(self):
        self.arrayMedidasReference = [sum(self.r_tmp), sum(self.r_tmp1), sum(self.r_tmp2), sum(self.r_tmp3),
                                      sum(self.r_tmp4), sum(self.r_tmp5), sum(self.r_tmp6), sum(self.r_tmp7)]
        self.array2 = np.true_divide(self.arrayMedidasReference, len(self.ref_points))

    def showReferenceHistogram(self):

        self.ReferenceHistogram(self.array2)
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

    def ReferenceHistogram(self, array1):
        f1 = plt.figure()
        bars = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        y_pos = np.arange(len(bars))
        ax = f1.add_subplot(1, 1, 1)
        ax.set_xlabel('Cardinal Points')
        plt.tight_layout(pad=2.0)
        # Add title and axis names
        ax.set_ylabel('Moved distance(mm)', labelpad=11)
        histograma = ax.bar(y_pos + 0.1, array1, width=0.4, color='steelblue', align='center', label='Distance(mm)')
        # print("check")
        # print(array2[0])
        # Create names
        ax.set_title('Reference Histogram')
        plt.xticks(y_pos, bars)
        leg = ax.legend();
        plt.subplots_adjust(left=0.17)

        return histograma


    def histogram(self, array1, array2, array3):
        f2 = plt.figure()
        bars = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        y_pos = np.arange(len(bars))
        ax = f2.add_subplot(3, 1, 1)

        plt.tight_layout(pad=2.0)
        # Add title and axis names
        ax.set_ylabel('Moved distance(mm)', labelpad=11)
        histograma = ax.bar(y_pos + 0.1, array1, width=0.4, color='steelblue', align='center', label='Distance(mm)')
        # print("check")
        # print(array2[0])
        # Create names
        plt.xticks(y_pos, bars)
        leg = ax.legend();

        bars1 = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        y_pos1 = np.arange(len(bars))
        ax1 = plt.subplot(3, 1, 2)
        ax1.set_ylabel('Number of vectors(%)')
        histograma1 = ax1.bar(y_pos1 + 0.1, array2, width=0.4, color='darkgray', align='center',
                              label='Number of vectors(%)')
        # print("check")
        # print(array2[0])
        # Create names
        plt.xticks(y_pos1, bars1)
        leg1 = ax1.legend();

        bars2 = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        y_pos2 = np.arange(len(bars))
        ax2 = plt.subplot(3, 1, 3)
        ax2.set_xlabel('Cardinal Points')
        # Add title and axis names

        ax2.set_ylabel('Center of mass(mm)', labelpad=11)
        histograma2 = ax2.bar(y_pos2 + 0.1, array3, width=0.4, color='steelblue', align='center', label='Distance(mm)')
        # print("check")
        # print(array2[0])
        # Create names
        plt.xticks(y_pos2, bars2)
        leg = ax2.legend();
        #print(self.arrayMedidasCentroide)
        plt.subplots_adjust(left=0.17)
        return histograma, histograma1, histograma2


    def linegraphic(self, array1, array2, array3, array4):
        f3 = plt.figure()
        #print("qqqq")
        x = np.linspace(0, self.num_frames, len(array1))
        #print("x")
       #print(x)

        plt.plot(x, array1, label='x1')  # Plot some data on the (implicit) axes.
        plt.plot(x, array2, label='y1')  # etc.
        plt.plot(x, array3, label='xRef')
        plt.plot(x, array4, label='yRef')
        plt.xlabel('Frames')
        plt.ylabel('Distance (mm)')
        plt.title("Center of Mass Movement")
        plt.legend()
        #print("xxxx")

    def hipote(self, x1, y1, x2, y2):  # teorema de pitagoras
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    def direcao(self, x_final, x_inicial, y_final, y_inicial):
        differenceX = x_final - x_inicial
        differenceY = y_final - y_inicial
        graus = math.atan2(differenceX, differenceY) / math.pi * 180
        if graus < 0:
            final_degrees = 360 + graus
        else:
            final_degrees = graus
        cardinal = ["S", "SW", "E", "NE", "N", "NW", "W", "SW", "S"]
        compass_lookup = round(final_degrees / 45)
        return cardinal[compass_lookup]

    def load_file(self, file):  # ver extensao
        number = []
        onlyfiles = [f for f in os.listdir('.') if
                     os.path.isfile(os.path.join('.', f))]  # load todos os files diretorios
        filename, file_extension = os.path.splitext(file)  # load do nome do ficheiro e da extensao
        alll_files = len(onlyfiles)  # obter todos os ficheiros do diretorio
        split = re.compile(r'\d+')  # split do numero do nome do ficheiro
        number = split.findall(filename) or ['0']  # obter o numero do ficheiro
        only_name = filename.replace(number[0], '')  # obter só o nome do ficheiro removendo o numero
        i = 0
        found = [s for s in onlyfiles if
                 only_name in s]  # construir array apenas com nomes de arquivos que correspondem ao only_name (do nome do arquivo)
        if len(found) == 0:  # se nao encontrar nenhum retorna o próprio
            return file
        while i < len(found):  # itera o array dos ficheiros encontrados e retira o numero
            number.append((split.findall(found[i]) or [0])[0])  # adiciona para o array number o numero encontrado
            i += 1
        number = [int(i) for i in number]  # converte todos os numeros do array para int (cast), alguns sao strings
        maxx_number = max(number)  # obtem o valor maximo
        return '{0}{1}{2}'.format(only_name, str(maxx_number + 1), file_extension)

    def add_point(self, x, y):  # à medida que são selecionados pontos estes são adicionados ao array
        global old_points, origin_points
        a_point = np.array([[x, y]], dtype=np.float32)  # formata as coordenadas x,y(float32)
        self.old_points = np.append(a_point, self.old_points, axis=0)  # faz append das coordenadas ao array
        self.origin_points = np.append(a_point, self.origin_points, axis=0)

    def addRef_point(self, x, y):  # à medida que são selecionados pontos estes são adicionados ao array
        global ref_points
        a_point = np.array([[x, y]], dtype=np.float32)  # formata as coordenadas x,y(float32)
        self.ref_points = np.append(a_point, self.ref_points, axis=0)  # faz append das coordenadas ao array
        self.ref_points_first_frame = np.append(a_point, self.ref_points, axis=0)

    def add_point_distance(self, x, y):
        global vector_distance_2points
        a_point_distance = np.array([[x, y]], dtype=np.float32)
        self.vector_distance_2points = np.append(a_point_distance, self.vector_distance_2points,
                                                 axis=0)  # faz append das coordenadas ao array

    def add_point_distance_perpendicular(self, x, y):
        global vector_distance_perpendicular_2points
        a_point_distance = np.array([[x, y]], dtype=np.float32)
        self.vector_distance_perpendicular_2points = np.append(a_point_distance,
                                                               self.vector_distance_perpendicular_2points,
                                                               axis=0)  # faz append das coordenadas ao array

    def add_point_scale_vector(self, x, y):
        global vector_scale
        a_point_scale = np.array([[x, y]], dtype=np.float32)
        self.vector_scale = np.append(a_point_scale, self.vector_scale, axis=0)  # faz append das coordenadas ao array

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

    def findScaleManually(self, vector_scale):
        dist = self.hipote(vector_scale[0][0], vector_scale[0][1], vector_scale[1][0], vector_scale[1][1])
        return dist

    def draw_spline(self, frame_spline, points):

        poly = cv2.approxPolyDP(np.array([points], dtype=np.int32), 1, True)  # aproximação curvilinea do contorno

        contour = cv2.drawContours(frame_spline, [poly], 0, (0, 255, 0), 1)  # desenho do contorno na "frame "contour

        return contour

    def centroide(self, points):
        if points.size > 2:
            mom = cv2.moments(points)
            center = (mom["m10"]/mom["m00"], mom["m01"]/mom["m00"])
        else:
            center = points[0]

        return center




    def draw_Refspline(self, frame_spline, points):



        poly = cv2.approxPolyDP(np.array([points], dtype=np.int32), 1, True)  # aproximação curvilinea do contorno

        contour = cv2.drawContours(frame_spline, [poly], 0, (255, 255, 0), 1)  # desenho do contorno na "frame "contour

        return contour

    def contourArea(self, points):


        sortedp = sorted(points,  # ordenar array em  orientação horária
                         key=lambda coord: (-135 - math.degrees(
                             math.atan2(*tuple(map(operator.sub, coord, self.centroide(points)))[::-1]))) % 360)

        poly = cv2.approxPolyDP(np.array([sortedp], dtype=np.int32), 1, True)  # aproximação curvilinea do contorno
        area = cv2.contourArea(poly)
        # print("Area")
        # print(area)
        return area

    def draw_center_vectors(self, f1):

        i = 0
        if self.old_points.size >= 2 and self.centroideAnterior is not None:

            grad_x, grad_y = self.center[0] - self.centroideAnterior[0], self.center[1] - self.centroideAnterior[1]
            val_x = int(self.center[0] + (f1 * grad_x))  # fator
            val_y = int(self.center[1] + (f1 * grad_y))

            cv2.arrowedLine(self.frame, (int(self.center[0]), int(self.center[1])), (val_x, val_y), (0, 255, 255),
                            1)  # f1 fator de aumento, para melhor visualização, ainda n foi posto

            if self.flag_hist and self.t == self.framesPerVector:  ##fazer o hist
                self.distancePercorridaCentroide = self.hipote(self.centroideAnterior[0], self.centroideAnterior[1],
                                                               # tava num sitio errado, é aqui
                                                               self.center[0], self.center[1])
                self.distancePercorridaCentroide = self.distancePercorridaCentroide / self.conversao
                self.distancePercorridaCentroide = round((self.distancePercorridaCentroide) * 10,
                                                         3)  # distancia percorrida pelo centroide de 6 em 6 frames

                exit = self.direcao(self.center[0], self.centroideAnterior[0], self.center[1],
                                    self.centroideAnterior[
                                        1])  # prints the direction of the cardinal points between two points!!
                # print(exit)
                if exit == self.cardinal_points[
                    0]:  # tamanho pixeis de cada posição 'N' ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                    self.c_tmp.append(self.distancePercorridaCentroide)

                if exit == self.cardinal_points[1]:  # 'NE'
                    # print("test")
                    self.c_tmp1.append(self.distancePercorridaCentroide)

                if exit == self.cardinal_points[2]:  # 'E'
                    self.c_tmp2.append(self.distancePercorridaCentroide)
                    # print(tmp2)
                if exit == self.cardinal_points[3]:  # 'SE'
                    self.c_tmp3.append(self.distancePercorridaCentroide)
                    # print(tmp3)
                if exit == self.cardinal_points[4]:  # 'S'
                    self.c_tmp4.append(self.distancePercorridaCentroide)
                    # print(tmp4)
                if exit == self.cardinal_points[5]:  # 'SW'
                    self.c_tmp5.append(self.distancePercorridaCentroide)
                    # print(tmp5)
                if exit == self.cardinal_points[6]:  # 'W'
                    self.c_tmp6.append(self.distancePercorridaCentroide)
                    # print(tmp6)
                if exit == self.cardinal_points[7]:  # 'NW'
                    self.c_tmp7.append(self.distancePercorridaCentroide)
                    # print(tmp7)

                for cardinal_point in self.cardinal_points:
                    # this assumes exit.count() returns an int
                    self.counts[cardinal_point] += exit.count(
                        cardinal_point)  # counts the number of times North appears

                for cardinal_point, count in self.counts.items():
                    # print(f'{cardinal_point} appears a total of {count} times.')
                    self.arrayArrowsCenter = [i for i in self.counts.values()]

                # tmp.append((hipote(x,y,x+grad_x,y+grad_y)))
                # print(tmp)
            i += 1
            # print(exit.count('N'))
            # print(hipote(x,y,x+grad_x,y+grad_y))   #  shows the distance between these two poin

    def draw_reference_vectors(self,points, f1):
            i = 0

            for x, y in points:
                cv2.circle(self.frame, (x, y), 1, (255, 255,0), -1)

                if self.vector_points_ref.size == points.size:
                    grad_x, grad_y = x - self.vector_points_ref[i][0], y - self.vector_points_ref[i][1]

                    val_x = int(x + (f1 * grad_x))  # fator
                    val_y = int(y + (f1 * grad_y))
                    cv2.arrowedLine(self.frame, (x, y), (val_x, val_y), (0, 255, 255),1)

                    if self.flag_hist == 1 and self.t == self.framesPerVector: #fazer hist
                        tamanho = self.hipote(x, y, x + grad_x, y + grad_y)
                        tamanho = tamanho / self.conversao * 10
                        # print(tamanho)
                        exit = self.direcao(x + grad_x, x, y + grad_y,
                                            y)  # prints the direction of the cardinal points between two points!!
                        # print(exit)
                        if exit == self.cardinal_points[
                            0]:  # tamanho pixeis de cada posição 'N' ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                            self.r_tmp.append(tamanho)

                        if exit == self.cardinal_points[1]:  # 'NE'
                            # print("test")
                            self.r_tmp1.append(tamanho)

                        if exit == self.cardinal_points[2]:  # 'E'
                            self.r_tmp2.append(tamanho)
                            # print(tmp2)
                        if exit == self.cardinal_points[3]:  # 'SE'
                            self.r_tmp3.append(tamanho)
                            # print(tmp3)
                        if exit == self.cardinal_points[4]:  # 'S'
                            self.r_tmp4.append(tamanho)
                            # print(tmp4)
                        if exit == self.cardinal_points[5]:  # 'SW'
                            self.r_tmp5.append(tamanho)
                            # print(tmp5)
                        if exit == self.cardinal_points[6]:  # 'W'
                            self.r_tmp6.append(tamanho)
                            # print(tmp6)
                        if exit == self.cardinal_points[7]:  # 'NW'
                            self.r_tmp7.append(tamanho)
                            # print(tmp7)

                        for cardinal_point in self.cardinal_points:
                            # this assumes exit.count() returns an int
                            self.counts[cardinal_point] += exit.count(
                                cardinal_point)  # counts the number of times North appears

                        for cardinal_point, count in self.counts.items():
                            # print(f'{cardinal_point} appears a total of {count} times.')
                            self.arrayReferenceArrows = [i for i in self.counts.values()]
                            # print(arrayArrows)
                        # tmp.append((hipote(x,y,x+grad_x,y+grad_y)))
                        # print(tmp)
                    i += 1
                    # print(exit.count('N'))
                    # print(hipote(x,y,x+grad_x,y+grad_y))   #  shows the distance between these two points



    def draw_vectors_and_set_histogram(self, points_to_track, f1):
        i = 0
        for x, y in points_to_track:
            cv2.circle(self.frame, (x, y), 1, (0, 255,), -1)
            if self.vector_points.size == points_to_track.size:
                grad_x, grad_y = x - self.vector_points[i][0], y - self.vector_points[i][1]
                val_x = int(x + (f1 * grad_x))  # fator
                val_y = int(y + (f1 * grad_y))
                cv2.arrowedLine(self.frame, (x, y), (val_x, val_y), (0, 255, 255),
                                1)  # f1 fator de aumento, para melhor visualização, ainda n foi posto

                if self.flag_hist == 1 and self.t == self.framesPerVector:  # faz 1 so vez, depois do primeiro ciclo a variavel é atualizada

                    tamanho = self.hipote(x, y, x + grad_x, y + grad_y)
                    tamanho = tamanho / self.conversao * 10
                    # print(tamanho)
                    exit = self.direcao(x + grad_x, x, y + grad_y,
                                        y)  # prints the direction of the cardinal points between two points!!
                    # print(exit)
                    if exit == self.cardinal_points[
                        0]:  # tamanho pixeis de cada posição 'N' ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                        self.tmp.append(tamanho)

                    if exit == self.cardinal_points[1]:  # 'NE'
                        # print("test")
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
                        self.counts[cardinal_point] += exit.count(
                            cardinal_point)  # counts the number of times North appears

                    for cardinal_point, count in self.counts.items():
                        # print(f'{cardinal_point} appears a total of {count} times.')
                        self.arrayArrows = [i for i in self.counts.values()]
                        #print(self.arrayArrows)
                        self.a = sum(self.arrayArrows)
                        self.new = [al / self.a for al in self.arrayArrows]
                        #print(new)
                        self.newArrows = [i * 100 for i in self.new]
                        #print(self.newArrows)

                    # tmp.append((hipote(x,y,x+grad_x,y+grad_y)))
                    # print(tmp)
            i += 1
            # print(exit.count('N'))
            # print(hipote(x,y,x+grad_x,y+grad_y))   #  shows the distance between these two points

    def order_points(self, A):
        # Sort A based on Y(col-2) coordinates
        sortedAc2 = A[np.argsort(A[:, 1]), :]

        # Get top two and bottom two points
        top2 = sortedAc2[0:2, :]
        bottom2 = sortedAc2[2:, :]

        # Sort top2 points to have the first row as the top-left one
        sortedtop2c1 = top2[np.argsort(top2[:, 0]), :]
        top_left = sortedtop2c1[0, :]

        # Use top left point as pivot & calculate sq-euclidean dist against
        # bottom2 points & thus get bottom-right, bottom-left sequentially
        sqdists = distance.cdist(top_left[None], bottom2, 'sqeuclidean')
        rest2 = bottom2[np.argsort(np.max(sqdists, 0))[::-1], :]

        # Concatenate all these points for the final output
        return np.concatenate((sortedtop2c1, rest2), axis=0)

    def format_array(self, track_array):
        f_array = np.array(track_array[0], dtype=np.float32)

        for x in track_array[1:]:
            add = np.array(x, dtype=np.float32)
            f_array = np.append(add, f_array, axis=0)
        return f_array

    def resample_points(self, spline, dif):  # devolve um arrray de pontos ao longo da spline com uma distancia de "dif"

        spline_gray = cv2.cvtColor(spline, cv2.COLOR_BGR2GRAY)  # passar para gray
        mask = cv2.findContours(spline_gray, cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_NONE)  # detetar contorno na imagem do gray frame

        points = np.unique((mask[0][0]), axis=0)  # sem rep
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

    def interp_point(self,points):
        x,y = points[0]
        self.old_points = np.array([[x, y]], dtype=np.float32)
        self.origin_points = np.array([[x, y]], dtype=np.float32)

        for p in range(0,len(points)):

            x1, y1 = self.old_points[0]
            if (p == len(points)-1):
                x2, y2 = points[0]  # para conectar o primeiro com o ultimo
            else:
                x2, y2 = points[p + 1]
            dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
            x0 = x1
            y0 = y1
            if (dist >= self.dif):
                n = int(dist/self.dif)

                for i in range(1, n+1):
                    xi = x0 + (x2 - x1) * self.dif / dist
                    yi = y0 + (y2 - y1) * self.dif / dist
                    self.add_point(xi,yi)
                    x0 = xi
                    y0 = yi

    def interpRef_point(self, points):
        x, y = points[0]
        self.ref_points = np.array([[x, y]], dtype=np.float32)
        self.ref_points_first_frame = np.array([[x, y]], dtype=np.float32)

        for p in range(0, len(points)):
            x1, y1 = self.ref_points[0]
            if (p == len(points) - 1):
                x2, y2 = points[0]  # para conectar o primeiro com o ultimo
            else:
                x2, y2 = points[p + 1]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            x0 = x1
            y0 = y1
            if (dist >= self.dif):
                n = int(dist / self.dif)

                for i in range(1, n + 1):
                    xi = x0 + (x2 - x1) * self.dif / dist
                    yi = y0 + (y2 - y1) * self.dif / dist
                    self.addRef_point(xi, yi)
                    x0 = xi
                    y0 = yi

if __name__ == '__main__':
    code("QUARTA01.wmv").execute()