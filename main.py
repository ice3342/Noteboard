import tkinter as tk
import os
from PIL import ImageTk, Image

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()     
        img_raw = Image.open("icy.fish.png").resize((50, 50))
        img = ImageTk.PhotoImage(img_raw)

class board(tk.Label):
    def __init__(self, image):
        super().__init__(image=image)
        self.offset_x = 0
        self.offset_y = 0
        self.bind('<Double-Button-1>', self.open)
        self.bind("<Button-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.configure(cursor="hand1")

    def open(self, event):
        print("OPEN!!!")
    
    def on_start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        new_x = event.x_root - self.winfo_toplevel().winfo_rootx() - self.offset_x
        new_y = event.y_root - self.winfo_toplevel().winfo_rooty() - self.offset_y
        self.place(x=new_x, y=new_y)

    def on_drop(self, event):
        self.on_drag(event)

if __name__ == "__main__":
    main()