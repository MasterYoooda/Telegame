import bot
from transitions import Machine
#Игра ждет ввода пользователя только в PlayerTurn.

class Person(object):
    pass

def win_check(field):
    winning_set = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in winning_set:
        if field[each[0]] == field[each[1]] == field[each[2]]:
            return (field[each[0]] + " Победил!")
    return False


def player_turn(player_token, field):
    valid_input = False

    while not valid_input:

        player_input = 1 #bot.GetPlayerTurn('') #ждет номер ячейки
            
        if player_input >= 1 and player_input <= 9:
            if str(field[player_input - 1]) not in "XO":
                field[player_input - 1] = player_token
                valid_input = True
            else:
                pass
                # bot.SendMessage("Поле уже занято!")
        else:
            pass
            # bot.SendMessage("Нет такой ячейки!")


def draw_field(field):
    field_representation = "-------------"
    for i in range(3):
        field_representation += "\n| {} | {} | {} |\n".format(field[0 + i*3], field[1 + i*3], field[2 + i*3])
        field_representation += "-------------"
    
    # bot.SendMessage(field_representation)


def game_manager():
    field = list(range(1,10))
    moves_count = 0
    file_manager("write", field)
    is_gameOver = False

    while not is_gameOver:
        draw_field(field)

        if (moves_count % 2 == 0):
            player_turn("X", field)
        else: 
            player_turn("O", field)
        
        moves_count += 1

        if moves_count > 4:
            game_status = win_check(field)

            if game_status:
                draw_field(field)
                # bot.SendMessage(game_status)
                is_gameOver = True
                break

        if (moves_count >= 9):
            # bot.SendMessage("Ничья!")
            is_gameOver = True
            break


def file_manager(op, data):
    if (op == "write"):
        file = open("game_data.txt", 'w')

        for d in data:
            file.write(str(d) + " ")

        file.close()

    return 0

game_manager()