import tkinter as tk
import os
from PIL import ImageTk, Image
import numpy as np

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x600")

        # set the weights for self
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # create the sidebar frame
        tool_frame = tk.Frame(self)
        tool_frame.grid(row=1, column=0, sticky="nsew")
        tool_frame.rowconfigure(0, weight=1)

        # create the wiget frame
        self.home_board = tk.Frame(self, bg="#222222")
        self.home_board.grid(row=1, column=1, sticky="nsew")
        self.home_board.columnconfigure(0, weight=1)
        self.home_board.rowconfigure(0, weight=1)

        # set the active_board to the home_board
        self.active_board = self.home_board

        boards_bar = tk.Frame(self, bg="#222222")
        boards_bar.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.board_frames = []
        self.boards = []

        # get and resize the icon images for use
        board_img_raw = Image.open("images/board_images/icy_fish.png").resize((50, 50))
        self.board_img = ImageTk.PhotoImage(board_img_raw)
        add_board_btn_img_raw = Image.open("images/btns/boads.png").resize((50, 50))
        add_board_btn_img = ImageTk.PhotoImage(add_board_btn_img_raw)
        # create and grid the add board btn
        add_board_btn = tk.Button(tool_frame, image=add_board_btn_img, bg="#222222", command=self.create_board)
        add_board_btn.grid(row=0, column=0, sticky="nw")

        # create the back btn
        Home_board_btn = tk.Button(boards_bar, text="Home", command=self.back_to_home, bg="#222222", fg="#eeeeee")
        Home_board_btn.grid(row=0, column=0, sticky="nw")

    # the function that handles the board creation
    def create_board(self):
        # give the board class what it need and grid it to row=0 clmn=0
        new_board = self.board(master=self.active_board, image=self.board_img, active_board=self.active_board, board_frames=self.board_frames, boards=self.boards).grid(row=0, column=0)
        self.boards.append(new_board)

    def back_to_home(self):
            (self.board_frames[x].grid_forget() for x in range(0, len(self.board_frames)))
            (self.boards[x].grid_forget() for x in range(0, len(self.boards)))
            


    # the board
    class board(tk.Label):
        def __init__(self, master, image, active_board, board_frames, boards):
            super().__init__(master=master, image=image)

            # get the offset variables ready
            self.offset_x = 0
            self.offset_y = 0

            self.active_board = active_board

            # the actions the board uses
            self.bind('<Double-Button-1>', self.open)
            self.bind("<Button-1>", self.on_drag_start)
            self.bind("<B1-Motion>", self.on_drag_motion)

            self.board_frame = tk.Frame(active_board, bg="#222222")
            board_frames.append(self.board_frame)

        # what happens when you open the board
        def open(self, event):
            self.board_frame.grid(row=0, column=0, sticky="nsew")
            self.active_board = self.board_frame
            print("Open!!!")
            

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