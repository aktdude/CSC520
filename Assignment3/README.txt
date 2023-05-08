N-QUEENS & Prolog

I made my code using VSCODE. The two files I have are nqueens.py and prolog.pl.

NQueens is a problem to make a chess board with a queen in each column and no queens attack each other
I run Question 1(NQueens) by doing:
python nqueens.py basic 10
python nqueens.py forward 10

for each of the algorithms. This prints a solution assigning to each queen, and the amount of backtracks.
It also prints a visual representation of the board where 0s are empty spots and Qs are the queens.
Here is an example output:
Solution: Q0= 0, Q1= 2, Q2= 5, Q3= 7, Q4= 9, Q5= 4, Q6= 8, Q7= 1, Q8= 3, Q9= 6
Backtrack count: 92
['Q', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', 'Q', '0', '0']
['0', 'Q', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', 'Q', '0']
['0', '0', '0', '0', '0', 'Q', '0', '0', '0', '0']
['0', '0', 'Q', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', 'Q']
['0', '0', '0', 'Q', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', 'Q', '0', '0', '0']
['0', '0', '0', '0', 'Q', '0', '0', '0', '0', '0']


For Question 3(Prolog) I ran it by doing:
swipl
[prolog].

Here are my queries and the results:
2 ?- bird(X).
X = frank ;
X = bob.

3 ?- human(albert).
true.

4 ?- human(bob).
false.

5 ?- creature(X).
X = albert ;
X = louis ;
X = frank ;
X = bob.

6 ?- fly(X).
X = bob ;
X = albert.



