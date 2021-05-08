import gamemanager
import random


def win_check():
    field = gamemanager.file_manager("read")
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