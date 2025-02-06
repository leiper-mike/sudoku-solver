from tkinter import Tk, BOTH, Canvas

class Window():
     def __init__(self, w, h):
          self.width = w
          self.height = h
          self.root = Tk()
          self.root.title = "Maze Solver"
          self.root.protocol("WM_DELETE_WINDOW", self.close)
          self.root.geometry(f"{w}x{h}")
          self.canvas = Canvas(width=w, height=h)
          self.canvas.pack()
          self.running = False
     def redraw(self):
          self.root.update_idletasks()
          self.root.update()
     def wait_for_close(self):
          self.running = True
          while self.running:
               self.redraw()
     def close(self):
          self.running = False