import tkinter as tk

class RegionSelectorUI:
    def __init__(self, window_x, window_y):
        """Initializes the region selector relative to the iPhone Mirroring window."""
        self.window_x = window_x  # ✅ Store iPhone Mirroring window X
        self.window_y = window_y  # ✅ Store iPhone Mirroring window Y

        self.root = tk.Tk()
        self.root.title("Region Selector")
        self.root.attributes("-topmost", True)  # ✅ Always on top
        self.root.geometry("300x200+100+100")  # ✅ Default size and position
        self.root.configure(bg="gray")

        self.label = tk.Label(self.root, text="Move & Resize the window.\nPress ENTER to confirm.",
                              bg="gray", fg="white", font=("Arial", 12))
        self.label.pack(expand=True, fill=tk.BOTH)

        # ✅ Track window movement & resizing
        self.root.bind("<Configure>", self.update_position)
        self.root.bind("<Return>", self.confirm_selection)  # ✅ Press ENTER to confirm selection

        print("🟢 Move & Resize over the iPhone Mirroring window.\nPress ENTER to confirm.")
        self.root.mainloop()  # ✅ Start the Tkinter main loop

    def update_position(self, event=None):
        """Gets the window's position and size when moved or resized, relative to the iPhone window."""
        self.absolute_x = self.root.winfo_x()
        self.absolute_y = self.root.winfo_y()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

        # ✅ Calculate relative coordinates
        self.relative_x = self.absolute_x - self.window_x
        self.relative_y = self.absolute_y - self.window_y

        print(f"🔵 Moving Window: X={self.absolute_x}, Y={self.absolute_y}, Width={self.width}, Height={self.height}")
        print(f"📏 Relative to iPhone Mirroring: X={self.relative_x}, Y={self.relative_y}, Width={self.width}, Height={self.height}")

    def confirm_selection(self, event=None):
        """Prints the final relative selection and closes the window."""
        print(f"✅ Final Selection (Relative to iPhone Mirroring): X={self.relative_x}, Y={self.relative_y}, Width={self.width}, Height={self.height}")
        self.root.destroy()

def select_region(window_x, window_y):
    """Launches the UI overlay to select a region relative to iPhone Mirroring window."""
    RegionSelectorUI(window_x, window_y)

if __name__ == "__main__":
    # Test Run: Replace with actual values from get_window_bounds()
    select_region(1173, 243)  # Example window position (Replace with real data)
