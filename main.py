from enum import Enum

from easyAI import AI_Player, Human_Player, Negamax, TwoPlayerGame

TABLE_WIDTH = 10
TABLE_HEIGHT = 10


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
        self.nplayer = 1
        self.table = [[] for _ in range(TABLE_WIDTH)]
        self.player1_piece_pool = PLAYER_1_PIECE_POOL
        self.player2_piece_pool = PLAYER_2_PIECE_POOL

    def possible_moves(self):
        available_colors = []

        if self.nplayer == 1:
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
        color = int(move[0])
        i = int(move[1])
        j = int(move[2])

        piece = (
            Piece.PINK_O if color == 'P' else Piece.GREEN_O
        ) if self.nplayer == 1 else (
            Piece.PINK_X if color == 'P' else Piece.GREEN_X
        )

        self.table[i][j] = piece

    def win(self):
        wining_pieces = [
            Piece.PINK_O, Piece.PINK_X
        ] if self.nplayer == 1 else [
            Piece.GREEN_O, Piece.GREEN_X
        ]

        # TODO

        return True

    def is_over(self):
        return self.win()

    def show(self):
        # TODO
        pass

    def scoring(self):
        return 100 if self.win() else 0


ai = Negamax(13)
game = XOBrainer([Human_Player(), AI_Player(ai)])
history = game.play()
