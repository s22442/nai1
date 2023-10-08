from enum import Enum

from easyAI import AI_Player, Human_Player, Negamax, TwoPlayerGame

TABLE_WIDTH = 10
TABLE_HEIGHT = 10
CELL_WIDTH = 5
WINNING_STRIKE = 5

GREEN = '\033[32m'  # Green Text
PINK = '\033[35m'  # Pink Text
ENDC = '\033[m'  # reset to the defaults


class Piece(Enum):
    PINK_X = 1
    GREEN_X = 2
    PINK_O = 3
    GREEN_O = 4


PLAYER_1_PIECE_POOL = [
    Piece.PINK_O,
    Piece.PINK_O,
    Piece.PINK_O,
    Piece.GREEN_O
]

PLAYER_2_PIECE_POOL = [
    Piece.GREEN_X,
    Piece.GREEN_X,
    Piece.GREEN_X,
    Piece.PINK_X
]


class XOBrainer(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.current_player = 1
        self.table = [
            [None for _ in range(TABLE_HEIGHT)]
            for _ in range(TABLE_WIDTH)
        ]
        self.player1_piece_pool = PLAYER_1_PIECE_POOL.copy()
        self.player2_piece_pool = PLAYER_2_PIECE_POOL.copy()

        self._build_winning_combinations()

    def _build_winning_combinations(self):
        self.winning_combinations = []

        # all horizontal combinations
        for i in range(TABLE_WIDTH - WINNING_STRIKE + 1):
            for j in range(TABLE_HEIGHT):
                self.winning_combinations.append(
                    [[i + k, j] for k in range(WINNING_STRIKE)]
                )

        # all vertical combinations
        for i in range(TABLE_WIDTH):
            for j in range(TABLE_HEIGHT - WINNING_STRIKE + 1):
                self.winning_combinations.append(
                    [[i, j + k] for k in range(WINNING_STRIKE)]
                )

        # all diagonal combinations
        for i in range(TABLE_WIDTH - WINNING_STRIKE + 1):
            for j in range(TABLE_HEIGHT - WINNING_STRIKE + 1):
                self.winning_combinations.append(
                    [[i + k, j + k] for k in range(WINNING_STRIKE)]
                )

        for i in range(WINNING_STRIKE, TABLE_WIDTH):
            for j in range(TABLE_HEIGHT - WINNING_STRIKE + 1):
                self.winning_combinations.append(
                    [[i - k, j + k] for k in range(WINNING_STRIKE)]
                )

        for i in range(TABLE_WIDTH - WINNING_STRIKE + 1):
            for j in range(WINNING_STRIKE, TABLE_HEIGHT):
                self.winning_combinations.append(
                    [[i + k, j - k] for k in range(WINNING_STRIKE)]
                )

        for i in range(WINNING_STRIKE, TABLE_WIDTH):
            for j in range(WINNING_STRIKE, TABLE_HEIGHT):
                self.winning_combinations.append(
                    [[i - k, j - k] for k in range(WINNING_STRIKE)]
                )

    def possible_moves(self):
        available_colors = []

        if self.current_player == 1:
            if self.player1_piece_pool.count(Piece.PINK_O):
                available_colors.append('P')
            if self.player1_piece_pool.count(Piece.GREEN_O):
                available_colors.append('G')
        else:
            if self.player2_piece_pool.count(Piece.PINK_X):
                available_colors.append('P')
            if self.player2_piece_pool.count(Piece.GREEN_X):
                available_colors.append('G')

        moves = []

        for i in range(TABLE_WIDTH):
            for j in range(TABLE_HEIGHT):
                if not self.table[i][j]:
                    for color in available_colors:
                        moves.append(f'{color}{i}{j}')

        return moves

    def make_move(self, move):
        color = move[0]
        i = int(move[1])
        j = int(move[2])

        piece = (
            Piece.PINK_O if color == 'P' else Piece.GREEN_O
        ) if self.current_player == 1 else (
            Piece.PINK_X if color == 'P' else Piece.GREEN_X
        )

        self.table[i][j] = piece

        pool = self.player1_piece_pool if self.current_player == 1 else self.player2_piece_pool
        pool.remove(piece)

        if len(pool) == 0:
            if self.current_player == 1:
                self.player1_piece_pool = PLAYER_1_PIECE_POOL.copy()
            else:
                self.player2_piece_pool = PLAYER_2_PIECE_POOL.copy()

    def win(self):
        wining_pieces = [
            Piece.PINK_O, Piece.PINK_X
        ] if self.current_player == 1 else [
            Piece.GREEN_O, Piece.GREEN_X
        ]

        for combination in self.winning_combinations:
            win = True
            for pos in combination:
                if self.table[pos[0]][pos[1]] not in wining_pieces:
                    win = False
                    break

            if win:
                return True

        return False

    def is_over(self):
        return self.win()

    def show(self):
        print("GAME STATE:")
        print("-" * CELL_WIDTH * TABLE_WIDTH)
        for i in range(TABLE_WIDTH):
            print("|", end="")
            for j in range(TABLE_HEIGHT):
                symbol = self.table[i][j]
                if symbol == Piece.PINK_X:
                    print(PINK + ' X', ENDC, end="")
                elif symbol == Piece.GREEN_X:
                    print(GREEN + ' X', ENDC, end="")
                elif symbol == Piece.PINK_O:
                    print(PINK + ' O', ENDC, end="")
                elif symbol == Piece.GREEN_O:
                    print(GREEN + ' O', ENDC, end="")
                else:
                    print('   ', end="")

                if j == TABLE_HEIGHT - 1:
                    print(" |")
                else:
                    print(" |", end="")

        print("-" * CELL_WIDTH * TABLE_WIDTH)

    def scoring(self):
        return 100 if self.win() else 0


ai = Negamax(2)
game = XOBrainer([Human_Player(), AI_Player(ai)])
history = game.play()
