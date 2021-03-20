import bot


def WinCheck(field):
    winning_set = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in winning_set:
        if field[each[0]] == field[each[1]] == field[each[2]]:
            return (field[each[0]] + " Победил!")
    return False


def PlayerTurn(player_token, field):
    valid_input = False

    while not valid_input:
        bot.SendMessage("Каков ход для " + player_token + "?(Номер ячейки)")
        player_input = bot.GetPlayerTurn('')
            
        if player_input >= 1 and player_input <= 9:
            if str(field[player_input - 1]) not in "XO":
                field[player_input - 1] = player_token
                valid_input = True
            else:
                bot.SendMessage("Поле уже занято")
        else:
            bot.SendMessage("Нет такой ячейки")


def DrawField(field):
    field_representation = "-------------"
    for i in range(3):
        field_representation += "\n| {} | {} | {} |\n".format(field[0 + i*3], field[1 + i*3], field[2 + i*3])
        field_representation += "-------------"
    
    bot.SendMessage(field_representation)


def GameManager():
    field = list(range(1,10))
    moves_count = 0
    is_gameOver = False

    while not is_gameOver:
        DrawField(field)

        if (moves_count % 2 == 0):
            PlayerTurn("X", field)
        else: 
            PlayerTurn("O", field)
        
        moves_count += 1

        if moves_count > 4:
            game_status = WinCheck(field)

            if game_status:
                DrawField(field)
                bot.SendMessage(game_status)
                is_gameOver = True
                break

        if (moves_count >= 9):
            bot.SendMessage("Ничья!")
            is_gameOver = True
            break


# GameManager(field)