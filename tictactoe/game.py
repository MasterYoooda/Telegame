from tictactoe.field import Field
from tictactoe.testimages import MakeImage
from abc import ABC, abstractmethod

class Game(ABC):
    # An indicator, whose turn
    _active_char = 'X'

    def __init__(self) -> None:
        self._field:Field = None
        self._char = None

    def set_field(self, field:Field):
        self._field = field

    @abstractmethod
    def set_char(self, char:str, player) -> None:
        self._char = char
        # self._players[char] = player

    @abstractmethod
    def move_processor(self):
        pass

    def update_map(self, cell_num:int, char:str) -> str:
        if str(self._field.get()[cell_num]) not in "XO":
            self._field.update_map(cell_num, char)
            return 'Успешно'
        else:
            return 'Ячейка занята'

    def check_win(self) -> str|None:
        field = self._field.get()
        win_set = list(self._field.get_winnig_set().keys())
        for each in win_set:
            if field[each[0]] == field[each[1]] == field[each[2]]:
                MakeImage().winline_draw(self._field.get(),
                                         Field.get_winnig_set()[each],
                                         Field.coords())
                return str(field[each[0]]+'Победил!')
        if len(frozenset(field)) == 2:
            return 'Ничья!'


class Single(Game):
    _game_mode = 'mode_single'

    def set_char(self, char: str, player) -> None:
        super().set_char(char, player)
        bot_char = 'XO'.replace(char, '')
        self.set_char(bot_char)

    def bot_move(self, char:str) -> str:
        is_moved, turn = False, 0
        # Bot tries to make a turn until it selects a free cell
        while not is_moved:
            turn = self._players[char].make_move()
            try:
                self.update_map(turn, char)
            except:
                pass
            else:
                is_moved = True
        return str(turn)

    def get_char(self, chat_id:str) -> str:
        if self._players['X'].get_chatId() != 0 and \
                self._players['X'].get_chatId() == chat_id:
            return 'X'
        else:
            return 'O'

    def move_processor(self, chat_id:str, cell_num=0) -> str|None:
        if self._active_char == self.get_char(chat_id):
            cell_occupied = self.update_map(cell_num, self.get_char(chat_id))
            if cell_occupied:
                return cell_occupied
        else:
            self.bot_move(self._active_char)
        win = self.check_win()
        if win:
            return win       
        # Change a turn of the move
        self._active_char = 'XO'.replace(self._active_char, '')
        # If it's the bot's turn - calls for it
        if self._active_char != self.get_char(chat_id):
            move = self.move_processor(chat_id, cell_num)
            if move:
                return move
        else:
            # if there're no moves of the real man(O) yet, there's no message to edit
            if not self._active_char in self._field.get_field():
                return
        return 'Ход выполнен!'