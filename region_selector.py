import tkinter as tk
import pyautogui

class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)  # ✅ 30% Transparency
        self.root.attributes("-topmost", True)  # ✅ Force window to stay on top
        self.root.overrideredirect(True)  # ✅ Remove window borders
        self.root.geometry(f"{pyautogui.size()[0]}x{pyautogui.size()[1]}+0+0")  # ✅ Fullscreen overlay

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ✅ Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        print("🟢 Region Selector is running... Click and drag to select an area.")
        self.root.mainloop()  # ✅ Start the Tkinter main loop

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def on_drag(self, event):
        self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", width=2)

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        x, y = min(self.start_x, end_x), min(self.start_y, end_y)
        width, height = abs(self.start_x - end_x), abs(self.start_y - end_y)

        print(f"🟢 Selected Region: X={x}, Y={y}, Width={width}, Height={height}")
        self.root.destroy()  # ✅ Close the window after selection

def select_region():
    RegionSelector()  # ✅ Run the Region Selector

if __name__ == "__main__":
    select_region()
