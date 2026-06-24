import json
# the save funcions 08
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