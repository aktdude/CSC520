### Tic Tac Toe
My code is ran in the following way:
python game-search.py a "1 2 0,0 1 0,0 0 2"
It outputs the Starting Player,
the Chosen Algorithm
The Sequence of Board States
The Winner
The number of game tree nodes.

The output I get for this example is:
Starting player: 
Player 1

Chosen Algorithm: Minimax

Sequence of board states:

[[1 2 0]
 [0 1 0]
 [0 0 2]]
------------

[[1 2 0]
 [1 1 0]
 [0 0 2]]
------------

[[1 2 2]
 [1 1 0]
 [0 0 2]]
------------

[[1 2 2]
 [1 1 1]
 [0 0 2]]
------------

Winner: Player 1

Number of game tree nodes: 238

(End of sample output)
If a, it runs the mini max algorithm
If b, it runs the alpha beta algorithm
My program assumes that at the beginning of the game, player 1 is always going first,
meaning that the board that is given to me will always have one more 1 or equal 1s to the number of 2s.
My program can handle at empty board or a full board, though it will take slightly longer for the empty board to run.
Additionally, there are many cases that will end in a tie, because if Player 1 and Player 2 both play optimally from the start,
the game will always end in a tie.
Finally, one thing to clarify, is if my algorithm finds that it will lose no matter what (2 threats of 3 in a row),
it will simply play the first available move, even if it's not a blocking move.
This is because even if it blocks one 3-in-a-row, it will still lose on the next move.

I developed the program in VSCode and added some comments clarifying throughout. 
Additionally, my written responses are in a separate document.
