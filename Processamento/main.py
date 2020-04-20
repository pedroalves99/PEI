from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

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

def main():
    filename = " "                   # Para guardar o nome do ficheiro guardado no saveAs
    window = Tk()
    window.title("EcoTracker")
    window.attributes("-zoomed", True)

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
    preferencesBt = Button(window, text="Preferences", width=10).grid(row=10, column=3, pady=(400,10))
    playbackSpeedLb = Label(window, text="Playback Speed", font="helvetica 10 bold").grid(row=11, column=3)
    oneBt = Button(window, text="1x", width=1).grid(row=12, column=3, sticky=E)
    seventyFiveBt = Button(window, text="0.75x", width=1).grid(row=12, column=3)
    halfBt = Button(window, text="0.5x", width=1).grid(row=12, column=3, sticky=W)

  
    window.mainloop()

main()