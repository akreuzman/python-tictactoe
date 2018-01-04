#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
A one-player Python tic-tac-toe game using a minimax algorithm.

Author: Andrew Kreuzman
"""

import copy
import os
import time

class TicTacToe:
    """
    A Tic Tac Toe game with all necessary methods.

    Begin a new game by calling the static method: `play_tictactoe`
    """
    PLAYER_ONE = 0
    PLAYER_TWO = 1

    def __init__(self):
        """Initialize game variables."""        
        self.currentBoard = [' ']*9
        self.playerOneMoves = []
        self.playerTwoMoves = []
        self.allMoves = [] #both players moves listed together
        self.currentPlayer = TicTacToe.PLAYER_ONE #toggles between 0 and 1


    def get_num_moves(self):
        """Returns the number of moves that have been completed."""
        return len(self.allMoves)


    def get_available_moves(self):
        """Returns a list of available indices remaining."""
        availableMoves = [index for index, value in enumerate(self.currentBoard) if value == ' ']
        return availableMoves


    def print_board(self):
        """Clears terminal window and prints the game board."""
        # Clear terminal window (independent of operating system)
        os.system('cls' if os.name == 'nt' else 'clear') #no user passed strings (safe)
        # Print current board
        print('|{}|{}|{}|\n|{}|{}|{}|\n|{}|{}|{}|'.format(*self.currentBoard))


    def add_move(self, moveIndex: int):
        """
        Adds a move to the currentBoard at the given index. 

        Move type (x/o) is determined by the currentPlayer variable. 
        Alternates currentPlayer after adding move to the board.
        """
        # Append move to correct player's list
        if self.currentPlayer == TicTacToe.PLAYER_ONE:
            self.playerOneMoves.append(moveIndex)
            symbol = 'x'
        else:
            self.playerTwoMoves.append(moveIndex)
            symbol = 'o'

        # Add move to allMoves and the board
        self.allMoves.append(moveIndex)
        self.currentBoard[moveIndex] = symbol
        # Toggle current player
        self.currentPlayer = (self.currentPlayer+1)%2


    def check_win(self):
        """
        Checks if game is over, returns winner id and bool.

        `winner`: 0 for PLAYER_ONE, 1 for PLAYER_TWO, -1 for no winner
        `over`: True if game over, False if not
        """
        winningCombos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        winner = -1 #no winner
        over = (len(self.allMoves) == 9) #false unless 9 moves made

        # Loop through possible winning combinations
        for combo in winningCombos:

            # Check player one's moves
            if set(combo).issubset(self.playerOneMoves):
                winner, over = TicTacToe.PLAYER_ONE, True
            # Check player two's moves
            elif set(combo).issubset(self.playerTwoMoves):
                winner, over = TicTacToe.PLAYER_TWO, True

        return winner, over


    def get_player_move(self):
        """Get input from player and validate it against possible inputs."""
        validMove = False

        # User selection must be an int from 1-9
        while not validMove:
            # Get input
            try:
                playerMove = int(input())
            # Not an int
            except ValueError:
                print('That\'s not a number, try again.')
                continue
            else: #is an int
                availableMoves = self.get_available_moves()
                
                # Out of range of board
                if not playerMove in range(1,10): 
                    print('{} is out of range, try again.'.format(playerMove))
                # Not an available move
                elif not playerMove-1 in availableMoves: 
                    print('{} is already taken, choose again.'.format(playerMove))
                else: #valid move
                    print('Player chose: {}'.format(playerMove))
                    validMove = True

        # Convert to board index and return
        return playerMove-1


    def minimax(self, maximize: bool):
        """
        Returns best move and minimized/maximized score for a given game.

        `game`: a TicTacToe game
        `maximize`: bool, True if score should be maximized, False if not

        Recursively calls itself on all possible games from given initial 
        game, alternately maximizing and minimizing score to account for 
        the two players. Score is determined by winning (positive) or 
        losing (negative) and modified by game length.

        The alternate maximize/minimize allows for it to return a move that 
        maximizes the score for one player while minimizing the score for 
        the other. The best move wins the fastest or prevents loss the 
        longest.
        """

        bestScore = None
        bestMove = None

        winner, isOver = self.check_win()

        # If game is over, get score
        if isOver: #game is over

            numMoves = self.get_num_moves()
            bestMove = self.allMoves[-1] #most recent move

            # Player wins (unfavorable)
            if winner == TicTacToe.PLAYER_ONE:
                bestScore = numMoves - 10 #always negative
            # CPU wins (favorable)
            elif winner == TicTacToe.PLAYER_TWO:
                bestScore = 10 - numMoves #always positive
            else: #tie (middle option)
                bestScore = 0

        else: #not isOver
            moves = []
            scores = []

            # Loop through possible moves
            for possibleMove in self.get_available_moves():
                
                # Create copy of current game and add possible move
                possibleGame = copy.deepcopy(self) #new object
                possibleGame.add_move(possibleMove)

                # Run minimax
                nextMove, nextScore = possibleGame.minimax(not maximize)

                # Add score,move pair to respective lists
                scores.append(nextScore)
                if maximize: #cpu's turn
                    moves.append(possibleMove) #current move is cpu's choice
                else: #player's turn
                    moves.append(nextMove) #next move is cpu's choice

            # Find best score
            if maximize:
                bestScore = max(scores)
            else: #not maximize
                bestScore = min(scores)

            # bestMove's index corresponds to bestScore's index
            bestMove = moves[scores.index(bestScore)]

        return bestMove, bestScore


    @staticmethod
    def print_game_instruc():
        """Prints starting instructions for a tic-tac-toe game."""

        startMsg = ('\nGet ready to play! You will be X\'s and the computer '
                    'will be O\'s!\nTo place an x, select the number of '
                    'the corresponding spot.\n')
        print(startMsg)
        time.sleep(2.5)

        # Print layout (player enters 1-9, moves shifted to 0-8 indices)
        layout = (
            '|1|2|3|\n'
            '|4|5|6|\n'
            '|7|8|9|\n'
            )
        print('Here\'s the layout of the board:\n{}'.format(layout))
        time.sleep(2)


    @staticmethod
    def play_tictactoe():
        """
        Starts a one player tic-tac-toe game.

        The player goes first, prompts player for input. Method runs 
        minimax function recursively to choose the best move in response.
        """

        newGame = TicTacToe()

        # Print instructions
        TicTacToe.print_game_instruc()

        # Countdown to game start
        print('Game starting in...',end='',flush=True)
        time.sleep(1)
        for countdown in [3,2,1]:
            print('{}...'.format(countdown),end='',flush=True)
            time.sleep(1)

        newGame.print_board()

        # Start game
        gameOver = False
        while not gameOver:

            # Get player move
            print('It\'s your turn, please choose a move:')
            playerMove = newGame.get_player_move()

            # Add move
            newGame.add_move(playerMove)
            newGame.print_board()

            # Check for win
            winner, gameOver = newGame.check_win()
            if gameOver:
                break

            # Use minimax method to choose best cpu move
            print('Computer\'s turn...')
            cpuMove, score = newGame.minimax(True)
            time.sleep(0.5)
            newGame.add_move(cpuMove)
            newGame.print_board()

            # Check for win
            winner, gameOver = newGame.check_win()

        # Print correct winner's message
        time.sleep(0.5)
        if winner == 0:
            print('Player 1 wins! Congratulations, human!')
        elif winner == 1:
            print('Computer wins! Looks like Drew coded this correctly!')
        elif winner == -1:
            print('It\'s a tie!')


if __name__ == '__main__':
    TicTacToe.play_tictactoe()



