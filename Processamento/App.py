from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import PIL.Image, PIL.ImageTk
from code import code
import cv2
import numpy as np
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
        
        # Para fullscreen, primeiro se for windows, depois se for linux
        #if platform == "win32":
        #    self.window.wm_state("zoomed")
        #else:
        #    self.window.attributes("-zoomed", True)


        # TOP LEFT BUTTONS
        self.histogramBt = Button(self.window, text="Histogram", width=10, height=1, command = self.getHistogram).grid(row=0, column=0, pady=2, padx=(5, 300))


        # BOTTOM LEFT BUTTONS
        self.evaluationTypeLb = Label(self.window, text="Evaluation Type", font="helvetica 10 bold").grid(row=11, column=0, sticky=W+N, padx=(5,0))
        self.evaluationType = Entry(self.window, width=34)
        self.evaluationType.grid(row=11, column=0, sticky=W+S, padx=(5,0), pady=(0,1))
        self.exportExcelBt = Button(self.window, text="Create Excel", width=10, height=1, command = lambda: self.exportExcel(self.evaluationType.get())).grid(row=12, column=0, padx=(5,0), sticky=W)
        self.addExcelBt = Button(self.window, text="Add to Excel", width=10, height=1, command = lambda: self.addExcel(self.evaluationType.get())).grid(row=12, column=0)


        # VIDEO CANVAS
        self.videoCanvas = Canvas(self.window, width=736, height=552)
        self.videoCanvas.grid(row=0, column=2, columnspan=7, rowspan=10)
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
        self.secContour = Button(self.window, text="Reference Contour", width=13, command=self.ref).grid(row=5, column=10, columnspan=2)

        # BOTTOM RIGHT BUTTONS
        self.preferencesBt = Button(self.window, text="Preferences", width=13, command=self.optionsWindow).grid(row=7, column=10, columnspan=2)
        self.playbackSpeedLb = Label(self.window, text="Playback Speed", font="helvetica 10 bold").grid(row=8, column=10, columnspan=2)
        self.oneBt = Button(self.window, text="1x", width=3, command = self.getSpeed1x).grid(row=9, column=10, sticky=E, columnspan=2)
        self.seventyFiveBt = Button(self.window, text="0.75x", width=3, command = self.getSpeed075x).grid(row=9, column=10, columnspan=2)
        self.halfBt = Button(self.window, text="0.5x", width=3, command = self.getSpeed05x).grid(row=9, column=10,sticky=W, columnspan=2)
        
        # SCALE BAR
        self.scaleBar = Scale(self.window, from_=0, to=1000, orient=HORIZONTAL, length=735)
        self.scaleBar.grid(row=11, column=5)

        self.filename = None
        self.delay = 15
        self.update()

        self.window.mainloop()

    def delAll(self):
        self.video = code(self.filename, framesPerVector, minDist)
        self.pauseButton.grid_remove()
        self.playButton.grid()
        self.video.pause = True

    def select_point(self,event):  # Chamada quando se clica no video, registando as coordenadas dos pontos selecionados
        self.video.point_selected = True
        print("flagDistance")
        print(self.video.flagDistance)
        if not self.video.flagDistance and not self.video.flagDistancePerpendicular and not self.video.flagRef and not self.video.manualScaleFlag:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (0, 255, 0),
                       -1)  # sempre que é clicado na imagem, faz um circulo a volta das coord

            if self.video.flag == 1:  # cria os arrays que vão ter as coordenadas dos pontos clicados
                self.video.old_points = np.array([[event.x, event.y]], dtype=np.float32)  # array que vai ter as coordenadas dos pontos conforme o movimento
                self.video.origin_points = np.array([[event.x, event.y]], dtype=np.float32)  # array que apenas vai conter as coordenadas dos pontos selecionados no inicio(útil para o loop)
                self.video.flag += 1
            else:
                self.video.add_point(event.x, event.y)

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
        if self.video.flagRef and not self.video.flagDistance and not self.video.flagDistancePerpendicular and not self.video.manualScaleFlag:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (255, 255, 0), -1)
            if self.video.flagRef == 1:
                self.video.ref_points = np.array([[event.x, event.y]], dtype=np.float32)
                self.video.ref_points_first_frame = np.array([[]], dtype=np.float32)
                self.video.flagRef += 1
            else:
                self.video.addRef_point(event.x, event.y)

        if self.video.manualScaleFlag:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (255, 255, 0), -1)
            if self.video.manualScaleFlag == 1:
                self.video.vector_scale = np.array([[event.x, event.y]], dtype=np.float32)
                self.video.manualScaleFlag += 1
            else:
                self.video.add_point_scale_vector(event.x, event.y)


    def update(self):  # função que serve de loop, chamada consoante o valor do self.delay em ms
        if self.filename is not None:  # and self.playing:
            self.frame = cv2.cvtColor(self.video.frame, cv2.COLOR_BGR2RGB)  # Rgb to Bgr
            self.resized = PIL.Image.fromarray(
                self.frame)  # .resize((self.videoCanvas.winfo_width(), self.videoCanvas.winfo_height()))
            self.photo = PIL.ImageTk.PhotoImage(image=self.resized)
            self.canvas_image = self.videoCanvas.create_image(0,0, image=self.photo, anchor=NW)
            self.videoCanvas.bind("<Button 1>", self.select_point)
            self.video.execute()

            print("flagScale")
            print(self.video.manualScaleFlag)

            if self.video.manualScaleFlag and not self.video.okClicked:
                mb.showinfo(title="Error!", message="Mark scale manually on 1cm!")
                self.video.okClicked = True

        self.window.after(self.delay, self.update)

    def getFileDir(self):
        self.filename = fd.askopenfilename(filetypes=[("Video files", ".avi .wmv .mp4")])
        self.video = code(self.filename, framesPerVector, minDist)
        self.videoCanvas.destroy()      #destroi o canvas que estava e mete um com o size proporcional ao video

        self.videoCanvas = Canvas(self.window, width=self.video.width, height=self.video.height)
        self.videoCanvas.grid(row=0, column=2, columnspan=7, rowspan=10)
        self.videoCanvas.configure(bg='grey')
        self.filenameLb = Label(self.window, text=self.filename, font="helvetica 9 bold").grid(row=14, column=0, sticky=W, padx=5)
        self.opened = True


    def getSpeed1x(self):
        self.delay = 15

    def getSpeed075x(self):
        self.delay = 23

    def getSpeed05x(self):
        self.delay = 30

    def getHistogram(self):
        code.showHistogram(self.video)

    def exportExcel(self, evaluationType):
        if len(evaluationType) != 0 and evaluationType != "Evaluation Type":
            filename = fd.asksaveasfilename()
            if(filename[-5:] != ".xlsx" or filename[-4:] != ".xls"):
                filename = filename+".xlsx"
            if self.opened:
                mb.showinfo(title="Done!", message="Exported successfully!")
            else:
                mb.showinfo(title="Error!", message="Please open a video first!")
        else:
            mb.showinfo(title="Done!", message="Please fill in the evaluation Type!")
        
        
       

    def addExcel(self, evaluationType):
        if len(evaluationType) != 0 and evaluationType != "Evaluation Type":
            # FAZER AS COISAS AQUI
            self.filename = fd.askopenfilename(filetypes=[("Excel sheet", ".xls .xlsx")])
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
        print("flag distance")
        print(self.video.flagDistance)

    def distancePerpendicular(self):
        self.video.flagDistancePerpendicular = True
        print("flag distance perpendicular")
        print(self.video.flagDistancePerpendicular)

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
        else:
            self.pauseButton.grid_remove()
            self.playButton.grid()
            self.video.pause = True


if __name__ == '__main__':
    App()