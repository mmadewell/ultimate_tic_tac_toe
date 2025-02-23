import pygame

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
        for row in self.board:
            if all(cell == player for cell in row):
                self.winner = player
                return
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                self.winner = player
                return
        if all(self.board[i][i] == player for i in range(3)):
            self.winner = player
            return
        if all(self.board[i][2-i] == player for i in range(3)):
            self.winner = player
            return
        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            self.winner = 'Draw'

    def is_full(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

class UltimateTicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Ultimate Tic-Tac-Toe")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.board = [[MiniTicTacToe() for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.last_move = None
        self.winner = None
        self.cell_size = 200  # Size of each big cell
        self.mini_cell_size = self.cell_size // 3

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        
        # Draw main grid lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, 600), 4)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (600, i * self.cell_size), 4)

        # Draw mini grids and contents
        for big_row in range(3):
            for big_col in range(3):
                mini = self.board[big_row][big_col]
                x_offset = big_col * self.cell_size
                y_offset = big_row * self.cell_size

                # Highlight target mini-board
                if (self.last_move and not mini.winner and 
                    big_row == self.last_move[0] and big_col == self.last_move[1]):
                    pygame.draw.rect(self.screen, (200, 255, 200), 
                                   (x_offset, y_offset, self.cell_size, self.cell_size))

                # Draw mini grid lines
                for i in range(1, 3):
                    pygame.draw.line(self.screen, (150, 150, 150),
                                   (x_offset + i * self.mini_cell_size, y_offset),
                                   (x_offset + i * self.mini_cell_size, y_offset + self.cell_size), 2)
                    pygame.draw.line(self.screen, (150, 150, 150),
                                   (x_offset, y_offset + i * self.mini_cell_size),
                                   (x_offset + self.cell_size, y_offset + i * self.mini_cell_size), 2)

                # Draw contents
                if mini.winner and mini.winner != 'Draw':
                    text = self.font.render(mini.winner, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(x_offset + self.cell_size/2, 
                                                    y_offset + self.cell_size/2))
                    self.screen.blit(text, text_rect)
                else:
                    for row in range(3):
                        for col in range(3):
                            if mini.board[row][col] != ' ':
                                text = self.font.render(mini.board[row][col], True, (0, 0, 0))
                                text_rect = text.get_rect(center=(
                                    x_offset + col * self.mini_cell_size + self.mini_cell_size/2,
                                    y_offset + row * self.mini_cell_size + self.mini_cell_size/2))
                                self.screen.blit(text, text_rect)

        # Draw player turn
        turn_text = self.font.render(f"Player {self.current_player}'s turn", True, (0, 0, 0))
        self.screen.blit(turn_text, (10, 10))

        if self.winner:
            win_text = self.font.render(f"Player {self.winner} wins!", True, (255, 0, 0))
            win_rect = win_text.get_rect(center=(300, 300))
            self.screen.blit(win_text, win_rect)

    def make_move(self, big_row, big_col, small_row, small_col):
        if self.winner:
            return False
        
        # Check if move is in valid mini-board
        if (self.last_move and not self.board[self.last_move[0]][self.last_move[1]].winner and
            (big_row != self.last_move[0] or big_col != self.last_move[1])):
            return False

        mini_board = self.board[big_row][big_col]
        if mini_board.winner:
            return False
        
        if not mini_board.make_move(small_row, small_col, self.current_player):
            return False

        self.last_move = (small_row, small_col)
        self.check_big_winner()
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_big_winner(self):
        for row in range(3):
            if all(self.board[row][col].winner == self.current_player for col in range(3)):
                self.winner = self.current_player
                return
        for col in range(3):
            if all(self.board[row][col].winner == self.current_player for row in range(3)):
                self.winner = self.current_player
                return
        if all(self.board[i][i].winner == self.current_player for i in range(3)):
            self.winner = self.current_player
            return
        if all(self.board[i][2-i].winner == self.current_player for i in range(3)):
            self.winner = self.current_player
            return

    def get_click_position(self, pos):
        big_row = pos[1] // self.cell_size
        big_col = pos[0] // self.cell_size
        small_row = (pos[1] % self.cell_size) // self.mini_cell_size
        small_col = (pos[0] % self.cell_size) // self.mini_cell_size
        return big_row, big_col, small_row, small_col

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
                    pos = pygame.mouse.get_pos()
                    big_row, big_col, small_row, small_col = self.get_click_position(pos)
                    self.make_move(big_row, big_col, small_row, small_col)

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.play()