import tkinter as tk
from PIL import ImageTk, Image
import os
import time as tm
import json

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
        tool_frame = tk.Frame(self, bg="#242424")
        tool_frame.grid(row=1, column=0, sticky="nsew")

        # create the wiget frame
        self.home_board = tk.Frame(self, bg="#222222")
        self.home_board.place(x=50, y=15, width=1000, height=1000)
        self.home_board.lower()
        self.home_board.columnconfigure(0, weight=1)
        self.home_board.rowconfigure(0, weight=1)
        self.home_board.bind("<Button-1>", self.on_drag_start)
        self.home_board.bind("<B1-Motion>", self.on_drag_motion)

        # set the active_board to the home_board
        self.active_board = self.home_board

        boards_bar = tk.Frame(self, bg="#222222")
        boards_bar.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.board_frames = []
        self.boards = []
        self.notes = []

        # get and resize the icon images for use
        # the image for the boards icon
        board_img_raw = Image.open("images/board_images/icy_fish.png").resize((50, 50))
        self.board_img = ImageTk.PhotoImage(board_img_raw)
        # the image for the button that adds board
        add_board_btn_img_raw = Image.open("images/widgets/boads.png").resize((50, 50))
        add_board_btn_img = ImageTk.PhotoImage(add_board_btn_img_raw)
        # the image for the button that adds notes
        add_note_btn_img_raw = Image.open("images/widgets/sticky-note_light.png").resize((50, 50))
        add_note_btn_img = ImageTk.PhotoImage(add_note_btn_img_raw)

        resize_point_img_raw = Image.open("images/widgets/resize_point.png").resize((10, 10))
        self.resize_point_img = ImageTk.PhotoImage(resize_point_img_raw)

        # create and grid the add board btn
        add_board_btn = tk.Button(tool_frame, image=add_board_btn_img,
                                  command=self.create_board,
                                    bg="#222222", fg="#eeeeee",
                                    highlightthickness = 0, bd = 0,
                                    activebackground="#222222", activeforeground="#ffffff")
        add_board_btn.grid(row=0, column=0, sticky="nw")
        # create the note creation button
        add_note_btn = tk.Button(tool_frame,
                                 image=add_note_btn_img,
                                 command=self.create_note,
                                    bg="#222222", fg="#eeeeee",
                                    highlightthickness = 0, bd = 0,
                                    activebackground="#222222", activeforeground="#ffffff")
        add_note_btn.grid(row=1, column=0, sticky="nw")
        # create the back to home btn in is off state
        self.Home_board_btn = tk.Button(boards_bar,
                                        text="Home",
                                        command=self.back_to_home,
                                        bg="#222222", fg="#eeeeee",
                                        height=1, width=4,
                                        state=tk.DISABLED,
                                        highlightthickness = 0, bd = 0,
                                        activebackground="#222222", activeforeground="#ffffff")
        self.Home_board_btn.grid(row=0, column=0, sticky="nw")

        board_separator = tk.Label(boards_bar, text="/", bg="#222222", fg="#ffffff").grid(row=0, column=1)
        
        # Add save/load buttons or keyboard shortcuts
        self.bind("<Control-s>", lambda e: self.export_state())
        self.bind("<Control-o>", lambda e: self.import_state())
    
    def export_state(self):
        """Export all children and their positions to JSON"""
        state = {
            "window": {
                "geometry": self.geometry(),
                "state": self.state()
            },
            "boards": [],
            "notes": []
        }

        # Export boards
        for board in self.boards:
            if board.master == self.home_board:
                parent_index = -1
            else:
                parent_index = next(
                    (i for i, b in enumerate(self.boards) if b.board_frame is board.master),
                    -1
                )
            board_data = {
                "parent_index" : parent_index,
                "x": board.winfo_x(),
                "y": board.winfo_y(),
                "width": board.winfo_width(),
                "height": board.winfo_height(),
                "name": board.winfo_children()[1].get("1.0", "end-1c").strip(),  # Get board name
                "name_width" : int(board.winfo_children()[1]["width"]),
                "name_height" : int(board.winfo_children()[1]["height"])
                
            }
            state["boards"].append(board_data)
        
        # Export notes
        for note in self.notes:
            if note.master == self.home_board:
                parent_index = -1
            else:
                parent_index = next(
                    (i for i, b in enumerate(self.boards) if b.board_frame is note.master),
                    -1
                )
            note_data = {
                "parent_index" : parent_index,
                "x": note.winfo_x(),
                "y": note.winfo_y(),
                "width": note.winfo_width(),
                "height": note.winfo_height(),
                "text": note.winfo_children()[0].get("1.0", "end-1c").strip()  # Get note text
            }
            state["notes"].append(note_data)
        
        # Save to file
        with open("app_state.json", "w") as f:
            json.dump(state, f, indent=2)
        
        print("State exported successfully!")
    
    def import_state(self):
        """Import and restore all children positions from JSON"""
        try:
            with open("app_state.json", "r") as f:
                state = json.load(f)
            
            # Restore window state
            self.geometry(state["window"]["geometry"])
            if state["window"]["state"] == "zoomed":
                self.state("zoomed")
            
            # Clear existing boards and notes
            for board in self.boards:
                board.destroy()
            for note in self.notes:
                note.destroy()
            self.boards.clear()
            self.notes.clear()
            
            # Restore boards
            for board_data in state["boards"]:
                if board_data["parent_index"] == -1:
                    masters_frame = self.home_board
                else:
                    masters_frame = self.boards[board_data["parent_index"]].board_frame

                new_board = self.board(master=masters_frame,
                                       image=self.board_img,
                                       app=self)
                new_board.place(x=board_data["x"], y=board_data["y"])
                # Restore name
                name_widget = new_board.winfo_children()[1]
                name_widget.delete("1.0", "end")
                name_widget.insert("1.0", board_data["name"])
                name_widget.configure(width=board_data["name_width"],
                                      height=board_data["name_height"])
                name_widget.tag_add("center", "1.0", "end")
                self.boards.append(new_board)
            
            # Restore notes
            for note_data in state["notes"]:
                if note_data["parent_index"] == -1:
                    masters_frame = self.home_board
                else:
                    masters_frame = self.boards[note_data["parent_index"]].board_frame
                new_note = self.note(master=masters_frame, app=self)
                new_note.place(x=note_data["x"], y=note_data["y"], 
                             width=note_data["width"], height=note_data["height"])
                # Restore text
                text_widget = new_note.winfo_children()[0]
                text_widget.delete("1.0", "end")
                text_widget.insert("1.0", note_data["text"])
                self.notes.append(new_note)
            
            print("State imported successfully!")
            
        except FileNotFoundError:
            print("No saved state file found")
        except Exception as e:
            print(f"Error importing state: {e}")

    # the function that handles the board creation
    def create_board(self):
        # get the position to place the new board
        center_x = self.home_board.winfo_width() / 2
        center_y = self.home_board.winfo_height() / 2
        # Creating a new board
        new_board = self.board(master=self.active_board, image=self.board_img, app=self)
        # place the board
        new_board.place(x=center_x, y=center_y)
        # record it to the boards list
        self.boards.append(new_board)
    
    def create_note(self):
        # get the position to place the new board
        center_x = self.home_board.winfo_width() / 2
        center_y = self.home_board.winfo_height() / 2
        # create the note
        new_note = self.note(master=self.active_board, app=self)
        # place the note
        new_note.place(x=center_x, y=center_y, width=300, height=80)
        self.notes.append(new_note)

    # the function that handles the back to home action
    def back_to_home(self):
        for child in self.home_board.winfo_children():
            if isinstance(child, tk.Frame):
                child.grid_forget()
            elif child.master != self.home_board:
                child.place_forget()
        # update the active_board variable
        self.active_board = self.home_board
        # get the Home_board button to is off state
        self.Home_board_btn.config(state=tk.DISABLED, cursor="")
        print("back home we go!")

    # handle dragging
    def on_drag_start(self, event):
        print("yaa you got me ^_^")
        # remove the +X+Y part of geometry
        only_width_and_hight = event.widget.master.winfo_geometry().split("+")[0]
        # split the width and hight into the max values of x and y
        self.max_x, self.max_y = (int(a) for a in only_width_and_hight.split("x"))

        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        print(f"D: X={widget._drag_start_x}")
        print(f"D: Y={widget._drag_start_y}")

    def on_drag_motion(self, event):
        widget = event.widget
        # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
        x = min(widget.winfo_x() - widget._drag_start_x + event.x, self.max_x - 50)
        y = min(widget.winfo_y() - widget._drag_start_y + event.y, self.max_y - 50)
        # place and extend the board
        widget.place(x=x, y=y)
        print(f"D: {widget.winfo_width()}")
    # ----------------    
            

    # the board
    class board(tk.Frame):
        def __init__(self, master, image, app):
            super().__init__(master=master, bg="#222222")
            self.rowconfigure(1, weight=1)

            icon = tk.Label(self, image=image)
            icon.grid(row=0,column=0)
            name = tk.Text(self, width=8, height=1,
                           wrap="word",
                           bg=self["bg"], fg="#ffffff",
                           bd=0, highlightthickness=0,
                           insertbackground="#aaaaaa")
            name.tag_configure("center", justify="center")
            name.insert(0.0, "board")
            name.tag_add("center", "0.0", "end")
            name.grid(row=1, column=0)

            # get the offset variables ready
            self.offset_x = 0
            self.offset_y = 0

            # the actions the board uses
            icon.bind("<Double-Button-1>", self.open)
            icon.bind("<Button-1>", self.on_drag_start)
            icon.bind("<B1-Motion>", self.on_drag_motion)

            name.bind("<Double-Button-1>", self.open)
            name.bind("<Button-1>", self.on_drag_start)
            name.bind("<B1-Motion>", self.on_drag_motion)
            name.bind("<KeyRelease>", self.on_release)
            name.bind("<Return>", self.on_enter)

            self.board_frame = tk.Frame(app.active_board, bg="#222222")
            app.board_frames.append(self.board_frame)

            self.board_frame.rowconfigure(0, weight=1)
            self.board_frame.columnconfigure(0, weight=1)

            self.app = app
            self.old_name_length = 0

        def on_release(self, event):
            widget = event.widget
            widget.tag_add("center", "1.0", "end")
            first, last = widget.yview()
            print(f"D: F-{first}, L-{last}")

            if len(widget.get("1.0", "end-1c")) < self.old_name_length:
                print("D: Del")
                print(f"D: {widget.get("1.0", "end-1c")}")
                if widget["width"] > 13 and len(widget.get("1.0", "end-1c")) % 14 == 0:
                    widget.config(height=int(widget["height"] - 1))
                elif first == 0 and len(widget.get("1.0", "end-1c")) <= 14 and int(widget["width"]) > 8:
                    widget.config(width=int(widget["width"]) - 1)


            elif widget["width"] > 13 and first > 0:
                widget.config(height=int(widget["height"] + 1))
            elif first > 0:
                widget.config(width=int(widget["width"] + 2))
            print(f"old L-{self.old_name_length}, new L-{len(widget.get("1.0", "end-1c"))}")
            print("\n")
            self.old_name_length = len(widget.get("1.0", "end-1c"))

        def on_enter(self, event):
            return "break"


        # what happens when you open the board
        def open(self, event):
            # grid the board_frame to be seen
            self.board_frame.grid(row=0, column=0, sticky="nsew")
            self.board_frame.tkraise()

            for child in self.board_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.grid_forget()
                elif child.master != self.board_frame:
                    child.place_forget()

            # Debuging
            print(f"Opening {self.board_frame}")
            print(f"parent: {self.app.active_board}")

            # Turn the Back to home button back on
            self.app.Home_board_btn.config(state=tk.NORMAL, cursor="hand2")

            # update the avite_board variable
            self.app.active_board = self.board_frame



        # handle dragging
        def on_drag_start(self, event):
                print("yaa you got me ^_^")
                # remove the +X+Y part of geometry
                only_width_and_hight = self.master.master.winfo_geometry().split("+")[0]
                # split the width and hight into the max values of x and y
                self.max_x, self.max_y = (int(x) for x in only_width_and_hight.split("x"))

                widget = event.widget
                widget._drag_start_x = event.x
                widget._drag_start_y = event.y

        def on_drag_motion(self, event):
            widget = event.widget
            # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
            x = max(min(widget.master.winfo_x() - widget._drag_start_x + event.x, self.max_x - 50), 0)
            y = max(min(widget.master.winfo_y() - widget._drag_start_y + event.y, self.max_y - 50) , 0)
            # place the board
            widget.master.place(x=x, y=y)
        # ----------------

    # the Note
    class note(tk.Frame):
        def __init__(self, master, app):
            super().__init__(master=master)

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)

            Text = tk.Text(self, wrap="word")
            Text.grid(row=0, column=0, sticky="nswe")
            resize_point = tk.Label(self, image=app.resize_point_img)
            resize_point.grid(row=0, column=0, sticky="se")
            
            # the actions the entry and resize_point uses
            Text.bind("<Button-1>", self.on_drag_start)
            Text.bind("<B1-Motion>", self.on_drag_motion)
            resize_point.bind("<Button-1>", self.on_start_resizing)
            resize_point.bind("<B1-Motion>", self.on_resizing)

        # handle resizing
        def on_start_resizing(self, event):
            # create an instense of the resize handle
            # to create variables and get is containers width/height
            widget = event.widget
            # get the width/height of the container before any modifying
            widget.start_width = widget.master.winfo_width()
            widget.start_height = widget.master.winfo_height()
            # get the positon of the handle
            widget.start_x_point = event.x_root
            widget.start_y_point = event.y_root
            # Debuging
            print(f"D: W-{widget.start_width}, H-{widget.start_height}")
            print("D:OSR")
        
        def on_resizing(self, event):
            # create an instense of the resize handle
            widget = event.widget

            # a variable to track how far
            # the x/y of the pointer is from the start of the resizing
            dx = event.x_root - widget.start_x_point
            dy = event.y_root - widget.start_y_point
            
            # create a new size for the container
            # that is more then 40
            new_width = max(40, widget.start_width + dx)
            new_height = max(40, widget.start_height + dy)
            # debuging
            print(f"D: W-{new_width}, H-{new_height}")
            # apply the new width/height to the container
            widget.master.place_configure(width=new_width, height=new_height)
        # ----------------

        # handle dragging
        def on_drag_start(self, event):
            print("yaa you got me ^_^")
            # remove the +X+Y part of geometry
            only_width_and_hight = self.master.master.winfo_geometry().split("+")[0]
            # split the width and hight into the max values of x and y
            self.max_x, self.max_y = (int(x) for x in only_width_and_hight.split("x"))

            widget = event.widget.master
            widget._drag_start_x = event.x
            widget._drag_start_y = event.y

        def on_drag_motion(self, event):
            widget = event.widget.master
            # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
            x = max(min(widget.winfo_x() - widget._drag_start_x + event.x, self.max_x - 50), 0)
            y = max(min(widget.winfo_y() - widget._drag_start_y + event.y, self.max_y - 50) , 0)
            # place the board
            widget.place(x=x, y=y)
        # ----------------


if __name__ == "__main__":
    main()