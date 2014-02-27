threes-ai
=========

An AI for Threes!, the popular iOS game. You can have the AI play or 'cheat' by entering in your own board and having the AI tell you which moves to make.

##Instructions

Simply run:

    python threes-ai.py
    
###Sample run
    Do you want to play or have the AI play? (Say "human" or "ai"): human
    Enter in the board (Enter in 16 numbers on one line): 0 2 0 1 3 0 0 3 0 0 0 1 1 3 2 2
    Enter in the anticipated value of the next piece: 3
    [0, 2, 0, 1]
    [3, 0, 0, 3]
    [0, 0, 0, 1]
    [1, 3, 2, 2]
    Perform Down Swipe
    Enter in your move (r, l, u, d): d
    
    Enter in the actual value of the new piece: 3
    Enter in the row or column of the new piece (A number between 0 and 3): 0
    [3, 0, 0, 0]
    [0, 2, 0, 1]
    [3, 0, 0, 3]
    [1, 3, 2, 3]
    Actual score: 15 Heuristic score: 173.96
    ...
