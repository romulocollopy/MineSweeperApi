class Boom(Exception):
    """Custom exception for when a bomb is triggered"""

    def __init__(self, message: str, board):
        super().__init__(message)
        self.board = board
