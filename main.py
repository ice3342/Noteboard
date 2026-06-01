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
        self.home_board.place(x=50, y=15, width=2104, height=1261)
        self.home_board.lower()
        self.home_board.columnconfigure(0, weight=1)
        self.home_board.rowconfigure(0, weight=1)
        self.home_board.bind("<Button-1>", self.on_MoveBoard_start)
        self.home_board.bind("<B1-Motion>", self.on_MoveBoard_motion)
        # set the active_board to the home_board
        self.active_board = self.home_board

        boards_bar = tk.Frame(self, bg="#222222")
        boards_bar.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.board_frames = []
        self.boards = []
        self.notes = []
        self.max_board_movement = -250

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
        add_board_btn = tk.Label(tool_frame, image=add_board_btn_img,
                                    bg="#222222", fg="#eeeeee",
                                    highlightthickness = 0, bd = 0,
                                    activebackground="#222222", activeforeground="#ffffff")
        add_board_btn.grid(row=0, column=0, sticky="nw")
        add_board_btn.bind("<Button-1>", lambda event: self.create_widget(event, "board"))
        add_board_btn.bind("<B1-Motion>", self.on_drag_new_widget_motion)
        add_board_btn.bind("<ButtonRelease-1>", self.on_place_new_widget)
        # create the note creation button
        add_note_btn = tk.Button(tool_frame, 
                                image=add_note_btn_img, bg="#222222", fg="#eeeeee",
                                highlightthickness = 0, bd = 0,
                                activebackground="#222222", activeforeground="#ffffff")
        add_note_btn.grid(row=1, column=0, sticky="nw")
        add_note_btn.bind("<Button-1>", lambda event: self.create_widget(event, "note"))
        add_note_btn.bind("<B1-Motion>", self.on_drag_new_widget_motion)
        add_note_btn.bind("<ButtonRelease-1>", self.on_place_new_widget)
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

    # the function that handles the creation of widgets
    def create_widget(self, event, widget_name):
        # create Board
        if widget_name == "board":
            # Creating a new board
            new_board = self.board(master=self.active_board, image=self.board_img, app=self)
            # record the new board to the boards list
            self.boards.append(new_board)
            print("D: board")
            print(f"D: {new_board.board_frame}")
            new_wig = new_board

        # create Note
        elif widget_name == "note":
            # create the note
            new_note = self.note(master=self.active_board, app=self)
            # record the new note to the notes list
            self.notes.append(new_note)
            print("D: note")
            new_wig = new_note

        # on the start of draging the new widget
        self.update_idletasks()
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        widget.new_wig = new_wig

        outOfBounds = self.winfo_geometry().split("+")[0]
        widget.bouds_x, widget.bouds_y =  (int(x) for x in outOfBounds.split("x"))
        print(widget.bouds_x, widget.bouds_y)

    # handle dragging
    def on_drag_new_widget_motion(self, event):
        widget = event.widget
        # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
        if widget.winfo_x() + self.home_board.winfo_x() - widget._drag_start_x + event.x < widget.bouds_x - 50:
            x = max(widget.winfo_x() - widget._drag_start_x + event.x, 0) - 50
            if widget.winfo_y() + self.home_board.winfo_y() - widget._drag_start_y + event.y < widget.bouds_y - 50:
                y = max(widget.winfo_y() - widget._drag_start_y + event.y, 15)
                # place the board
                widget.new_wig.place(x=x, y=y)
    
    def on_place_new_widget(self, event):
        widget = event.widget
        if widget.new_wig.winfo_x() <= -10 or widget.new_wig.winfo_y() <= 15:
            widget.new_wig.destroy()
        widget.new_wig.update()
        print("D: im done updating")
        
    # ----------------

    # the function that handles the back to home action
    def back_to_home(self):
        for child in self.home_board.winfo_children():
            try:
                if child.ISMETHEBOARD_FRAME == "Ya is me":
                    child.place_forget()
            except AttributeError:
                if child.master != self.home_board:
                    child.place_forget()
        # update the active_board variable
        self.active_board = self.home_board
        # get the Home_board button to is off state
        self.Home_board_btn.config(state=tk.DISABLED, cursor="")
        print("back home we go!")

    # handle the moving and expending of the board
    def on_MoveBoard_start(self, event):
        print("yaa you got me ^_^")
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        widget.update_idletasks()

        for child in widget.children.values():
            right = child.winfo_x() + child.winfo_width()
            bottom = child.winfo_y() + child.winfo_height()

            big = 100
            small_x = right + widget.winfo_x() + self.max_board_movement
            small_y = bottom + widget.winfo_y() + self.max_board_movement
            if (small_x >= big or small_y >= big) and (widget.winfo_x() == self.max_board_movement or widget.winfo_y() == self.max_board_movement):
                self.max_board_movement -= 250
                widget.place(width = widget.winfo_width() + 250, height = widget.winfo_height() + 250)
                print("time to grow")
                print(self.max_board_movement)
                break

        print(f"D: X={widget._drag_start_x}")
        print(f"D: Y={widget._drag_start_y}")

    def on_MoveBoard_motion(self, event):
        widget = event.widget
        # the action draging nad the max and min values that x and y can be which is set to the border of the frame
        x = max(min(widget.winfo_x() - widget._drag_start_x + event.x, 0), self.max_board_movement)
        print(f"D:X-{x}")
        y = max(min(widget.winfo_y() - widget._drag_start_y + event.y, 0), self.max_board_movement)
        print(f"D:Y-{y}")
        # place and extend the board
        widget.place(x=x, y=y)
    # ----------------    
    
    # handle dragging
    def on_drag_start(self, event):
            print("yaa you got me ^_^")
            self.update_idletasks()
            widget = event.widget
            widget._drag_start_x = event.x
            widget._drag_start_y = event.y

            outOfBounds = self.winfo_geometry().split("+")[0]
            widget.bouds_x, widget.bouds_y =  (int(x) for x in outOfBounds.split("x"))
            print(widget.bouds_x, widget.bouds_y)


    def on_drag_motion(self, event):
        widget = event.widget
        # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
        if widget.master.winfo_x() + self.home_board.winfo_x() - widget._drag_start_x + event.x < widget.bouds_x - 50:
            x = max(widget.master.winfo_x() - widget._drag_start_x + event.x, 0)
            if widget.master.winfo_y() + self.home_board.winfo_y() - widget._drag_start_y + event.y < widget.bouds_y - 50:
                y = max(widget.master.winfo_y() - widget._drag_start_y + event.y, 15)
                # place the board
                widget.master.place(x=x, y=y)
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
            icon.bind("<Button-1>", app.on_drag_start)
            icon.bind("<B1-Motion>", app.on_drag_motion)

            name.bind("<Double-Button-1>", self.open)
            name.bind("<Button-1>", app.on_drag_start)
            name.bind("<B1-Motion>", app.on_drag_motion)
            name.bind("<KeyRelease>", self.on_release)
            name.bind("<Return>", self.on_enter)

            self.board_frame = tk.Frame(app.active_board, bg="#222222")
            app.board_frames.append(self.board_frame)
            self.board_frame.bind("<Button-1>", app.on_MoveBoard_start)
            self.board_frame.bind("<B1-Motion>", app.on_MoveBoard_motion)
            self.board_frame.ISMETHEBOARD_FRAME = "Ya is me"

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
            self.board_frame.place(width=2104, height=1261)
            self.board_frame.tkraise()

            for child in self.board_frame.winfo_children():
                try:
                    if child.ISMETHEBOARD_FRAME == "Ya is me":
                        child.place_forget()
                except AttributeError: 
                    if child.master != self.board_frame:
                        child.place_forget()

            # Debuging
            print(f"Opening {self.board_frame}")
            print(f"parent: {self.app.active_board}")

            # Turn the Back to home button back on
            self.app.Home_board_btn.config(state=tk.NORMAL, cursor="hand2")

            # update the avite_board variable
            self.app.active_board = self.board_frame

    # the Note
    class note(tk.Frame):
        def __init__(self, master, app):
            super().__init__(master=master)

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)

            Text = tk.Text(self, wrap="word", width=40, height=5)
            Text.grid(row=0, column=0, sticky="nswe")
            resize_point = tk.Label(self, image=app.resize_point_img)
            resize_point.grid(row=0, column=0, sticky="se")
            
            # the actions the entry and resize_point uses
            Text.bind("<Button-1>", app.on_drag_start)
            Text.bind("<B1-Motion>", app.on_drag_motion)
            resize_point.bind("<Button-1>", self.on_start_resizing)
            resize_point.bind("<B1-Motion>", self.on_resizing)

            self.app = app

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


if __name__ == "__main__":
    main()