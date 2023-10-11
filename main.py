"""
    This project is a terminal representation of a board game called XOBrainer
    in which a player is facing an AI-driven opponent utilizing Negamax algorithm
    from easyAI framework.

    Link to XOBrainer's instructions: https://xobrainer.com/images/pdf/XOBrainer_instructions_english_web.pdf

    To run this project on Windows make sure that you:
    - download the latest version of python,
    - download and install easyAI with the following command via cmd:
        "sudo pip install easyAI",
    - and launch the project from your favourite IDE

    Project created by:
        Kajetan Welc
        Daniel Wirzba
"""

from enum import Enum

from easyAI import AI_Player, Human_Player, Negamax, TwoPlayerGame

# game configuration
TABLE_WIDTH = 10
TABLE_HEIGHT = 10
WINNING_STRIKE = 5

# displaying game state
CELL_WIDTH = 5
GREEN_COLOR = '\033[32m'
PINK_COLOR = '\033[35m'
RESET_COLOR = '\033[m'


class Piece(Enum):
    """
        An enumerated class holding a numeric representation of all types of pieces
    """
    PINK_X = 1
    GREEN_X = 2
    PINK_O = 3
    GREEN_O = 4


# template holding list of player 1 pieces
PLAYER_1_PIECE_POOL = [
    Piece.PINK_O,
    Piece.PINK_O,
    Piece.PINK_O,
    Piece.GREEN_O
]

# template holding list of player 2 pieces
PLAYER_2_PIECE_POOL = [
    Piece.GREEN_X,
    Piece.GREEN_X,
    Piece.GREEN_X,
    Piece.PINK_X
]


class XOBrainer(TwoPlayerGame):
    """
        A class to represent the XOBrainer game.

        ...

        Attributes
        ----------
        players : list
            a list consisting of 2 easyAI classes
        table : list
            a two-dimensional list containing states of all the fields on the board
        player1_piece_pool : list
            a list containing player's 1 left to play pieces
        player2_piece_pool : list
            a list containing player's 2 left to play pieces

        Methods
        -------
        _build_winning_combinations:
            Method used to generate all possible winning combinations on the board.
        """
    def __init__(self, players):
        """
            Method used to initialize and construct the necessary attributes for the XOBrainer object.

            Parameters
            ----------
            players : list,
            Requires to have 2 easyAI classes passed in:
            - easyAI.Player.Human_Player    - which is a class for a human player, who gets asked by text what moves he
                                            wants to make
            - easyAI.Player.AI_Player       - which is a class for an AI player which must be initialized with an AI
                                            algorithm, like negamax

            Returns
            -------
            None
        """
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
        """
            Method used to generate all possible winning combinations on the board

            Parameters
            ----------
            self : instance of the class,

            Returns
            -------
            None
        """
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
        """
            Method used to generate all possible moves in the current analyzed state of the game

            Parameters
            ----------
            self : instance of the class,

            Returns
            -------
            moves: list of possible moves like: [P11, P43, G21, ...] etc.
            where the letter stands for piece's colour and the first and second digit
            stands accordingly for the board's row and the column.
        """
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
        """
            Method used to register the next move on the board.

            Parameters
            ----------
            self : instance of the class,
            move : str,
                a 3-char-long string defining the type and location of the next move,
                like P12, where the letter stands for piece's colour and the first and second digit
                stand accordingly for the row and the column on the board with values ranging from 0 to 9.

            Returns
            -------
            None
        """
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
        """
            Method used to register the next move on the board.

            Parameters
            ----------
            self : instance of the class,
            move : str,

            Returns
            -------
             False : Boolean value,
                if the game is determined not to be won after last player's move
             True : Boolean value,
                if the game is determined to be won after last player's move
        """
        wining_piece_groups = [
            [Piece.PINK_O, Piece.PINK_X],
            [Piece.PINK_O, Piece.GREEN_O],
        ] if self.current_player == 1 else [
            [Piece.GREEN_O, Piece.GREEN_X],
            [Piece.GREEN_X, Piece.PINK_X],
        ]

        for wining_pieces in wining_piece_groups:
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
        """
            Method used to determine if the game is over.

            Parameters
            ----------
            self : instance of the class,

            Returns
            -------
            a win() method execution returning either False or True
        """
        return self.win()

    def _print_piece(self, piece: Piece):
        """
            Method used to print a single piece

            Parameters
            ----------
            self : instance of the class,
            piece: Piece,
                one of player's left pieces to be printed

            Returns
            -------
            None
        """
        match piece:
            case Piece.PINK_X:
                print(PINK_COLOR + 'X', RESET_COLOR, end="")
            case Piece.GREEN_X:
                print(GREEN_COLOR + 'X', RESET_COLOR, end="")
            case Piece.PINK_O:
                print(PINK_COLOR + 'O', RESET_COLOR, end="")
            case Piece.GREEN_O:
                print(GREEN_COLOR + 'O', RESET_COLOR, end="")

    def show(self):
        """
            Method used to print the current state of game's board and each player's left pieces.

            Parameters
            ----------
            self : instance of the class,

            Returns
            -------
            None
        """
        print("GAME STATE:")

        print("Player 1 pieces: ", end="")
        for piece in self.player1_piece_pool:
            self._print_piece(piece)
        print()

        print("Player 2 pieces: ", end="")
        for piece in self.player2_piece_pool:
            self._print_piece(piece)
        print()

        print("-" * CELL_WIDTH * TABLE_WIDTH)
        for i in range(TABLE_WIDTH):
            print("|", end="")
            for j in range(TABLE_HEIGHT):
                symbol = self.table[i][j]

                print(' ', end="")

                if symbol == None:
                    print('  ', end="")
                else:
                    self._print_piece(symbol)

                if j == TABLE_HEIGHT - 1:
                    print(" |")
                else:
                    print(" |", end="")

        print("-" * CELL_WIDTH * TABLE_WIDTH)

    def scoring(self):
        """
            A method used by the AI when determining next best move.

            Parameters
            ----------
            self : instance of the class,

            Returns
            -------
            100: int,
                if the move ends with a win
            0: int
                if the move does not end with a win
        """
        return 100 if self.win() else 0


ai = Negamax(2)
game = XOBrainer([Human_Player(), AI_Player(ai)])
history = game.play()
