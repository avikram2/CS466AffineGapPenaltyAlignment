# CS466AffineGapPenaltyAlignment

Final Project CS 466 Ayush Vikram: Extending Pairwise Global Alignment Algorithm to Handle Affine Gap Penalties

Code Usage:
The implementation is present in alignment.py

Firstly, you can set up your scoring parameters by using an object of the ScoringFunction class.

Syntax: ScoringFunction(match, gap_opening_penalty, gap_extension_penalty, mismatch)

For example, s = ScoringFunction(10, 7, 3, -2) will return an object of the ScoringFunction class which has match = 10, gap_opening penalty of 7, gap_extension penalty of 3 and mismatch of -2. Note that gap_opening_penalty and gap_extension_penalty will always be non-negative, as we are following the lecture definition, in which they are positive quantities that are subtracted.

Next, you can create an object of class AffineAlignment, passing in the ScoringFunction object:

a = AffineAlignment(s)

In this class, the align member function will take in two strings, v, and w as parameters, and will return the alignment score, aligned version of v, and aligned w as a tuple.
For example,
a = AffineAlignment(s)
val = a.align("AAC", "ACAAC")
val[0] will equal -9, the score
val[1] will equal "--AAC", aligned v
val[2] will equal "ACAAC", aligned w


Data:
The DNA_random(length) function will return a randomly-generated DNA string of the length specified. These can be passed into the .align() function to perform affine gap alignment. 

The results_random_DNA_strings(length1 = 50, length2 = 75, gap_opening = 10, gap_extension = 5, match = 7, mismatch = -4) function takes in as parameter the length1 (length of v), length2 (length of w), gap opening and gap extension penalties (note, non-negative), and mismatch score, create a Scoring Function object, pass it in into a AffineAlignment object, run the alignment, and then print out the score and aligned v and aligned w.
