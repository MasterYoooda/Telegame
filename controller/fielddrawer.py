import math
from PIL import Image, ImageDraw
from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def __call__(self):
        pass


class Circle(Figure):
    def __call__(self, point:list, im: Image): 
        x, y, r = point[0], point[1], 100
        # im = Image.open('pol2.jpg')
        draw = ImageDraw.Draw(im)
        draw.ellipse(
            xy=(x-r/math.sqrt(2),y-r/math.sqrt(2),x+r/math.sqrt(2),y+r/math.sqrt(2)),
            fill="white",
            outline="black",
            width=10
        )


class Cross(Figure):
    def __call__(self, point:list, im: Image):
        x, y = point[0], point[1]
        # im = Image.open('pol2.jpg')
        draw = ImageDraw.Draw(im)
        r = 100
        draw.line(
            xy=(x-r/math.sqrt(2),y-r/math.sqrt(2),x+r/math.sqrt(2),y+r/math.sqrt(2)),
            fill="black",
            width=10)
        draw.line(
            xy=(x+r/math.sqrt(2),y-r/math.sqrt(2),x-r/math.sqrt(2),y+r/math.sqrt(2)),
            fill="black",
            width=10)
        

class WinLine():
    def __call__(self, line:list, im: Image):
        x1,y1,x2,y2 = line[0], line[1], line[2], line[3]
        # im = Image.open('pol2.jpg')
        draw = ImageDraw.Draw(im)
        draw.line(
            xy=(x1,y1,x2,y2),
            fill="red",
            width=10
        )
        im.save('pol2.jpg', quality=200)   


class MakeImage:
    __cross = Cross()
    __circle = Circle()
    __winline = WinLine()

    def image_draw(self, coors: list, point_positions: dict, im: Image = None):
        if not im:
            im = Image.open('pol.jpg')
        for i in range(len(coors)):
            if coors[i] == 'X':
                self.__cross(point_positions[str(i)], im)
            if coors[i] == 'O':
                self.__circle(point_positions[str(i)], im)
        im.save('pol2.jpg', quality=200) 

    def winline_draw(self, coors: list, line: list, point_positions: dict):
        im = Image.open('pol.jpg')
        self.image_draw(coors, point_positions, im)
        self.__winline(line, im)


# circle = Circle()
#circle([110,110])
# cross = Cross()
# cross([320,110])
# circle([110,110])
# cross((320,110))
# cross((320,320))
# cross((320,530))
# winline = WinLine()
# winline(320,25,320,615)