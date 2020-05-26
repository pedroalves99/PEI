from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import PIL.Image, PIL.ImageTk
from code import code
import cv2
import numpy as np
import excelWriter as ew
from sys import platform

# Default Values
framesPerVector = 6
minDist = 4


class App:
    def __init__(self):
        self.opened = False
        self.window = Tk()
        self.window.title("EcoTracker")
        self.window.geometry("1280x720")        #Fixed window size
        self.window.resizable(False, False)
        self.change = False
        self.frame_num = 0
        self.first_frame = 0

        # TOP LEFT BUTTONS
        self.histogramBt = Button(self.window, text="Histogram", width=10, height=1, command = self.getHistogram).grid(row=0, column=0, pady=2, padx=(10, 250))
        self.referenceHistogram = Button(self.window, text="Reference Histogram", width=15, height=1, command = self.getReferenceHistogram).grid(row=0, column=0, pady=2, padx=(100,50))
        self.CenterOfMass = Button(self.window, text="Center of Mass", width=10, height=1, command=self.getCenterOfMass).grid(row=1, column=0, pady=2, padx=(10, 250), sticky=N)

        # BOTTOM LEFT BUTTONS
        self.evaluationTypeLb = Label(self.window, text="Evaluation Type", font="helvetica 10 bold").grid(row=11, column=0, sticky=W+N, padx=(5,0))
        self.evaluationType = Entry(self.window, width=34)
        self.evaluationType.grid(row=11, column=0, sticky=W+S, padx=(5,0), pady=(0,1))
        self.exportExcelBt = Button(self.window, text="Create Excel", width=10, height=1, command = lambda: self.exportExcel(self.evaluationType.get())).grid(row=12, column=0, padx=(5,0), sticky=W)
        self.addExcelBt = Button(self.window, text="Add to Excel", width=10, height=1, command = lambda: self.addExcel(self.evaluationType.get())).grid(row=12, column=0)

        # VIDEO CANVAS
        self.videoCanvas = Canvas(self.window, width=736, height=552)
        self.videoCanvas.grid(row=0, column=2, columnspan=7, rowspan=10, pady=(15,0), padx=(0,30))
        self.videoCanvas.configure(bg='grey')

        # PLAY BUTTON
        self.playImage = PhotoImage(file="playbutton.png")  
        self.playButton = Button(self.window, width=50, height=50, image=self.playImage, command=self.play)
        self.playButton["border"] = "0"
        self.playButton.grid(row=12, column=5)

        # PAUSE BUTTON
        self.pauseImage = PhotoImage(file="pausebutton.png")  
        self.pauseButton = Button(self.window, width=50, height=50, image=self.pauseImage, command=self.play)
        self.pauseButton["border"] = "0"
        self.pauseButton.grid(row=12, column=5)
        self.pauseButton.grid_remove()

        # TOP RIGHT BUTTONS
        self.openBt = Button(self.window, text="Open", command=self.getFileDir, width=13).grid(row=0, column=10, columnspan=2, padx=10)
        self.saveAsBt = Button(self.window, text="Save As", width=13, command=self.saveFileDir).grid(row=1, column=10, columnspan=2)
        self.resetPointsBt = Button(self.window, text="Reset All", width=13, command=self.delAll).grid(row=2,column=10, columnspan=2)
        self.distance1 = Button(self.window, text="Distance 1", width=13, command=self.distance).grid(row=3, column=10, columnspan=2)
        self.distance2 = Button(self.window, text="Distance 2", width=13, command=self.distancePerpendicular).grid(row=4, column=10, columnspan=2)
        self.secContour = Button(self.window, text="Reference Contour", width=13, command=self.ref)
        self.secContour.grid(row=5, column=10, columnspan=2)        

        # BOTTOM RIGHT BUTTONS
        self.preferencesBt = Button(self.window, text="Preferences", width=13, command=self.optionsWindow).grid(row=7, column=10, columnspan=2)
        self.playbackSpeedLb = Label(self.window, text="Playback Speed", font="helvetica 10 bold").grid(row=8, column=10, columnspan=2)
        self.oneBt = Button(self.window, text="1x", width=3, command = self.getSpeed1x).grid(row=9, column=10, sticky=E, columnspan=2)
        self.seventyFiveBt = Button(self.window, text="0.75x", width=3, command = self.getSpeed075x).grid(row=9, column=10, columnspan=2)
        self.halfBt = Button(self.window, text="0.5x", width=3, command = self.getSpeed05x).grid(row=9, column=10,sticky=W, columnspan=2)
        
        # SCALE BAR
        self.scaleBar = Scale(self.window, from_=0, to=1000, orient=HORIZONTAL, length=650, command=self.onChange)
        self.scaleBar.grid(row=11, column=5, padx=40)
        self.plusBt = Button(self.window, text=">", font="helvetica 10 bold", command = self.increaseFrame).grid(row=11, column=5, sticky=E+S)
        self.minusBt = Button(self.window, text="<", font="helvetica 10 bold", command = self.decreaseFrame).grid(row=11, column=5, sticky=W+S)


        # SCALE BUTTONS 
        self.canvasSizeLb = Label(self.window, text="Video canvas size", font="helvetica 12 bold").grid(row=7, column=0, sticky=W+S, padx=(5,0))
        self.canvasSizeLbTwo = Label(self.window, text="Changing this option will reset the video", font="helvetica 10 bold").grid(row=8, column=0, padx=(5,0), sticky=W+N)
        self.plusSizeBt = Button(self.window, text="+", font="helvetica 10 bold", command=self.incrSize).grid(row=8, column=0, sticky=W+S, padx=(5,0))
        self.minusSizeBt = Button(self.window, text="-", font="helvetica 10 bold", command=self.decrSize).grid(row=8, column=0, padx=100, sticky=W+S)


        self.filename = None
        self.delay = 15
        self.update()

        self.window.mainloop()


    def incrSize(self):
        if self.opened:
            currSize = self.video.scale_percent
            self.video = code(self.filename, framesPerVector, minDist, currSize+1)
            self.videoCanvas.destroy()
            self.videoCanvas = Canvas(self.window, width=self.video.width, height=self.video.height)
            self.videoCanvas.grid(row=0, column=2, columnspan=7, rowspan=10, pady=(15,0))
            self.videoCanvas.configure(bg='grey')
        else:
            mb.showinfo(title="Error!", message="Please open a video first!")

    def decrSize(self):
        if self.opened:
            currSize = self.video.scale_percent
            self.video = code(self.filename, framesPerVector, minDist, currSize-1)
            self.videoCanvas.destroy()
            self.videoCanvas = Canvas(self.window, width=self.video.width, height=self.video.height)
            self.videoCanvas.grid(row=0, column=2, columnspan=7, rowspan=10, pady=(15,0))
            self.videoCanvas.configure(bg='grey')
        else:
            mb.showinfo(title="Error!", message="Please open a video first!")




    def increaseFrame(self):
        self.scaleBar.set(self.scaleBar.get()+1)

    def decreaseFrame(self):
        self.scaleBar.set(self.scaleBar.get()-1)

    def delAll(self):
        self.video = code(self.filename, framesPerVector, minDist)
        self.pauseButton.grid_remove()
        self.playButton.grid()
        self.video.pause = True
        self.scaleBar.set(0)
        self.first_frame = 0
        self.video.record = []
        self.frame_num = 1

    def select_point(self,event):  # Chamada quando se clica no video, registando as coordenadas dos pontos selecionados
        self.video.point_selected = True
        if self.video.doScale:
            if not self.video.manualScaleFlag:
                try:
                    self.video.conversao = self.video.findScale(self.frame)
                except IndexError:
                    self.video.manualScaleFlag = True
            elif self.video.vector_scale.size > 2:
                self.video.conversao = self.video.findScaleManually(self.video.vector_scale)
                self.video.doScale = False

        if not self.video.flagDistance and not self.video.flagDistancePerpendicular and not self.video.flagRef and not self.video.manualScaleFlag:
            if self.video.flag == 1:  # cria os arrays que vão ter as coordenadas dos pontos clicados
                self.click_points = [(event.x,event.y)]
                self.video.flag += 1
            else:
                self.click_points.append((event.x,event.y))
            cv2.circle(self.video.frame, self.click_points[-1], 2, (0, 255, 0), -1)

        if self.video.flagRef and not self.video.flagDistance and not self.video.flagDistancePerpendicular and not self.video.manualScaleFlag:

            self.video.hasRef = True
            if self.video.flagRef == 1:
                self.video.flagRef += 1
                self.click_Refpoints = [(event.x, event.y)]
            else:
              self.click_Refpoints.append((event.x, event.y))

            cv2.circle(self.video.frame, self.click_Refpoints[-1], 2, (255, 255, 0), -1)

        if self.video.flagDistance:

            cv2.circle(self.video.frame, (event.x, event.y), 2, (0, 0, 255),-1)  # sempre que é clicado na imagem, faz um circulo a volta das coord
            if self.video.flag1 == 1:
                self.video.vector_distance_2points = np.array([[event.x, event.y]], dtype=np.float32)  # adiciona os 2 pontos selecionados para calcular a distancia
                self.video.flag1 += 1
            else:
                self.video.add_point_distance(event.x, event.y)

        if self.video.flagDistancePerpendicular:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (255, 0, 255),-1)  # sempre que é clicado na imagem, faz um circulo a volta das coord
            if self.video.flag2 == 1:
                self.video.vector_distance_perpendicular_2points = np.array([[event.x, event.y]], dtype=np.float32)  # adiciona os 2 pontos selecionados para calcular a distancia
                self.video.flag2 += 1
            else:
                self.video.add_point_distance_perpendicular(event.x, event.y)


        if self.video.manualScaleFlag:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (255, 255, 0), -1)
            if self.video.manualScaleFlag == 1:
                self.video.vector_scale = np.array([[event.x, event.y]], dtype=np.float32)
                self.video.manualScaleFlag += 1
            else:
                self.video.add_point_scale_vector(event.x, event.y)

    def delete_point(self, event):
        if not self.video.flagDistance and not self.video.flagDistancePerpendicular and not self.video.flagRef and not self.video.manualScaleFlag:
            cv2.circle(self.video.frame, self.click_points[-1], 2, (0, 0, 0), -1)
            if len(self.click_points) > 1:
                self.click_points = self.click_points[:-1]
                print(self.click_points,":",len(self.click_points))
            else:
                self.click_points.clear()
                print("ollllll",self.click_points)
        if self.video.flagRef and not self.video.flagDistance and not self.video.flagDistancePerpendicular and not self.video.manualScaleFlag:
            if len(self.click_Refpoints)==0:
                self.video.flagRef = False

            else:
                cv2.circle(self.video.frame, self.click_Refpoints[-1], 2, (0, 0, 0), -1)
                if len(self.click_Refpoints) > 1:
                    self.click_Refpoints= self.click_Refpoints[:-1]

                else:
                    self.click_Refpoints.clear()
                    self.video.hasRef = False

        if self.video.flagDistance:
            if self.video.vector_distance_2points != 0:
                x, y = self.video.vector_distance_2points[0]
                cv2.circle(self.video.frame, (x, y), 2, (0, 0, 0), -1)
            self.video.vector_distance_2points = self.video.vector_distance_2points[1:]

        if self.video.flagDistancePerpendicular:
            if self.video.vector_distance_perpendicular_2points != 0:
                x, y = self.video.vector_distance_perpendicular_2points[0]
                cv2.circle(self.video.frame, (x, y), 2, (0, 0, 0), -1)
            self.video.vector_distance__perpendicular_2points = self.video.vector_distance__perpendicular_2points[1:]

    def update(self):  # função que serve de loop, chamada consoante o valor do self.delay em ms
        if(self.opened):
            if(self.video.flagRef):
                self.secContour.config(relief="sunken")
            else:
                self.secContour.config(relief="raised")
        
        if self.filename is not None:  # and self.playing:
            self.frame = cv2.cvtColor(self.video.frame, cv2.COLOR_BGR2RGB)  # Rgb to Bgr
            self.resized = PIL.Image.fromarray(
                self.frame)  # .resize((self.videoCanvas.winfo_width(), self.videoCanvas.winfo_height()))
            self.photo = PIL.ImageTk.PhotoImage(image=self.resized)
            self.canvas_image = self.videoCanvas.create_image(0,0, image=self.photo, anchor=NW)
            self.videoCanvas.bind("<Button 1>", self.select_point)
            self.videoCanvas.bind("<Button 3>", self.delete_point)
            self.scaleBar.config(to=self.video.total_frames)

            if len(self.video.record) <= (self.frame_num - self.first_frame - 1):
                self.video.show_record = False
                
            if not self.change:
                self.video.execute()

            self.change = False

            if not self.video.pause:
                if not self.video.show_record :
                    self.scaleBar.set(self.video.cap.get(cv2.CAP_PROP_POS_FRAMES))
                else:
                    self.scaleBar.set(self.frame_num)
                    if self.frame_num == self.video.total_frames:
                        self.frame_num = self.first_frame
                    else:
                        self.frame_num += 1


            if self.video.manualScaleFlag and not self.video.okClicked:
                mb.showinfo(title="Error!", message="Mark scale manually on 1cm!")
                self.video.okClicked = True

        self.window.after(self.delay, self.update)

    def getFileDir(self):
        self.filename = fd.askopenfilename(filetypes=[("Video files", ".avi .wmv .mp4")])
        self.video = code(self.filename, framesPerVector, minDist)
        self.videoCanvas.destroy()      #destroi o canvas que estava e mete um com o size proporcional ao video

        self.videoCanvas = Canvas(self.window, width=self.video.width, height=self.video.height)
        self.videoCanvas.grid(row=0, column=2, columnspan=7, rowspan=10, pady=(15,0))
        self.videoCanvas.configure(bg='grey')
        self.filenameLb = Label(self.window, text=self.filename, font="helvetica 9 bold").grid(row=15, column=0, columnspan=30, sticky=W+S, padx=5)
        self.opened = True


    def getSpeed1x(self):
        self.delay = 15

    def getSpeed075x(self):
        self.delay = 23

    def getSpeed05x(self):
        self.delay = 30

    def getHistogram(self):
        self.video.calcHistogram()
        self.video.showHistogram()

    def getReferenceHistogram(self):
        self.video.calcRefHistogram()
        self.video.showReferenceHistogram()

    def getCenterOfMass(self):
        self.video.showGraph()
        #print("aqui")

    def exportExcel(self, evaluationType):
        if len(evaluationType) != 0 and evaluationType != "Evaluation Type":
            filename = fd.asksaveasfilename()
            if(filename[-5:] != ".xlsx" or filename[-4:] != ".xls"):
                filename = filename+".xlsx"

                self.video.calcHistogram()
                if self.video.flagRef:
                    self.video.calcRefHistogram()
                else:
                    #print("not ref")
                    self.video.array2 = []

                ew.create_excel(filename)
                ew.add_data(filename, self.filename, evaluationType, self.video.arrayx, self.video.arrayMedidasCentroide, self.video.array2, self.video.area_initial, self.video.area, 0, 0)
            if self.opened:
                mb.showinfo(title="Done!", message="Exported successfully!")
            else:
                mb.showinfo(title="Error!", message="Please open a video first!")
        else:
            mb.showinfo(title="Done!", message="Please fill in the evaluation Type!")
        
        
       

    def addExcel(self, evaluationType):
        if len(evaluationType) != 0 and evaluationType != "Evaluation Type":
            # FAZER AS COISAS AQUI
            filename = fd.askopenfilename(filetypes=[("Excel sheet", ".xls .xlsx")])
            self.video.calcHistogram()
            if self.video.flagRef:
                self.video.calcRefHistogram()
            ew.add_data(filename, self.filename, evaluationType, self.video.arrayx, self.video.arrayMedidasCentroide,self.video.array2, self.video.area_initial, self.video.area, 0, 0)
            mb.showinfo(title="Done!", message="Exported successfully!")
        else:
            mb.showinfo(title="Done!", message="Please fill in the evaluation Type!")
        

    def saveFileDir(self, evaluationType):
        filename = fd.asksaveasfilename()
        if self.opened:
            mb.showinfo(title="Done!", message="Saved successfully!")
        else:
            mb.showinfo(title="Error!", message="Please open a video first!")

    def distance(self):
        self.video.flagDistance = True
        #print("flag distance")
        #print(self.video.flagDistance)

    def distancePerpendicular(self):
        self.video.flagDistancePerpendicular = True
        #print("flag distance perpendicular")
        #print(self.video.flagDistancePerpendicular)

    def ref(self):
        if self.video.flagRef:
            self.video.flagRef = False
        else:
            self.video.flagRef = True


    def optionsWindow(self):
        optionsWindow = Toplevel()
        optionsWindow.title("Preferences")
        optionsWindow.geometry("400x140+300+150")
        optionsWindow.resizable(0, 0)  # Removes maximize button
        optionsWindow.attributes('-topmost', 'true')  # Always on top

        minDistL = Label(optionsWindow, text="Distance between resampling points", font="helvetica 10 bold").grid(row=1, column=1,columnspan=3,sticky=W, pady=(20,20),padx=(15,0))
        minDistEntry = Entry(optionsWindow)
        minDistEntry.delete(0, END)
        minDistEntry.insert(0, minDist)
        minDistEntry.grid(row=1, column=4)

        nfv = Label(optionsWindow, text="Number of frames per vector", font="helvetica 10 bold").grid(row=2, column=1,columnspan=3,sticky=W, padx=(15, 0))
        nfvEntry = Entry(optionsWindow, text=framesPerVector)
        nfvEntry.delete(0, END)
        nfvEntry.insert(0, framesPerVector)
        nfvEntry.grid(row=2, column=4)

        # Resets changes to default values
        resetBt = Button(optionsWindow, text="Reset", width=10, height=1,
                         command=lambda: self.insertVal(nfvEntry, minDistEntry)).grid(row=3, column=2, padx=(20, 5), pady=(15, 0))

        # Closes window, discards changes
        discardBt = Button(optionsWindow, text="Discard", width=10, height=1, command=lambda: optionsWindow.destroy()).grid(row=3, column=3, padx=(28, 0), pady=(15, 0))

        # Closes window, saves values
        confirmBt = Button(optionsWindow, text="Confirm", width=10, height=1, command=lambda: self.saveValues(nfvEntry, minDistEntry, optionsWindow)).grid(row=3, column=4,padx=(5, 0),pady=(15, 0))

    def insertVal(self, nfvEntry, minDistEntry):
        nfvEntry.delete(0, END)
        nfvEntry.insert(0, 6)
        minDistEntry.delete(0, END)
        minDistEntry.insert(0, 4)

    def saveValues(self, nfvEntry, minDistEntry, optionsWindow):
        global framesPerVector, minDist
        framesPerVector = nfvEntry.get()
        minDist = minDistEntry.get()
        optionsWindow.destroy()

    def play(self):
        if self.video.pause:  # usar a variavel do code.py
            self.playButton.grid_remove()
            self.pauseButton.grid()
            self.video.pause = False

            if len(self.click_points) > 0 and self.video.q == 0:
                self.video.interp_point(self.click_points)

            if self.video.hasRef and self.video.q1 == 0:
                self.video.interpRef_point(self.click_Refpoints)
        else:
            self.pauseButton.grid_remove()
            self.playButton.grid()
            self.video.pause = True

    def onChange(self, frame_num):

        #print("tamanho array" +str(len(self.video.record)))
        #print(frame_num)
        frame_num = int(frame_num)
        self.frame_num = frame_num

        if len(self.video.record)  > (frame_num - self.first_frame - 1) and len(self.video.record) != 0:

            self.video.show_record = True
            self.change = True
            self.video.old_frame = self.video.record[frame_num - self.first_frame - 1]
            self.video.frame = self.video.old_frame
            self.video.old_frame = cv2.cvtColor(self.video.old_frame, cv2.COLOR_BGR2GRAY)

        elif self.opened and self.video.pause and self.video.cap.get(cv2.CAP_PROP_POS_FRAMES) != frame_num:

            self.video.set_frame = frame_num
            self.change = True
            print("change")
            pass
            # if self.video.pause:
            self.video.cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_num))
            self.first_frame = frame_num
            __, self.video.old_frame = self.video.cap.read()

            self.video.old_frame = self.video.resize(self.video.old_frame)

            self.video.frame = self.video.old_frame
            self.video.old_frame = cv2.cvtColor(self.video.old_frame,cv2.COLOR_BGR2GRAY)  # passa a primeira frame para grayScale
            # else:
            # pass
            # print("not in pause")
            # self.video.cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_num))
            # __, self.video.frame1 = self.video.cap.read()
            #
            # self.video.frame1 = self.video.resize(self.video.frame1)
        # else:
        #     self.scaleBar.set(0)
if __name__ == '__main__':
    App()