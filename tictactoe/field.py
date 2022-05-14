from attr import field
# from controller.fielddrawer import MakeImage
from controller.exceptions import *

class Field:
    _fieldMap:list
    _point_positions = {
        '0' : (110,110),
        '1' : (320,110),
        '2' : (530, 110),
        '3' : (110,320),
        '4' : (320,320),
        '5' : (530,320),
        '6' : (110,530),
        '7' : (320,530),
        '8' : (530,530)
    }
    _winning_set = {
        (0,1,2) : (25,110,615,110),
        (3,4,5) : (25,320,615,320),
        (6,7,8) : (25,530,615,530),
        (0,3,6) : (110,25,110,615),
        (1,4,7) : (320,25,320,615),
        (2,5,8) : (530,25,530,615),
        (0,4,8) : (25,25,615,615),
        (2,4,6) : (615,25,25,615)
    }

    def __init__(self):
        self._fieldMap = list(range(0,9))

    def __call__() -> dict:
        return Field._point_positions
        
    def coords(self) -> dict:
        return self._point_positions

    def get(self) -> list:
        return self._fieldMap

    def get_winnig_set(self) -> dict:
        return self._winning_set

    def update_map(self, i:int, char:str) -> None:
        self._fieldMap[i] = char

    def field_status(self) -> Win|Draw|None:
        ws = self._winning_set.keys()
        for each in ws:
            if self._fieldMap[each[0]] == \
                    self._fieldMap[each[1]] == \
                    self._fieldMap[each[2]]:
                # MakeImage().winline_draw(
                #         self._fieldMap,
                #         self._winning_set[each],
                #         self.coords)
                raise Win(field[each[0]])
        if len(frozenset(self._fieldMap)) == 2:
            raise Draw()