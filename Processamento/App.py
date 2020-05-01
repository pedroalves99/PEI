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

        #window.attributes("-zoomed", True)         # UNCOMMENT FOR LINUX
        self.window.wm_state("zoomed")                 # UNCOMMENT FOR WINDOWS

        # POSIÇÕES ADAPTADAS AO ECRÃ DO CASAS
        # TOP LEFT BUTTONS
        self.histogramBt = Button(self.window, text="Histogram", width=10, height=2).grid(row=1, column=1)
        self.compassRoseBt = Button(self.window, text="Compass Rose", width=10, height=2).grid(row=1, column=2)

        # VIDEO CANVAS
        self.videoCanvas = Canvas(self.window, width = 1000, height = 700)
        self.videoCanvas.grid(row=1, column=3, rowspan=10, padx=15, pady=10)
        self.videoCanvas.configure(bg='grey')


        # TOP RIGHT BUTTONS
        self.openBt = Button(self.window, text="Open", width=10, command=self.getFileDir).grid(row=1, column=5, columnspan=2)
        self.saveAsBt = Button(self.window, text="Save As", width=10, command=self.saveFileDir).grid(row=2, column=5, columnspan=2)
        self.resetPointsBt = Button(self.window, text="Reset Points", width=10).grid(row=3, column=5, columnspan=2)

        # BOTTOM RIGHT BUTTONS
        self.preferencesBt = Button(self.window, text="Preferences", width=10, command=self.optionsWindow).grid(row=10, column=5, pady=(400,10))
        self.playbackSpeedLb = Label(self.window, text="Playback Speed", font="helvetica 10 bold").grid(row=11, column=5)
        self.oneBt = Button(self.window, text="1x", width=1).grid(row=12, column=5, sticky=E)
        self.seventyFiveBt = Button(self.window, text="0.75x", width=1).grid(row=12, column=5)
        self.halfBt = Button(self.window, text="0.5x", width=1).grid(row=12, column=5, sticky=W)
        self.filename = None

        self.delay = 15
        self.update()

        self.window.mainloop()

    def select_point(self, event):  # Chamada quando se clica no video, registando as coordenadas dos pontos selecionados

        self.video.point_selected = True
        print("flagDistance")
        print(self.video.flagDistance)
        if not self.video.flagDistance:
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

        else:
            cv2.circle(self.video.frame, (event.x, event.y), 2, (0, 0, 255),
                       -1)  # sempre que é clicado na imagem, faz um circulo a volta das coord
            if self.video.flag1 == 1:
                self.video.vector_distance_2points = np.array([[event.x, event.y]],
                                                        dtype=np.float32)  # adiciona os 2 pontos selecionados para calcular a distancia
                self.video.flag1 += 1
            else:
                self.video.add_point_distance(event.x, event.y)

    def update(self):                                                           #função que serve de loop, chamada consoante o valor do self.delay em ms

        if self.filename is not None:
            self.frame = cv2.cvtColor(self.video.frame, cv2.COLOR_BGR2RGB)#Rgb to Bgr
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
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

if __name__ == '__main__':
    App()