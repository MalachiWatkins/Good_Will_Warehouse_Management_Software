from datetime import datetime
from tkinter import *
from tkinter import ttk

Storage_Type = ['Tote', 'Gaylord', 'Other']
Store_Number = ['224', '118']
def main():
    def done():

        return
    win= Tk()
    win.title("Warehouse Management")
    win.geometry("800x500")

    MainLable=Label(win, text="Received Information", font=("Courier 22 bold"))
    MainLable.pack()

    storageVar = StringVar(win)
    storageVar.set('Storage Type') # Def Value
    storage = OptionMenu(win, storageVar, *Storage_Type)
    storage.config(bg="#ffffff")
    storage.pack()   #place(x=20,y=45)

    storeVar = StringVar(win)
    storeVar.set('Store Number') # Def Value
    store = OptionMenu(win, storeVar, *Store_Number)
    store.config(bg="#ffffff")
    store.pack()   #place(x=20,y=45)

    ttk.Button(win, text= "Confirm",width= 20, command= done).pack(side = BOTTOM, pady = 10)

    win.mainloop()
    return

main()
time.sleep(100)
