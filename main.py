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
        lb1 = board(img)
        lb1.place(x=10, y=10)
        lb1.add_dragable_widget(lb1)

class board(tk.Label):
    def __init__(self, image):
        super().__init__(image=image)
        self.bind('<Double-Button-1>', self.open)

    def open(self, event):
        print("OPEN!!!")

    def add_dragable_widget(self, widget):
        self.widget = widget
        self.offset_x = 0
        self.offset_y = 0
        self.widget.bind("<Button-1>", self.on_start_drag)
        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<ButtonRelease-1>", self.on_drop)
        self.widget.configure(cursor="hand1")
    
    def on_start_drag(self, event):
        # Calculate offset between mouse and widget's top-left corner
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        new_x = event.x_root - self.widget.winfo_toplevel().winfo_rootx() - self.offset_x
        new_y = event.y_root - self.widget.winfo_toplevel().winfo_rooty() - self.offset_y
        self.widget.place(x=new_x, y=new_y)

    def on_drop(self, event):
        self.on_drag(event)

if __name__ == "__main__":
    main()