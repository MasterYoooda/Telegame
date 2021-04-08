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

    # if player_input >= 1 and player_input <= 9:
    #     if str(field[player_input - 1]) not in "XO":
    #         field[player_input - 1] = player_token
    #         valid_input = True
    #     else:
    #         pass
    #         # bot.SendMessage("Поле уже занято!")
    # else:
    #     pass
    #     # bot.SendMessage("Нет такой ячейки!")


# def draw_field(field):
#     field_representation = "-------------"
#     for i in range(3):
#         field_representation += "\n| {} | {} | {} |\n".format(field[0 + i*3], field[1 + i*3], field[2 + i*3])
#         field_representation += "-------------"    
    # bot.SendMessage(field_representation)


def start_game():
    field = list(range(1,10))
    gamemanager.file_manager("write", field)
    # while not is_gameOver:
    #     draw_field(field)

    #     if (moves_count % 2 == 0):
    #         player_turn("X", field)
    #     else: 
    #         player_turn("O", field)
        
    #     moves_count += 1

    #     if moves_count > 4:
    #         game_status = win_check(field)

    #         if game_status:
    #             draw_field(field)
    #             # bot.SendMessage(game_status)
    #             is_gameOver = True
    #             break

    #     if (moves_count >= 9):
    #         # bot.SendMessage("Ничья!")
    #         is_gameOver = True
    #         break



