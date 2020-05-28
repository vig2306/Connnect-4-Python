from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image

def call_game():
    root.destroy()
    os.system("python game_ai.py")

def call_gui():
    root.destroy()
    os.system("python gui.py")

root = Tk()
root.title("Connect-4")
root.geometry("400x150")
root.configure(bg='white')
root.style = ttk.Style() 
root.style.configure('TButton', font = ('calibri', 20),borderwidth = '4') 
#('clam', 'alt', 'default', 'classic')
root.style.theme_use("clam")
    
frame= Frame(root)
frame.pack()

imgpath = 'image.PNG'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas = Canvas(root,width=400,height=150)
canvas.create_image(535,200,anchor=E,image=photo)
canvas.pack(side="right")

button1 = ttk.Button(root, text="Play Again", width=18, command=call_game)
button1.place(relx =0.15, rely=0.4, anchor=W)

button2 = ttk.Button(root, text="Main Menu", width=18, command= call_gui)
button2.place(relx=0.55, rely=0.4, anchor=W)

        
root.mainloop()

 
