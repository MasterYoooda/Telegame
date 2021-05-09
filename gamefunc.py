import gamemanager
import botfunc
import random


class Field:
    fieldMap:list
    point_positions = {
        '0' : (110,110),
        '1' : (320,110),
        '2' : (530, 100),
        '3' : (110,320),
        '4' : (320,320),
        '5' : (530,320),
        '6' : (110,530),
        '7' : (320,530),
        '8' : (530,530)
    }


    def __init__(self):
        self.fieldMap = list(range(0,9))
        #self.fileManager('write')


    def fileManager(self, op):
        if (op == "write"):
            file = open("game_data.txt", 'w')

            for d in self.fieldMap:
                file.write(str(d) + " ")
            file.close()

        if (op == "read"):
            file = open("game_data.txt", 'r')
            field = file.readline().split(' ')
            field.pop(len(field) - 1)#  удаление лишнего пробела
            file.close()
            return field   
        return 0


class Player:
    token = None
    character = ''

    def __init__(self, token, character):
        self.token = token 
        self.character = character


class GameBot(Player):
    token = 0

    def __init__(self, character:str):
        self.character = character


    def makeMove(self):
        #  well, this is temporary
        return random.randint(0,8)
    

class Game:
    field:Field
    game_mode = None
    players_list = {'X':Player, 'O':Player}

    def startGame(self):
        self.field = Field()


    def playerTurn(self, cell_number:int, character:str):        
        if str(self.field.fieldMap[cell_number]) not in "XO":
                self.field.fieldMap[cell_number] = character
                #self.field.fileManager("write")
        else:
            raise gamemanager.GameExceptions('Ячейка занята!')


    def botTurn(self, character:str):
        is_rightmove, turn = False, 0

        while (not is_rightmove):
            turn = self.players_list[character].makeMove()
            try:
                self.playerTurn(turn, character)
            except gamemanager.GameExceptions as g_exc:
                pass
            else:
                is_rightmove = True
        return str(turn)  #  возвращает текстовый ключ из словаря клеток 


    def winCheck(self):
        field = self.field.fieldMap
        winning_set = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))    

        for each in winning_set:
            if field[each[0]] == field[each[1]] == field[each[2]]:
                raise gamemanager.GameExceptions(field[each[0]] + " Победил!")

        if (len(frozenset(field)) == 2):
            raise gamemanager.GameExceptions("Ничья!")


#---------------

def win_check():
    field = botfunc.game.field.fieldMap
    winning_set = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))    

    for each in winning_set:
        if field[each[0]] == field[each[1]] == field[each[2]]:
            return (field[each[0]] + " Победил!")

    if (len(frozenset(field)) == 2):
        return "Ничья!"
                
    return False


def bot_turn(point_positions_keys, token):
    is_suitable = False
    turn = 0
    while (not is_suitable):
        turn =  random.randint(0,8)
        #  путаница с bool: для одного False - хорошо, для другого - плохо
        #<- Сделать отдельно обработку исключений и bool переменных 🧐? 
        is_suitable = not player_turn(turn, token)
    return point_positions_keys[turn]  #  возвращает текстовый ключ из словаря клеток 


def player_turn(cell_number, token):        
    field = gamemanager.file_manager("read")

    if str(field[cell_number]) not in "XO":
            field[cell_number] = token
            gamemanager.file_manager("write", field)
            return 0
    else:
        return "error" #<- в будущем надо заменить на класс исключений


def start_game():
    field = list(range(1,10))
    gamemanager.file_manager("write", field)