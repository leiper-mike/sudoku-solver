from cell import Cell

class Board():
     def __init__(self, x, y, cellSizeX, cellSizeY, win, lineColor = "black"):
          self.x = x
          self.y = y
          self.window = win
          self.cellSizeX = cellSizeX
          self.cellSizeY = cellSizeY
          self.lineColor = lineColor
          self.cells = []
          for i in range(0,9):
               self.cells.append([])
               self.cells[i] = [0 for x in range(0,9)]
     def draw(self):
          for i in range(0,9):
               y1 = self.y + (self.cellSizeY * i)
               for j in range(0,9):
                    x1 = self.x + (self.cellSizeX * j)
                    x2 = x1+self.cellSizeX
                    y2 = y1+self.cellSizeY
                    #makes lines thicker to delineate boxes and edge of board
                    # top line
                    if i == 0 or i == 3 or i == 6:
                         self.window.canvas.create_line(x1,y1,x2,y1,fill=self.lineColor,width=4)
                    else:
                         self.window.canvas.create_line(x1,y1,x2,y1,fill=self.lineColor,width=2)
                    #bottom line
                    if i == 8:
                         self.window.canvas.create_line(x2,y2,x1,y2,fill=self.lineColor,width=4)
                    else:
                         self.window.canvas.create_line(x2,y2,x1,y2,fill=self.lineColor,width=2)
                    #left line
                    if j == 0 or j == 3 or j == 6:
                         self.window.canvas.create_line(x1,y2,x1,y1,fill=self.lineColor,width=4)
                    else:
                         self.window.canvas.create_line(x1,y2,x1,y1,fill=self.lineColor,width=2)
                    #right line
                    if j == 8:
                         self.window.canvas.create_line(x2,y1,x2,y2,fill=self.lineColor,width=4)
                    else:
                         self.window.canvas.create_line(x2,y1,x2,y2,fill=self.lineColor,width=2)
                   
                    
                    
                    
     