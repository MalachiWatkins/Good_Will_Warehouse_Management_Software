from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Button
import time
from datetime import date
from tkinter import messagebox
from pymongo import MongoClient
import pymongo

warehouse_db = cluster["WAREHOUSE_MANAGEMENT"]
receiverCollection = warehouse_db["receiver"]

processor_post = {
    'Storage_Type': '',
    'Date_Received': '',
    'Date_Processed': '',
    'Manifest_Number': '',
    'Store_Number': '',
    'Contents': '',
    'Problems': '',

}

Storage_Type = ['Tote', 'Gaylord', 'Other']
Store_Number = ['224', '118']
contents_list = ['Jewelry', 'Collectables', 'Books', 'Media']
def warehouse_worker():
    global storageVar
    global storeVar
    global contentsVar
    global problemsent
    global quantent

    def add():

        today = date.today()
        date_format = today.strftime("%B %d, %Y")
        receiver_post = {
            'Quantity': quantent.get(),
            'Storage_Type': storageVar.get(),
            'Date_Received': date_format,
            'Store_Number': storeVar.get(),
            'Contents': contentsVar.get(),
            'Problems': problemsent.get(),

        }
        if storageVar.get() != "Storage Type":
            receiverCollection.insert_one(receiver_post)
            print(receiver_post)
            messagebox.showinfo("showinfo", "Data Submitted")
        ##
        # MongoDB stuff Goes here
        ##
        # Insted of exit create a gui showing complete
        return


    win= Tk()
    win.title("Warehouse Management")
    win.geometry("1050x200")

    MainLable=Label(win, text="Received Information", font=("Courier 22 bold"))
    MainLable.pack()

    quant=Label(win, text="Quantity:", font=("Courier 14 bold"))
    quant.place(x=10,y=45)
    quantent= Entry(win, width= 2)
    quantent.focus_set()
    quantent.place(x=120,y=50)

    storageVar = StringVar(win)
    storageVar.set('Storage Type') # Def Value
    storage = OptionMenu(win, storageVar, *Storage_Type)
    storage.config(bg="#ffffff")
    storage.place(x=140,y=45)

    storeVar = StringVar(win)
    storeVar.set('Store Number') # Def Value
    store = OptionMenu(win, storeVar, *Store_Number)
    store.config(bg="#ffffff")
    store.place(x=250,y=45)

    contentsVar = StringVar(win)
    contentsVar.set('Contents') # Def Value
    contents = OptionMenu(win, contentsVar, *contents_list)
    contents.config(bg="#ffffff")
    contents.place(x=370,y=45)

    problems=Label(win, text="Problems:", font=("Courier 14 bold"))
    problems.place(x=480,y=45)
    problemsent= Entry(win, width= 75)
    problemsent.focus_set()
    problemsent.place(x=580,y=50)

    button = Button(win, text="Done", command=lambda: [add(), win.destroy()])
    button.pack(side = BOTTOM, pady = 10)

    button1 = Button(win, text="Add", command=lambda: [ add(), win.destroy(), warehouse_worker()])
    button1.pack(side = BOTTOM, pady = 10)


    win.mainloop()
    return

def processor():
    ##
    # MongoDB STUFF GOES HERE
    ##
    return

def main():
    win= Tk()
    win.title("Warehouse Management")
    win.geometry("950x200")

    MainLable=Label(win, text="Warehouse Management ", font=("Courier 22 bold"))
    MainLable.pack()


    button1 = Button(win, text="Receiving", command=lambda: [ win.destroy(),warehouse_worker()])
    button1.pack(side = BOTTOM, pady = 10)

    button = Button(win, text="Processor", command=lambda: [ win.destroy(),processor()])
    button.pack(side = BOTTOM, pady = 10)
    win.mainloop()

    return

def generate_excel_file():


    return

main()
time.sleep(100)
