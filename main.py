class MiniTicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.winner = None

    def make_move(self, row, col, player):
        if self.winner or self.board[row][col] != ' ':
            return False
        self.board[row][col] = player
        self.check_winner(player)
        return True

    def check_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                self.winner = player
                return
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                self.winner = player
                return
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            self.winner = player
            return
        if all(self.board[i][2-i] == player for i in range(3)):
            self.winner = player
            return
        # Check for draw
        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            self.winner = 'Draw'

    def is_full(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

class UltimateTicTacToe:
    def __init__(self):
        self.board = [[MiniTicTacToe() for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.last_move = None
        self.winner = None

    def print_board(self):
        for i in range(3):
            for row in range(3):
                line = ''
                for j in range(3):
                    mini = self.board[i][j]
                    if mini.winner and mini.winner != 'Draw':
                        line += f' {mini.winner * 3} |'
                    else:
                        line += ' ' + ''.join(mini.board[row]) + ' |'
                print(line[:-1])  # Remove trailing '|'
                if row < 2:
                    print('-' * 13)
            if i < 2:
                print('=' * 13)

    def make_move(self, big_row, big_col, small_row, small_col):
        if self.winner:
            return False
        
        mini_board = self.board[big_row][big_col]
        if mini_board.winner:  # If mini-board is already won
            return False
        
        if not mini_board.make_move(small_row, small_col, self.current_player):
            return False

        self.last_move = (small_row, small_col)
        self.check_big_winner()
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_big_winner(self):
        # Check rows
        for row in range(3):
            if all(self.board[row][col].winner == self.current_player for col in range(3)):
                self.winner = self.current_player
                return
        # Check columns
        for col in range(3):
            if all(self.board[row][col].winner == self.current_player for row in range(3)):
                self.winner = self.current_player
                return
        # Check diagonals
        if all(self.board[i][i].winner == self.current_player for i in range(3)):
            self.winner = self.current_player
            return
        if all(self.board[i][2-i].winner == self.current_player for i in range(3)):
            self.winner = self.current_player
            return

    def play(self):
        print("Welcome to Ultimate Tic-Tac-Toe!")
        print("Format: big_row,big_col,small_row,small_col (0-2 each)")
        
        while not self.winner:
            self.print_board()
            print(f"Player {self.current_player}'s turn")
            
            if self.last_move and not self.board[self.last_move[0]][self.last_move[1]].winner:
                print(f"Must play in mini-board at {self.last_move}")
                target_row, target_col = self.last_move
            else:
                print("Can play in any mini-board")
                target_row, target_col = None, None

            while True:
                move = input("Enter move: ").split(',')
                if len(move) != 4:
                    print("Invalid format! Use: big_row,big_col,small_row,small_col")
                    continue
                
                try:
                    big_row, big_col, small_row, small_col = map(int, move)
                    if not all(0 <= x <= 2 for x in [big_row, big_col, small_row, small_col]):
                        raise ValueError
                    
                    # Check if move is in valid mini-board based on last move
                    if target_row is not None and (big_row != target_row or big_col != target_col):
                        print(f"Must play in mini-board at {self.last_move}")
                        continue
                    
                    if self.make_move(big_row, big_col, small_row, small_col):
                        break
                    else:
                        print("Invalid move! Space taken or mini-board already won.")
                except ValueError:
                    print("Invalid input! Use numbers 0-2")

        self.print_board()
        print(f"Player {self.winner} wins!" if self.winner else "Game ended in a draw!")

if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.play()