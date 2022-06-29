from datetime import datetime
from tkinter import *
from tkinter import ttk

Storage_Type = ['Tote', 'Gaylord', 'Other']
def main():
    def done():

        return
    win= Tk()
    win.title("")
    win.geometry("800x500")
    MainLable=Label(win, text="System Information", font=("Courier 22 bold"))
    MainLable.pack()
    listerVar = StringVar(win)
    listerVar.set('Lister Name') # Def Value
    lister = OptionMenu(win, listerVar, *lister_names)
    lister.config(bg="#ffffff")
    lister.place(x=20,y=45)

    ttk.Button(win, text= "Confirm",width= 20, command= done).pack(side = BOTTOM, pady = 10)

    win.mainloop()
    return

main()
time.sleep(100)
