from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from code import code

#Default Values
framesPerVector = 6
minDist = 4

def main():

    window = Tk()
    window.title("EcoTracker")

    window.attributes("-zoomed", True)         # UNCOMMENT FOR LINUX
    #window.wm_state("zoomed")                 # UNCOMMENT FOR WINDOWS

    # POSIÇÕES ADAPTADAS AO ECRÃ DO CASAS
    # TOP LEFT BUTTONS
    histogramBt = Button(window, text="Histogram", width=10, height=2).grid(row=1, column=1)
    compassRoseBt = Button(window, text="Compass Rose", width=10, height=2).grid(row=1, column=2)

    # VIDEO CANVAS
    videoCanvas = Canvas(window, width=1000, height=700)
    videoCanvas.grid(row=1, column=3, rowspan=10, padx=15, pady=10)
    videoCanvas.configure(bg='grey')


    # TOP RIGHT BUTTONS
    openBt = Button(window, text="Open", width=10, command=getFileDir).grid(row=1, column=5, columnspan=2)
    saveAsBt = Button(window, text="Save As", width=10, command=saveFileDir).grid(row=2, column=5, columnspan=2)
    resetPointsBt = Button(window, text="Reset Points", width=10).grid(row=3, column=5, columnspan=2)
    
    # BOTTOM RIGHT BUTTONS
    preferencesBt = Button(window, text="Preferences", width=10, command=optionsWindow).grid(row=10, column=5, pady=(400,10))
    playbackSpeedLb = Label(window, text="Playback Speed", font="helvetica 10 bold").grid(row=11, column=5)
    oneBt = Button(window, text="1x", width=1).grid(row=12, column=5, sticky=E)
    seventyFiveBt = Button(window, text="0.75x", width=1).grid(row=12, column=5)
    halfBt = Button(window, text="0.5x", width=1).grid(row=12, column=5, sticky=W)

    window.mainloop()




def getFileDir():
    filename = fd.askopenfilename(filetypes=[("Video files",".avi .wmv .mp4")])
    code(filename, framesPerVector, minDist).execute()


def saveFileDir():
    global filename
    filename = fd.asksaveasfilename()  
    mb.showinfo(title="Done!", message="Saved successfully!") 
    # save com o code.py


def optionsWindow():
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
    resetBt = Button(optionsWindow, text="Reset", width=10, height=1, command= lambda: insertVal(nfvEntry, minDistEntry)).grid(row=3, column=2, padx=(20,5), pady=(15,0))

    # Closes window, discards changes
    discardBt = Button(optionsWindow, text="Discard", width=10, height=1, command= lambda: optionsWindow.destroy()).grid(row=3, column=3, padx=(28,0), pady=(15,0))
    
    # Closes window, saves values
    confirmBt = Button(optionsWindow, text="Confirm", width=10, height=1, command= lambda: saveValues(nfvEntry, minDistEntry, optionsWindow)).grid(row=3, column=4, padx=(5,0), pady=(15,0))


def insertVal(nfvEntry, minDistEntry):
    nfvEntry.delete(0, END)
    nfvEntry.insert(0, 6)
    minDistEntry.delete(0, END)
    minDistEntry.insert(0, 4)

def saveValues(nfvEntry, minDistEntry, optionsWindow):
    global framesPerVector, minDist
    framesPerVector = nfvEntry.get()
    minDist = minDistEntry.get()
    optionsWindow.destroy()

if __name__ == '__main__':
    main()