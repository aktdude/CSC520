For the written part I am submitting a scanned PDF. I also have an image file that may be slightly clearer but due to the
submisison specifications I am refraining from submitting that unless asked.
I also can bring the physical copy if necessary and requested soon after the due date.

For the coding part, I added more titles and description for understanding purposes.
Here is a sample runthrough:

PS C:\Users\aktdu\Desktop\Assign4> python HMM.py HMM_model.txt RFB

START PROBABILITIES
p(H0 = O) = 0.3
p(H0 = A) = 0.4
p(H0 = N) = 0.3
--------------------------------
TRANSITION PROBABILITIES
p(H(i) = O | H(i-1) = O) = 0.5
p(H(i) = A | H(i-1) = O) = 0.4
p(H(i) = N | H(i-1) = O) = 0.1
p(H(i) = O | H(i-1) = A) = 0.3
p(H(i) = A | H(i-1) = A) = 0.5
p(H(i) = N | H(i-1) = A) = 0.2
p(H(i) = O | H(i-1) = N) = 0
p(H(i) = A | H(i-1) = N) = 0.4
p(H(i) = N | H(i-1) = N) = 0.6
--------------------------------
OBSERVATION PROBABILITIES
p(O(i) = R | H(i) = O) = 0.8
p(O(i) = F | H(i) = O) = 0.1
p(O(i) = B | H(i) = O) = 0.1
p(O(i) = R | H(i) = A) = 0.2
p(O(i) = F | H(i) = A) = 0.4
p(O(i) = B | H(i) = A) = 0.4
p(O(i) = R | H(i) = N) = 0
p(O(i) = F | H(i) = N) = 0.5
p(O(i) = B | H(i) = N) = 0.5
--------------------------------
RESULTS

Before evidence observed:
p(H0): {'O': '0.3', 'A': '0.4', 'N': '0.3'}

p(H1): {'O': 0.27, 'A': 0.44, 'N': 0.29}

State R observed
        Updated distribution ( p(H1 | R) ) = {'O': 0.71053, 'A': 0.28947, 'N': 0.0} (alpha=3.28947)

State F observed
        Updated distribution ( p(H2 | R,F) ) = {'O': 0.15775, 'A': 0.6122, 'N': 0.23005} (alpha=3.56804)

State B observed
        Updated distribution ( p(H3 | R,F,B) ) = {'O': 0.07525, 'A': 0.52883, 'N': 0.39592} (alpha=2.86647)