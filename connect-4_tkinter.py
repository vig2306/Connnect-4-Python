from tkinter import * 
from tkinter import font
from tkinter.ttk import * 
from PIL import ImageTk, Image

import os
def call_window_Two_player():
    os.system("python game.py")
    

def call_window_One_player():
    os.system("python connect4_with_ai.py")

def call_window_tkinterpage():
    root = Tk()
    root.title('Connect-4')
    root.geometry("300x260")

    x=Label(root, text="Player 1:", font="none 14 bold", width=700, anchor=CENTER)
    x.place(relx=0.5, rely=0.1, anchor=CENTER)
    
    y=Label(root, text="Player 2:", font="none 14 bold", width=700, anchor=CENTER)
    y.place(relx=0.5, rely=0.4, anchor=CENTER)

    n1 = StringVar()
    name1 = Entry(root, textvariable=n1, width=13)
    name1.config(font=("Arial", 15))
    name1.focus_set()  
    name1.place(relx=0.5, rely=0.22, anchor=CENTER)

    n2= StringVar()
    name2 = Entry(root,textvariable=n2, width=13)
    name2.config(font=("Arial", 15))
    name2.focus_set()  
    name2.place(relx=0.5, rely=0.52, anchor=CENTER)

    button = Button(root, text="START", width=12, command= call_window_Two_player)
    button.place(relx=0.5, rely=0.75, anchor=CENTER)


root = Tk()
root.title("Connect-4")
root.geometry("460x460")

root.style = Style() 
root.style.configure('W.TButton', font = 
               ('calibri', 20), 
                    borderwidth = '4') 
#('clam', 'alt', 'default', 'classic')
root.style.theme_use("clam")
  
frame= Frame(root)
frame.pack()

imgpath = 'tkinter_1.jpg'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas = Canvas(root,width=460,height=460)
canvas.create_image(0,0,anchor=NW,image=photo)
canvas.pack()


w = Label(root, text="Connect-4", font="none 24 bold", width=700, anchor=CENTER)
w.place(relx=0.5, rely=0.1, anchor=CENTER)


button1 = Button(root, text="ONE PLAYER", width=20, command= call_window_One_player)
button1.place(relx=0.5, rely=0.3, anchor=CENTER)

button2 = Button(root, text="TWO PLAYER", width=20,command= call_window_tkinterpage)
button2.place(relx=0.5, rely=0.45, anchor=CENTER)

button3 = Button(root, text="EXIT", width=20, command= frame.quit)
button3.place(relx=0.5, rely=0.6, anchor=CENTER)


        
root.mainloop()






