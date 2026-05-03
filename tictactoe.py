from logging import fatal
from urllib.parse import uses_query

board = [' ',' ',' ',' ',
         ' ',' ',' ',' ',
         ' ',' ',' ',' ']

current_player = 'X'


def print_board():
    print(board[0], board[1], board[2], sep='|')
    print('-----')
    print(board[3], board[4], board[5], sep='|')
    print('-----')
    print(board[6], board[7], board[8], sep='|')
    print('-----')

def change_player():
    global current_player

    if current_player == 'X':
        current_player = 'O'
    else:
        current_player = 'X'

def is_win():
# ======================  Вертикаль
    if board[0] == board[1] == board[2] and board[0] != ' ':
        return True

    if board[3] == board[4] == board[5] and board[3] != ' ':
        return True

    if board[6] == board[7] == board[8] and board[6] != ' ':
        return True
#====================== Горизонталь
    if board[0] == board[3] == board[6] and board[0] != ' ':
        return True

    if board[1] == board[4] == board[7] and board[1] != ' ':
        return True

    if board[2] == board[5] == board[8] and board[2] != ' ':
        return True
# ====================== Діагональ
    if board[0] == board[4] == board[8] and board[0] != ' ':
        return True

    if board[2] == board[4] == board[6] and board[2] != ' ':
        return True

    return False


def game():
    while True:
        print_board()
        user_turn = int(input(f'[{current_player}] | Зробіть хід(1-9): '))

        if 1 <= user_turn <= 9 and board[user_turn - 1] == ' ':
            board[user_turn - 1] = current_player

            if  is_win():
                print_board()
                print(f'Переміг {current_player}')
                break

            if board.count(' ') == 0:
                print_board()
                print('нічія!')
                break

            change_player()

game()