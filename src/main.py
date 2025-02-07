from window import Window
from board import Board
from tkinter import Tk
def main():
     root = Tk()
     win = Window(800,600, root)
     board = Board(5,5,30,30,win.canvas)
     board.draw()
     root.mainloop()
main()
