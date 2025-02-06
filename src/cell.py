class Cell():
     def __init__(self, p1, p2):
          self.p1 = p1
          self.p2 = p2
     def draw(self, canvas, fillColor):
          x1 = self.p1[0]
          y1 = self.p1[1]
          x2 = self.p2[0]
          y2 = self.p2[1]
          canvas.create_line(x1,y1,x2,y1,fill=fillColor,width=2)
          canvas.create_line(x2,y1,x2,y2,fill=fillColor,width=2)
          canvas.create_line(x2,y2,x1,y2,fill=fillColor,width=2)
          canvas.create_line(x1,y2,x1,y1,fill=fillColor,width=2)