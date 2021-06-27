import math
from PIL import Image, ImageDraw
from abc import ABC, abstractmethod

point_positions = {
        0 : (110,110),
        1 : (320,110),
        2 : (530,110),
        3 : (110,320),
        4 : (320,320),
        5 : (530,320),
        6 : (110,530),
        7 : (320,530),
        8 : (530,530)
    }

class Figure(ABC):
    @abstractmethod
    def __call__(self):
        pass

class ImageMake():
    
    def image_draw(self,coors):
        for i in range(len(coors)):
            if coors[i] == 'X':
                cross(point_positions[i])
            if coors[i] == 'O':
                circle(point_positions[i])

    def winline_draw(self,win_coors):
        im = Image.open('pol2.jpg')
        draw = ImageDraw.Draw(im)
        draw.line(
            xy=(win_coors[0],win_coors[1],win_coors[2],win_coors[3]),
            fill="red",
            width=10
        )
        im.save('pol2.jpg', quality=200)   



class Circle(Figure):
    def __call__(self, point:list): 
        x, y = point[0], point[1]

        r = 100

        try:
            im = Image.open('pol2.jpg')
        except:
            im = Image.open('pol.jpg')

        draw = ImageDraw.Draw(im)

        draw.ellipse(
            xy=(x-r/math.sqrt(2),y-r/math.sqrt(2),x+r/math.sqrt(2),y+r/math.sqrt(2)),
            fill="white",
            outline="black",
            width=10
        )
        im.save('pol2.jpg', quality=200)


class Cross(Figure):
    def __call__(self, point:list):
        x, y = point[0], point[1]

        try:
            im = Image.open('pol2.jpg')
        except:
            im = Image.open('pol.jpg')

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

        im.save('pol2.jpg', quality=200) 


# class WinLine():
#     def __call__(self, line:list):
#         x1,y1,x2,y2 = line[0], line[1], line[2], line[3]
#         im = Image.open('pol2.jpg')
#         draw = ImageDraw.Draw(im)
#         draw.line(
#             xy=(x1,y1,x2,y2),
#             fill="red",
#             width=10
#         )
#         im.save('pol2.jpg', quality=200)   





circle = Circle()
#circle([110,110])
cross = Cross()
# cross([320,110])
# circle([110,110])
# cross((320,110))
# cross((320,320))
# cross((320,530))
# winline = WinLine()
# winline(320,25,320,615)



# ImageMake().image_draw(['X','X','X','X','X','X','X','X','X'])
# ImageMake().winline_draw((25,110,615,110))
