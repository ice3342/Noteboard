import tkinter as tk
import os
from PIL import ImageTk, Image

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x600")

        # set the weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # create the sidebar frame
        sidebar_frame = tk.Frame(self)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.rowconfigure(0, weight=1)

        # create the wiget frame
        self.widget_frame = tk.Frame(self, bg="#222222")
        self.widget_frame.grid(row=0, column=1, sticky="nsew")

        # get and resize the icon images for use
        board_img_raw = Image.open("images/board_images/icy_fish.png").resize((50, 50))
        self.board_img = ImageTk.PhotoImage(board_img_raw)
        add_board_btn_img_raw = Image.open("images/btns/boads.png").resize((50, 50))
        add_board_btn_img = ImageTk.PhotoImage(add_board_btn_img_raw)
        # create and grid the add board btn
        add_board_btn = tk.Button(sidebar_frame, image=add_board_btn_img, bg="#222222", command=self.create_board)
        add_board_btn.grid(row=0, column=0, sticky="nw")

    # the function that handles the board creation
    def create_board(self):
        # give the board class what it need and grid it to row=0 clmn=0
        board_wiget = board(master=self.widget_frame, image=self.board_img)
        board_wiget.grid(row=0, column=0)

# the board
class board(tk.Label):
    def __init__(self, master, image):
        super().__init__(master=master, image=image)

        # get the offset variables ready
        self.offset_x = 0
        self.offset_y = 0

        # the actions the board uses
        self.bind('<Double-Button-1>', self.open)
        self.bind("<Button-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)

    # what happens when you open the board 
    def open(self, event):
        print("OPEN!!!")

    # handle dragging
    def on_drag_start(self, event):
        # remove the +X+Y part of geometry
        only_width_and_hight = self.master.winfo_geometry().split("+")[0]
        # split the width and hight into the max values of x and y
        self.max_x, self.max_y = (int(x) for x in only_width_and_hight.split("x"))

        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
        x = max(min(widget.winfo_x() - widget._drag_start_x + event.x, self.max_x - 50), 0)
        y = max(min(widget.winfo_y() - widget._drag_start_y + event.y, self.max_y - 50) , 0)
        # place the board
        widget.place(x=x, y=y)
    # ----------------

if __name__ == "__main__":
    main()