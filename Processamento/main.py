from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb


#testing purpouses, replace by actual values later
framesPerVector = 100
trackingPoints = 200


def getFileDir():
    filename = fd.askopenfilename(filetypes=[("Video files",".avi .wmv .mp4")])
    # começar tracking

def saveFileDir():
    global filename
    filename = fd.asksaveasfilename()  
    mb.showinfo(title="Done!", message="Saved successfully!") 
    # save com o code.py

def saveFile():
    global filename
    try:
        filename
    except NameError:
        mb.showerror(title="Error Saving", message="Please 'Save As' before saving")
    else:
        mb.showinfo(title="Done!", message="Saved successfully!")

    # save com o code.py

def optionsWindow():
    optionsWindow = Toplevel()
    optionsWindow.title("Preferences")
    optionsWindow.geometry("400x140+300+150")
    optionsWindow.resizable(0,0)        # Removes maximize button
    optionsWindow.attributes('-topmost', 'true')    # Always on top


    ntp = Label(optionsWindow, text="Number of tracking points", font="helvetica 11 bold").grid(row=1, column=1, columnspan=3, sticky=W, pady=(20,20), padx=(15,0))
    ntpEntry = Entry(optionsWindow)
    ntpEntry.delete(0, END)
    ntpEntry.insert(0, trackingPoints)
    ntpEntry.grid(row=1, column=4)
    
    nfv = Label(optionsWindow, text="Number of frames per vector", font="helvetica 11 bold").grid(row=2, column=1, columnspan=3, sticky=W, padx=(15,0))
    nfvEntry = Entry(optionsWindow, text=framesPerVector)
    nfvEntry.delete(0, END)
    nfvEntry.insert(0, framesPerVector)
    nfvEntry.grid(row=2, column=4)


    
    # Resets changes to default values
    resetBt = Button(optionsWindow, text="Reset", width=10, height=1, command= lambda: insertVal(nfvEntry, ntpEntry)).grid(row=3, column=2, padx=(20,5), pady=(15,0))

    # Closes window, discards changes
    discardBt = Button(optionsWindow, text="Discard", width=10, height=1, command= lambda: optionsWindow.destroy()).grid(row=3, column=3, padx=(28,0), pady=(15,0))
    
    # Closes window, saves values
    confirmBt = Button(optionsWindow, text="Confirm", width=10, height=1, command= lambda: saveValues(nfvEntry, ntpEntry, optionsWindow)).grid(row=3, column=4, padx=(5,0), pady=(15,0))


def insertVal(nfvEntry, ntpEntry):
    # ARRANJAR DEFAULT VALUES
    nfvEntry.delete(0, END)
    nfvEntry.insert(0, 100)
    ntpEntry.delete(0, END)
    ntpEntry.insert(0, 200)

def saveValues(nfvEntry, ntpEntry, optionsWindow):
    global framesPerVector, trackingPoints
    framesPerVector = nfvEntry.get()
    trackingPoints = ntpEntry.get()
    optionsWindow.destroy()


def main():

    window = Tk()
    window.title("EcoTracker")
    window.wm_state('zoomed')

    # POSIÇÕES ADAPTADAS AO ECRÃ DO CASAS
    # TOP LEFT BUTTONS
    histogramBt = Button(window, text="Histogram", width=10, height=2).grid(row=1, column=1)
    compassRoseBt = Button(window, text="Compass Rose", width=10, height=2).grid(row=1, column=2, padx=(0,1060))

    # TOP RIGHT BUTTONS

    openBt = Button(window, text="Open", width=10, command=getFileDir).grid(row=1, column=3, columnspan=2)
    saveBt = Button(window, text="Save", width=10, command=saveFile).grid(row=2, column=3, columnspan=2)
    saveAsBt = Button(window, text="Save As", width=10, command=saveFileDir).grid(row=3, column=3, columnspan=2)
    resetPointsBt = Button(window, text="Reset Points", width=10).grid(row=4, column=3, columnspan=2)
    
    # BOTTOM RIGHT BUTTONS
    preferencesBt = Button(window, text="Preferences", width=10, command=optionsWindow).grid(row=10, column=3, pady=(400,10))
    playbackSpeedLb = Label(window, text="Playback Speed", font="helvetica 10 bold").grid(row=11, column=3)
    oneBt = Button(window, text="1x", width=1).grid(row=12, column=3, sticky=E)
    seventyFiveBt = Button(window, text="0.75x", width=1).grid(row=12, column=3)
    halfBt = Button(window, text="0.5x", width=1).grid(row=12, column=3, sticky=W)

    window.mainloop()


if __name__ == '__main__':
    main()