import tkinter as tk
import widgets as wig

# handle dragging for the classes 04
def on_drag_start(event):
    widget = event.widget
    app = widget.master.app
    app.update_idletasks()
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    app.focused_on = widget.master
    widget.focused_note = True if isinstance(app.focus_get().master, wig.note) and app.focus_get()["state"] == tk.NORMAL else False
    widget.focus_set()
    
    print("yaa you got me ^_^")

    outOfBounds = app.winfo_geometry().split("+")[0]
    widget.bouds_x, widget.bouds_y =  (int(x) for x in outOfBounds.split("x"))
    print(widget.bouds_x, widget.bouds_y)

    app.Activate_ActiveWig_Frame()

def on_drag_motion(event):
    widget = event.widget
    app = widget.master.app
    # the action draging nad the max and min values that x and y can be which is set to the border of the frame  
    if widget.master.winfo_x() + app.home_board.winfo_x() - widget._drag_start_x + event.x < widget.bouds_x - 50 and widget.focused_note == False:
        x = max(widget.master.winfo_x() - widget._drag_start_x + event.x, -50)
        if widget.master.winfo_y() + app.home_board.winfo_y() - widget._drag_start_y + event.y < widget.bouds_y - 50:
            y = max(widget.master.winfo_y() - widget._drag_start_y + event.y, 15)
            # place the widget
            widget.master.place(x=x, y=y)
# ----------------

# handle the moving and expending of the board 07
def on_MoveBoard_start(event):
    print("yaa you got me ^_^")
    widget = event.widget
    app = widget.app
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    app.focused_on = widget
    widget.focus_set()

    for child in widget.children.values():
        right = child.winfo_x() + child.winfo_width()
        bottom = child.winfo_y() + child.winfo_height()

        big = 100
        small_x = right + widget.winfo_x() + app.max_board_movement
        small_y = bottom + widget.winfo_y() + app.max_board_movement
        if (small_x >= big or small_y >= big) and (widget.winfo_x() == app.max_board_movement or widget.winfo_y() == app.max_board_movement):
            app.max_board_movement -= 250
            widget.place(width = widget.winfo_width() + 250, height = widget.winfo_height() + 250)
            print("time to grow")
            print(app.max_board_movement)
            break
    
    app.Activate_ActiveWig_Frame()

    print(f"D: X={widget._drag_start_x}")
    print(f"D: Y={widget._drag_start_y}")

def on_MoveBoard_motion(event):
    widget = event.widget
    app = widget.app
    # the action draging nad the max and min values that x and y can be which is set to the border of the frame
    x = max(min(widget.winfo_x() - widget._drag_start_x + event.x, 0), app.max_board_movement)
    print(f"D:X-{x}")
    y = max(min(widget.winfo_y() - widget._drag_start_y + event.y, 0), app.max_board_movement)
    print(f"D:Y-{y}")
    # place and extend the board
    widget.place(x=x, y=y)
# ----------------