from window import Window
from board import Board
def main():
     win = Window(800,600)
     board = Board(5,5,30,30,win)
     board.draw()
     win.wait_for_close()
main()
