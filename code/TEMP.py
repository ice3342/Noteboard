import tkinter as tk

def on_anyPress(event):
    text = event.widget

    pos1 = int(text.index("insert").split(".")[1])
    OneCharBack = text.get(text.index("insert -1c"))
    BPoint = "•"

    if event.keysym == "BackSpace":
        if OneCharBack == BPoint:
            text.delete("insert -1c", "insert")

    elif event.keysym == "Return":
        if BPoint in text.get("insert -1 line linestart", "insert -1 line lineend"):
            txt.insert("insert", "• ")
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

root = tk.Tk()

txt = tk.Text(root)
txt.pack()

txt.insert("end", "• Item 1\n• Item 2\n")

txt.bind("<KeyRelease>", on_anyPress)
txt.bind("<ButtonRelease-1>", on_anyPress)
root.mainloop()