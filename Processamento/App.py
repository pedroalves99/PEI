from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import PIL.Image, PIL.ImageTk
from code import code
import cv2
import numpy as np


#Default Values
framesPerVector = 6
minDist = 4
class App:

    def __init__(self):
        self.window = Tk()
        self.window.title("EcoTracker")
        self.screenWidth = self.window.winfo_screenwidth()
        self.screenHeight = self.window.winfo_screenheight()
        self.window.attributes("-zoomed", True)         # UNCOMMENT FOR LINUX
        #self.window.wm_state("zoomed")                 # UNCOMMENT FOR WINDOWS
        print(int(self.screenWidth/1000))

        # TOP LEFT BUTTONS
        self.histogramBt = Button(self.window, text="Histogram", width=int(self.screenWidth/190), height=int(self.screenHeight/384)).grid(row=1, column=1, padx=(0, self.screenWidth/4.1))

        # VIDEO CANVAS
        self.videoCanvas = Canvas(self.window, width = self.screenWidth/1.7, height = self.screenHeight/1.15)
        self.videoCanvas.grid(row=1, column=3, rowspan=10, padx=self.screenWidth/128, pady=(self.screenWidth/192,0))
        self.videoCanvas.configure(bg='grey')
    
        # PLAY BUTTON
        self.playImage = PhotoImage(file="playbutton.png")  
        self.playButton = Button(self.window, width=int(self.screenWidth/30), height=int(self.screenWidth/30), image=self.playImage, command=self.play)
        self.playButton["border"] = "0"
        self.playButton.grid(row=11, column=3)

        # PAUSE BUTTON
        self.pauseImage = PhotoImage(file="pausebutton.png")  
        self.pauseButton = Button(self.window, width=int(self.screenWidth/30), height=int(self.screenWidth/30), image=self.pauseImage, command=self.play)
        self.pauseButton["border"] = "0"
        self.pauseButton.grid(row=11, column=3)
        self.pauseButton.grid_remove()

        # TOP RIGHT BUTTONS
        self.openBt = Button(self.window, text="Open", width=int(self.screenWidth/100), command=self.getFileDir).grid(row=1, column=5, columnspan=2)
        self.saveAsBt = Button(self.window, text="Save As", width=int(self.screenWidth/100), command=self.saveFileDir).grid(row=2, column=5, columnspan=2)
        self.resetPointsBt = Button(self.window, text="Reset Points", width=int(self.screenWidth/100)).grid(row=3, column=5, columnspan=2)
        self.distance1 = Button(self.window, text="Distance1", width=int(self.screenWidth/100), command=self.distance).grid(row=4, column=5, columnspan=2)
        self.distance2 = Button(self.window, text="Distance2", width=int(self.screenWidth/100), command=self.distancePerpendicular).grid(row=5, column=5, columnspan=2)

        # BOTTOM RIGHT BUTTONS
        self.preferencesBt = Button(self.window, text="Preferences", width=int(self.screenWidth/100), command=self.optionsWindow).grid(row=7, column=5, pady=(self.screenWidth/6.4,self.screenHeight/192))
        self.playbackSpeedLb = Label(self.window, text="Playback Speed", font="helvetica 10 bold").grid(row=8, column=5, pady=0)
        self.oneBt = Button(self.window, text="1x", width=int(self.screenWidth/1000)).grid(row=9, column=5, sticky=E)
        self.seventyFiveBt = Button(self.window, text="0.75x", width=int(self.screenWidth/1000)).grid(row=9, column=5)
        self.halfBt = Button(self.window, text="0.5x", width=int(self.screenWidth/1000)).grid(row=9, column=5, sticky=W)
        self.filename = None

        self.delay = 15
        self.update()

        self.window.mainloop()

    def select_point(self, event):  # Chamada quando se clica no video, registando as coordenadas dos pontos selecionados

        self.video.point_selected = True
        print("flagDistance")
        print(self.video.flagDistance)
        if not self.video.flagDistance and not self.video.flagDistancePerpendicular:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (0, 255, 0),
                       -1)  # sempre que é clicado na imagem, faz um circulo a volta das coord

            if self.video.flag == 1:  # cria os arrays que vão ter as coordenadas dos pontos clicados
                self.video.old_points = np.array([[event.x, event.y]],
                                           dtype=np.float32)  # array que vai ter as coordenadas dos pontos conforme o movimento
                self.video.origin_points = np.array([[event.x, event.y]],
                                              dtype=np.float32)  # array que apenas vai conter as coordenadas dos pontos selecionados no inicio(útil para o loop)
                self.video.flag += 1
            else:
                self.video.add_point(event.x, event.y)

        if self.video.flagDistance:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (0, 0, 255),
                       -1)  # sempre que é clicado na imagem, faz um circulo a volta das coord
            if self.video.flag1 == 1:
                self.video.vector_distance_2points = np.array([[event.x, event.y]],
                                                        dtype=np.float32)  # adiciona os 2 pontos selecionados para calcular a distancia
                self.video.flag1 += 1
            else:
                self.video.add_point_distance(event.x, event.y)

        if self.video.flagDistancePerpendicular:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (255, 0, 255),
                       -1)  # sempre que é clicado na imagem, faz um circulo a volta das coord
            if self.video.flag2 == 1:
                self.video.vector_distance_perpendicular_2points = np.array([[event.x, event.y]],
                                                              dtype=np.float32)  # adiciona os 2 pontos selecionados para calcular a distancia
                self.video.flag2 += 1
            else:
                self.video.add_point_distance_perpendicular(event.x, event.y)


    def update(self):                                                           #função que serve de loop, chamada consoante o valor do self.delay em ms

        if self.filename is not None:   # and self.playing:
            self.frame = cv2.cvtColor(self.video.frame, cv2.COLOR_BGR2RGB)#Rgb to Bgr
            self.resized = PIL.Image.fromarray(self.frame)  #.resize((self.videoCanvas.winfo_width(), self.videoCanvas.winfo_height()))
            self.photo = PIL.ImageTk.PhotoImage(image=self.resized)
            self.videoCanvas.create_image(0, 0, image=self.photo, anchor=NW)
            self.video.execute()
            self.videoCanvas.bind("<Button 1>", self.select_point)

        self.window.after(self.delay, self.update)

    def getFileDir(self):
        self.filename = fd.askopenfilename(filetypes=[("Video files",".avi .wmv .mp4")])
        self.video = code(self.filename, framesPerVector, minDist)



    def saveFileDir(self):

        filename = fd.asksaveasfilename()
        mb.showinfo(title="Done!", message="Saved successfully!")
        # save com o code.py

    def distance(self):
        self.video.flagDistance = True
        print("flag distance")
        print(self.video.flagDistance)

    def distancePerpendicular(self):
        self.video.flagDistancePerpendicular = True
        print("flag distance perpendicular")
        print(self.video.flagDistancePerpendicular)

    def optionsWindow(self):
        optionsWindow = Toplevel()
        optionsWindow.title("Preferences")
        optionsWindow.geometry("400x140+300+150")
        optionsWindow.resizable(0,0)        # Removes maximize button
        optionsWindow.attributes('-topmost', 'true')    # Always on top


        minDistL = Label(optionsWindow, text="Distance between resampling points", font="helvetica 10 bold").grid(row=1, column=1, columnspan=3, sticky=W, pady=(20,20), padx=(15,0))
        minDistEntry = Entry(optionsWindow)
        minDistEntry.delete(0, END)
        minDistEntry.insert(0, minDist)
        minDistEntry.grid(row=1, column=4)

        nfv = Label(optionsWindow, text="Number of frames per vector", font="helvetica 10 bold").grid(row=2, column=1, columnspan=3, sticky=W, padx=(15,0))
        nfvEntry = Entry(optionsWindow, text=framesPerVector)
        nfvEntry.delete(0, END)
        nfvEntry.insert(0, framesPerVector)
        nfvEntry.grid(row=2, column=4)



        # Resets changes to default values
        resetBt = Button(optionsWindow, text="Reset", width=10, height=1, command= lambda: self.insertVal(nfvEntry, minDistEntry)).grid(row=3, column=2, padx=(20,5), pady=(15,0))

        # Closes window, discards changes
        discardBt = Button(optionsWindow, text="Discard", width=10, height=1, command= lambda: optionsWindow.destroy()).grid(row=3, column=3, padx=(28,0), pady=(15,0))

        # Closes window, saves values
        confirmBt = Button(optionsWindow, text="Confirm", width=10, height=1, command= lambda: self.saveValues(nfvEntry, minDistEntry, optionsWindow)).grid(row=3, column=4, padx=(5,0), pady=(15,0))


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
        if self.video.pause:                    # usar a variavel do code.py
            self.playButton.grid_remove()
            self.pauseButton.grid()
            self.video.pause = False
        else:
            self.pauseButton.grid_remove()
            self.playButton.grid()
            self.video.pause = True


if __name__ == '__main__':
    App()