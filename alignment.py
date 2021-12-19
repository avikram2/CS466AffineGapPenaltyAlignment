class ScoringFunction(object):
    def __init__(self, match, gap_opening_penalty, gap_extension_penalty, mismatch):
        assert gap_opening_penalty >= 0
        # "Gap Opening Penalty must be non-negative"
        assert gap_extension_penalty >= 0
        self.match = match
        self.gap_opening_penalty = gap_opening_penalty
        self.gap_extension_penalty = gap_extension_penalty
        self.mismatch = mismatch

    def score(self, x, y):
        if x == y:
            return self.match
        elif x != '-' and y != '-':
            return self.mismatch


class AffineAlignment(object):
    def __init__(self, scoring_function):
        self.scoring_function = scoring_function

    def first_recursion(self, first, match, second, i, j):
        if j > 1:
            return max((first[i][j-1] - self.scoring_function.gap_extension_penalty), (match[i][j-1] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)))
        elif j > 0:
            return match[i][j-1] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)


    def match_recursion(self, first, match, second, i, j, x, y):
        if i > 0 and j > 0:
            match_mismatch = match[i-1][j-1] + self.scoring_function.score(x, y)
            return max(first[i][j], second[i][j], match_mismatch)
        elif j > 0:
            return first[i][j]
        elif i > 0:
            return second[i][j]
        

    def second_recursion(self, first, match, second, i, j):
        if i > 1:
            return max(second[i-1][j] - self.scoring_function.gap_extension_penalty, match[i-1][j] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty))
        elif i > 0:
            return match[i-1][j] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)



    def align(self, v, w):
        first_sequence_gap_matrix = [[float('-inf') for j in range(len(w)+1)] for i in range(len(v)+1)]
        match_mismatch_matrix = [[float('-inf') for j in range(len(w)+1)] for i in range(len(v)+1)]
        second_sequence_gap_matrix = [[float('-inf') for j in range(len(w)+1)] for i in range(len(v)+1)]
        
        match_mismatch_matrix[0][0] = 0

        for i in range(1, len(v)+1):
            if (i == 1):
                second_sequence_gap_matrix[1][0] = -1*(self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)
            else:
                second_sequence_gap_matrix[i][0] = max(second_sequence_gap_matrix[i-1][0] - self.scoring_function.gap_extension_penalty, match_mismatch_matrix[i-1][0] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty))

            match_mismatch_matrix[i][0] = second_sequence_gap_matrix[i][0]
        
        for j in range(1, len(w)+1):
            if j == 1:
                first_sequence_gap_matrix[0][j] = -1*(self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)
            else:
                first_sequence_gap_matrix[0][j] = max(first_sequence_gap_matrix[0][j-1] - self.scoring_function.gap_extension_penalty, match_mismatch_matrix[0][j-1] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty))

            match_mismatch_matrix[0][j] = first_sequence_gap_matrix[0][j]

        for i in range(1, len(v)+1):
            for j in range(1, len(w)+1):
                first_sequence_gap_matrix[i][j] =self.first_recursion(first_sequence_gap_matrix, match_mismatch_matrix, second_sequence_gap_matrix, i, j)
                match_mismatch_matrix[i][j] = self.match_recursion(first_sequence_gap_matrix, match_mismatch_matrix, second_sequence_gap_matrix, i, j, v[i-1], w[j-1])
                second_sequence_gap_matrix[i][j] = self.second_recursion(first_sequence_gap_matrix, match_mismatch_matrix, second_sequence_gap_matrix, i, j)
               

        alignment_score = max(first_sequence_gap_matrix[len(v)][len(w)], second_sequence_gap_matrix[len(v)][len(w)], match_mismatch_matrix[len(v)][len(w)])
        print(match_mismatch_matrix)
        return alignment_score
 

def lecture_example_test():
    s = ScoringFunction(1, 10, 1, -1)
    a = AffineAlignment(s)
    assert a.align("AAC", "ACAAC") == -9
    



if __name__ == "__main__":
    s = ScoringFunction(1, 10, 1, -1)
    a = AffineAlignment(s)
    print(a.align("AAC", "ACAAC"))
                    
                

