field = list(range(1, 10))


def WinCheck(field):
    winning_set = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in winning_set:
        if field[each[0]] == field[each[1]] == field[each[2]]:
            return (field[each[0]] + " Победил!")
    return False


def PlayerTurn(player_token):
    valid_input = False

    while not valid_input:
        player_input = input("Каков ход для " + player_token + "?(Номер ячейки) ")

        try:
            player_input = int(player_input)
        except:
            print("Введен не номер ячейки")
            continue
            
        if player_input >= 1 and player_input <= 9:
            if str(field[player_input - 1]) not in "XO":
                field[player_input - 1] = player_token
                valid_input = True
            else:
                print("Поле уже занято")
        else:
            print("Нет такой ячейки")


def DrawField(field):
    print("-------------")
    for i in range(3):
        print("|", field[0 + i*3], "|", field[1 + i*3],
         "|", field[2 + i*3], "|")
        print("-------------")


def GameManager(field):
    moves_count = 0
    is_gameOver = False

    while not is_gameOver:
        DrawField(field)

        if (moves_count % 2 == 0):
            PlayerTurn("X")
        else: 
            PlayerTurn("O")
        
        moves_count += 1

        if moves_count > 4:
            game_status = WinCheck(field)

            if game_status:
                DrawField(field)
                print(game_status)
                is_gameOver = True
                break

        if (moves_count == 9):
            print("Ничья!")
            is_gameOver = True
            break



GameManager(field)