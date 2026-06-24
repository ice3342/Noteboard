import tkinter as tk
from PIL import ImageTk, Image
import os
import time as tm
import json
import movement as move
import widgets as wig
def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    # what happends at launch 00
    def __init__(self):
        super().__init__()
        self.geometry("850x600")

        # set the weights for self
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # create the sidebar frame
        tool_frame = tk.Frame(self, bg="#242424")
        tool_frame.grid(row=1, column=0, sticky="nsew")

        # active widget frame
        self.ActiveWig_Frame = tk.Frame(self, bg="#242424")
        # an empty frame that is there to show you can't change the widget
        self.empty_frame = tk.Frame(self.ActiveWig_Frame, bg="#242424")

        # create the wiget frame
        self.home_board = tk.Frame(self, bg="#222222")
        self.home_board.place(x=50, y=15, width=2104, height=1261)
        self.home_board.lower()
        self.home_board.app = self
        self.home_board.columnconfigure(0, weight=1)
        self.home_board.rowconfigure(0, weight=1)
        self.home_board.bind("<Button-1>", move.on_MoveBoard_start)
        self.home_board.bind("<B1-Motion>", move.on_MoveBoard_motion)
        self.home_board.ISMETHEFRAME = "Ya is me"
        # set the active_board to the home_board
        self.active_board = self.home_board

        boards_bar = tk.Frame(self, bg="#222222")
        boards_bar.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.board_frames = []
        self.boards = []
        self.notes = []
        self.max_board_movement = -250
        self.focused_on = self.home_board

        # load the images
        self.loadImages()

        # create and grid the add board btn
        add_board_btn = tk.Label(tool_frame, image=self.add_board_btn_img,
                                    bg="#222222", fg="#eeeeee",
                                    highlightthickness = 0, bd = 0,
                                    activebackground="#222222", activeforeground="#ffffff")
        add_board_btn.grid(row=0, column=0, sticky="nw")
        add_board_btn.bind("<Button-1>", lambda event: self.create_widget(event, "board"))
        add_board_btn.bind("<B1-Motion>", self.on_drag_new_widget_motion)
        add_board_btn.bind("<ButtonRelease-1>", self.on_place_widget)
        # create the note creation button
        add_note_btn = tk.Button(tool_frame, 
                                image=self.add_note_btn_img, bg="#222222", fg="#eeeeee",
                                highlightthickness = 0, bd = 0,
                                activebackground="#222222", activeforeground="#ffffff")
        add_note_btn.grid(row=1, column=0, sticky="nw")
        add_note_btn.bind("<Button-1>", lambda event: self.create_widget(event, "note"))
        add_note_btn.bind("<B1-Motion>", self.on_drag_new_widget_motion)
        add_note_btn.bind("<ButtonRelease-1>", self.on_place_widget)
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
        self.bind("<Delete>", self.on_delete)

    # activate the active wigets editor frame
    def Activate_ActiveWig_Frame(self):
        # check if its a frame
        try:
            if self.focused_on.ISMETHEFRAME == "Ya is me":
                self.ActiveWig_Frame.grid_forget()
                print("its a frame")
        # if not open the widgets editor
        except AttributeError:
            # check if the widget has a editor frame
            try:
                self.ActiveWig_Frame.grid(row=1, column=0, sticky="nsew")
                self.focused_on.editor_frame.grid(row=1, column=0, sticky="nsew")
                self.focused_on.editor_frame.tkraise()
            # if no, grid an empty one that show there is nothing to change
            except AttributeError:
                print("the widget doesn't have an editor frame")
                self.empty_frame.grid(row=1, column=0, sticky="nsew")
                self.empty_frame.tkraise()
            

    # the save funcions 08
    def export_state(self):
        """Export all children and their positions to JSON"""
        state = {
            "window": {
                "geometry": self.geometry(),
                "state": self.state()
            },
            "boards": [],
            "notes": [],
            "max_board_movement": self.max_board_movement
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
                board.board_frame.destroy()
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

                new_board = wig.board(master=masters_frame,
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
                new_note = wig.note(master=masters_frame, app=self)
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
    # ----------

    # the function that handles the creation of widgets 03
    def create_widget(self, event, widget_name):
        # create Board
        if widget_name == "board":
            # Creating a new board
            new_board = wig.board(master=self.active_board, image=self.board_img, app=self)
            # record the new board to the boards list
            self.boards.append(new_board)
            print("D: board")
            print(f"D: {new_board.board_frame}")
            new_wig = new_board

        # create Note
        elif widget_name == "note":
            # create the note
            new_note = wig.note(master=self.active_board, app=self)
            # record the new note to the notes list
            self.notes.append(new_note)
            print("D: note")
            new_wig = new_note
        
        for child in new_wig.children.values():
            child.bind("<ButtonRelease-1>", self.on_place_widget)

        # on the start of draging the new widget
        self.update_idletasks()
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        widget.new_wig = new_wig

        outOfBounds = self.winfo_geometry().split("+")[0]
        widget.bouds_x, widget.bouds_y =  (int(x) for x in outOfBounds.split("x"))
        print(widget.bouds_x, widget.bouds_y)

    # the delete widget from the baord action 02
    def on_delete(self, event):
        widget = self.focused_on
        
        # is the widget an instance of the baord
        if isinstance(widget, wig.board):
            # try removing the widget and its board_frame from the there lists if posible 
            # and delete them
            try:
                self.boards.remove(widget)
                widget.destroy()
                self.board_frames.remove(widget.board_frame)
                widget.board_frame.destroy()
            except ValueError:
                print("E: the board was not on the list")
            print("is a board")
        # is the widget an instance of the note
        elif isinstance(widget, wig.note):
            # try removing the widget from its list if posible and delete it
            try:
                self.notes.remove(widget)
                widget.destroy()

            except ValueError:
                print("E: the note was not on the list")
            print("is a note")

    # handle dragging of the new widgets 05
    def on_drag_new_widget_motion(self, event):
        widget = event.widget
        # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
        if widget.winfo_x() + self.home_board.winfo_x() - widget._drag_start_x + event.x < widget.bouds_x - 50:
            x = max(widget.winfo_x() - widget._drag_start_x + event.x, 0) - 50
            if widget.winfo_y() + self.home_board.winfo_y() - widget._drag_start_y + event.y < widget.bouds_y - 50:
                y = max(widget.winfo_y() - widget._drag_start_y + event.y, 15)
                # place the widget
                widget.new_wig.place(x=x, y=y)
    # ----------------
    def on_place_widget(self, event):
        try:
            widget = event.widget
            if widget.new_wig.winfo_x() <= -10 or widget.new_wig.winfo_y() <= 15:
                if isinstance(widget.new_wig, wig.board):
                    try:
                        self.boards.remove(widget.new_wig)
                        self.board_frames.remove(widget.new_wig.board_frame)
                        widget.new_wig.board_frame.destroy()
                    except ValueError:
                        print("E: the board was not on the list")
                    print("is a board")
                elif isinstance(widget.new_wig, wig.note):
                    try:
                        self.notes.remove(widget.new_wig)
                    except ValueError:
                        print("E: the note was not on the list")
                    print("is a note")
                widget.new_wig.destroy()
            widget.new_wig.update()
        except AttributeError:
            widget = event.widget
            if widget.master.winfo_x() <= -10 or widget.master.winfo_y() <= 15:
                if isinstance(widget.master, wig.board):
                    try:
                        self.boards.remove(widget.master)
                        self.board_frames.remove(widget.master.board_frame)
                        widget.master.board_frame.destroy()
                    except ValueError:
                        print("E: the board was not on the list")
                    print("is a board")
                elif isinstance(widget.master, wig.note):
                    try:
                        self.notes.remove(widget.master)
                    except ValueError:
                        print("E: the note was not on the list")
                    print("is a note")
                widget.master.destroy()
            

            elif isinstance(widget.master, wig.note):
                widget.master.on_anyPress(event)

            widget.master.update()

    # the function that handles the back to home action 06
    def back_to_home(self):
        for child in self.home_board.winfo_children():
            try:
                if child.ISMETHEFRAME == "Ya is me":
                    child.place_forget()
            except AttributeError:
                if child.master != self.home_board:
                    child.place_forget()
        # update the active_board variable
        self.active_board = self.home_board
        # get the Home_board button to is off state
        self.Home_board_btn.config(state=tk.DISABLED, cursor="")
        self.focused_on = self.home_board
        print("back home we go!")

    def loadImages(self):
        # get and resize the icon images for use
        board_img_raw = Image.open("images/board_images/icy_fish.png").resize((50, 50))
        add_board_btn_img_raw = Image.open("images/widgets/Dark/Tool_bar/boads.png").resize((50, 50))
        add_note_btn_img_raw = Image.open("images/widgets/Dark/Tool_bar/sticky-note_light.png").resize((50, 50))
        BPoint_list__btn_img_raw = Image.open("images/widgets/Dark/note/list-interface-symbol.png").resize((50, 50))
        resize_point_img_raw = Image.open("images/widgets/Dark/note/resize_point.png").resize((15, 15))
        
        # the image for the boards icon
        self.board_img = ImageTk.PhotoImage(board_img_raw)

        # main buttons
        # the image for the button that adds board
        self.add_board_btn_img = ImageTk.PhotoImage(add_board_btn_img_raw)
        # the image for the button that adds notes
        self.add_note_btn_img = ImageTk.PhotoImage(add_note_btn_img_raw)
        # ------------
        
        # note editor frame
        # the Image for the make bullet-point list button
        self.make_BPoint_list__btn_img = ImageTk.PhotoImage(BPoint_list__btn_img_raw)
        # -----------------

        # the image for the resize point in note
        self.resize_point_img = ImageTk.PhotoImage(resize_point_img_raw)


if __name__ == "__main__":
    main()