from datetime import datetime
from tkinter import *
from tkinter import ttk

worker_post = {
    'Storage_Type': '',
    'Date_Received': '',
    'Store_Number': '',
    'Contents': '',
    'Problems': '',

}

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
    storage.place(x=20,y=45)

    storeVar = StringVar(win)
    storeVar.set('Store Number') # Def Value
    store = OptionMenu(win, storeVar, *Store_Number)
    store.config(bg="#ffffff")
    store.place(x=135,y=45)

    contentsVar = StringVar(win)
    contentsVar.set('Contents') # Def Value
    contents = OptionMenu(win, contentsVar, *contents_list)
    contents.config(bg="#ffffff")
    contents.place(x=260,y=45)

    problems=Label(win, text="Problems:", font=("Courier 14 bold"))
    problems.place(x=360,y=45)
    problemsent= Entry(win, width= 75)
    problemsent.focus_set()
    problemsent.place(x=475,y=50)

    # text_box = Text(
    #     win,
    #     height=4,
    #     width=20
    # )
    # text_box.pack(expand=True)


    # Button for done
    # Button for another page of items
    ttk.Button(win, text= "Confirm",width= 20, command= done).pack(side = BOTTOM, pady = 10)

    win.mainloop()
    return

warehouse_worker()
time.sleep(100)
def processor():


    return

def generate_excel_file():


    return
