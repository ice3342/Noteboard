import tkinter as tk
import movement as move
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
        icon.bind("<Button-1>", move.on_drag_start)
        icon.bind("<B1-Motion>", move.on_drag_motion)

        name.bind("<Double-Button-1>", self.open)
        name.bind("<Button-1>", move.on_drag_start)
        name.bind("<B1-Motion>", move.on_drag_motion)
        name.bind("<KeyRelease>", self.on_release)
        name.bind("<Return>", self.on_enter)

        self.board_frame = tk.Frame(app.active_board, bg="#222222")
        app.board_frames.append(self.board_frame)
        self.board_frame.bind("<Button-1>", move.on_MoveBoard_start)
        self.board_frame.bind("<B1-Motion>", move.on_MoveBoard_motion)
        self.board_frame.ISMETHEFRAME = "Ya is me"
        self.board_frame.app = app

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
                if child.ISMETHEFRAME == "Ya is me":
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

        self.Text = tk.Text(self, wrap="word",
                       width=40, height=5,
                       bg="#222222", fg="#ffffff",
                       insertbackground="#ffffff",
                       state=tk.DISABLED,
                       highlightthickness = 0, highlightcolor="#000000")
        self.Text.grid(row=0, column=0, sticky="nswe")
        resize_point = tk.Label(self, image=app.resize_point_img,
                                highlightthickness = 0, bd = 0)
        resize_point.grid(row=0, column=0, sticky="se")

        # create the editor frame that can change the widget in different ways
        self.editor_frame = tk.Frame(app.ActiveWig_Frame, bg="#242424")

        # create and grid the add board btn
        make_BPoint_list_btn = tk.Label(self.editor_frame, image=app.make_BPoint_list__btn_img,
                                    bg="#222222", fg="#eeeeee",
                                    highlightthickness = 0, bd = 0,
                                    activebackground="#222222", activeforeground="#ffffff")
        make_BPoint_list_btn.grid(row=0, column=0, sticky="nw")
        make_BPoint_list_btn.bind("<Button-1>", self.make_BPoint_list)

        # the actions the Text and resize_point uses
        self.Text.bind("<Button-1>", self.on_click)
        self.Text.bind("<Double-Button-1>", self.except_text)
        self.Text.bind("<B1-Motion>", move.on_drag_motion)
        self.Text.bind("<FocusIn>", self.focus_handler)
        self.Text.bind("<FocusOut>", self.focus_handler)
        self.Text.bind("<KeyRelease>", self.on_anyPress)
        # if you want the mouse click for on_anyPress go to on_place_widget in main.py
        resize_point.bind("<Button-1>", self.on_click)
        resize_point.bind("<B1-Motion>", self.on_resizing)

        self.app = app

    def on_click(self, event):
        widget = event.widget
        # if it's the text part of the note
        if isinstance(widget, tk.Text) and self.app.focused_on != widget:
            move.on_drag_start(event)
        # if it's the resize_point of the note
        elif isinstance(widget, tk.Label):
            self.on_resizing_start(event)

    # handle resizing
    def on_resizing_start(self, event):
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

    def on_anyPress(self, event):
        text = event.widget

        pos1 = int(text.index("insert").split(".")[1])
        OneCharBack = text.get(text.index("insert -1c"))
        BPoint = "•"

        if event.keysym == "BackSpace":
            if OneCharBack == BPoint:
                text.delete("insert -1c", "insert")

        elif event.keysym == "Return":
            if BPoint in text.get("insert -1 line linestart", "insert -1 line lineend"):
                text.insert("insert", "• ")
                print("ent")

        elif event.keysym == "Left":
            if OneCharBack == BPoint:
                if text.index("insert").split(".")[0] != "1":
                    text.mark_set("insert", "insert -1 line lineend")
                else:
                    text.mark_set("insert", "insert +1c")

        elif event.keysym == "Right":
            # if there is a bullet point after insert
            if text.get(text.index("insert")) == BPoint:
                text.mark_set("insert", "insert +2c")

        elif event.keysym == "Up":
            # is the char before the insert a Bullet point 
            if OneCharBack == BPoint:
                # check if it's the fist line if not, move the insert +1
                if text.index("insert").split(".")[0] != "1":
                    text.mark_set("insert", "insert +1c")
                    # if not then move insert +2
                else:
                    text.mark_set("insert", "insert +2c")
            
            if text.get(text.index("insert")) == BPoint:
                if text.index("insert").split(".")[0] != "1":
                    text.mark_set("insert", "insert +2c")

        elif event.keysym == "Down":
            # is the char before the insert a Bullet point 
            if OneCharBack == BPoint:
                # check if it's the fist line if not, move the insert +1
                if text.index("insert").split(".")[0] != "1":
                    text.mark_set("insert", "insert +1c")
                    # if not then move insert +2
                else:
                    text.mark_set("insert", "insert +2c")
            
            if text.get(text.index("insert")) == BPoint:
                if text.index("insert").split(".")[0] != "1":
                    text.mark_set("insert", "insert +2c")

        # if left mouse is release
        elif event.num == 1:
            if BPoint in text.get("insert -1c", "insert +1c"):
                text.mark_set("insert", f"insert +{2 - pos1}c")
                return "break"

    def focus_handler(self, event):
        widget = event.widget
        if event.type == tk.EventType.FocusIn:
            widget.config(highlightcolor="#ffffff", highlightthickness = 2)
        
        elif event.type == tk.EventType.FocusOut:
            widget.config(highlightcolor="#000000", highlightthickness = 0, state=tk.DISABLED)
            print("OUT")

    def make_BPoint_list(self, event):
        BPoint = "•"
        # get the start and ene indexs of the selected in a tuple
        selected_range = self.Text.tag_ranges("sel")

        MakeBPointList = True
        
        # if there is a selection
        if selected_range:
            # create a list that contains all the new line character
            idxs = []
            # get the line to start from
            start = f"{str(selected_range[0]).split(".")[0]}.0"
            # the loop that will fill the idxs
            while True:
                # search for an index
                idx = self.Text.search("\n", start, stopindex=selected_range[1], regexp=True)
                # if there is no idx left break the loop 
                if not idx:
                    # append the last line in the selected_range becuse the last line didn't register
                    # as it didn't reach the new line character
                    idxs.append(str(selected_range[1]).split(".")[0])
                    break
                # append only the line of the index
                idxs.append(idx.split(".")[0])
                # advence the loop
                start = f"{idx}+1c"
            print(idxs)
            # for every indexed line check if it has a bullet point and keep track of time the loop happend
            for i, idx in enumerate(idxs):
                # get the first char in the indexed line
                start_char = self.Text.get(f"{idx}.0", f"{idx}.1")
                # check if it should make the bulletpoint list or delete it 
                if start_char == BPoint and i == 0:
                    MakeBPointList = False
                elif start_char != BPoint:
                    MakeBPointList = True
                print(MakeBPointList)
            # make the Bullet Point List
            if MakeBPointList == True:
                for idx in idxs:
                    # get the start two chars, if it is already a bullet skip it
                    StartOfLine = self.Text.get(f"{idx}.0", f"{idx}.2")
                    if StartOfLine != f"{BPoint} ":
                        self.Text.insert(f"{idx}.0", f"{BPoint} ")
            # if it should remove the bullet list
            else:
                for idx in idxs:
                    # get the start two chars, if it is a bullet delete it
                    StartOfLine = self.Text.get(f"{idx}.0", f"{idx}.2")
                    if StartOfLine == f"{BPoint} ":
                        self.Text.delete(f"{idx}.0", f"{idx}.2")
                print("it idi adad")

        # if there is no selection just add or remove the bullet point in the line
        elif BPoint in self.Text.get("insert linestart", "insert lineend"):
            self.Text.delete("insert linestart", "insert linestart +2c")
        elif BPoint not in self.Text.get("insert linestart", "insert lineend"):
            self.Text.insert("insert linestart", f"{BPoint} ")

    def except_text(self, event):
        self.Text.config(state=tk.NORMAL)

