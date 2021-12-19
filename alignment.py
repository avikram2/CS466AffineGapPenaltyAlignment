class BacktrackingPointers(object):
    def __init__(self, v, w):
        self.v = v
        self.w = w
        self.i = len(v)
        self.j = len(w)
        self.right_backpointer_matrix = [["STOP" for j in range(len(w)+1)] for i in range(len(v)+1)]
        self.diag_backpointer_matrix = [["STOP" for j in range(len(w)+1)] for i in range(len(v)+1)]
        self.down_backpointer_matrix = [["STOP" for j in range(len(w)+1)] for i in range(len(v)+1)]

    def set_pointer(self, current_matrix, i, j, previous_matrix, i_prev, j_prev):
        if (current_matrix == 'right'):
            self.right_backpointer_matrix[i][j] = (previous_matrix, i_prev, j_prev)
        elif (current_matrix == 'diag'):
            self.diag_backpointer_matrix[i][j] = (previous_matrix, i_prev, j_prev)
        elif (current_matrix == "down"):
            self.down_backpointer_matrix[i][j] = (previous_matrix, i_prev, j_prev)
        
        else:
            Exception("Current Matrix argument is invalid")


    def backtrace(self, ending_matrix):
        v_alignment = ""
        w_alignment = ""
        curr_matrix = None
        if ending_matrix == "right":
            curr_matrix = self.right_backpointer_matrix
        elif ending_matrix == "diag":
            curr_matrix = self.diag_backpointer_matrix
        elif ending_matrix == "down":
            curr_matrix = self.down_backpointer_matrix

        else:
            Exception("Ending Matrix argument is not valid")    
        
        while (curr_matrix[self.i][self.j] != "STOP"):
            pointer = curr_matrix[self.i][self.j]
            if (pointer[0] == "right"):
                v_alignment += "-"
                w_alignment += self.w[self.j-1]
                curr_matrix = self.right_backpointer_matrix
            elif (pointer[0] == "diag"):
                v_alignment += self.v[self.i-1]
                w_alignment += self.w[self.j-1]
                curr_matrix = self.diag_backpointer_matrix
            elif (pointer[0] == "down"):
                v_alignment += self.v[self.i-1]
                w_alignment += "-"
                curr_matrix = self.down_backpointer_matrix
            
            self.i = pointer[1]
            self.j = pointer[2]
            
        return (v_alignment[::-1], w_alignment[::-1])



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

    def first_recursion(self, first, match, second, i, j, backtrace):
        if j > 1:
            extension_val = first[i][j-1] - self.scoring_function.gap_extension_penalty
            opening_val = match[i][j-1] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)
            if (extension_val > opening_val):
                backtrace.set_pointer("right", i, j, "right", i, j-1)
                return extension_val, backtrace
            else:
                backtrace.set_pointer("right", i, j, "diag", i, j-1)
                return opening_val, backtrace
        elif j > 0:
            backtrace.set_pointer("right", i, j, "diag", i, j-1)
            return match[i][j-1] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty), backtrace


    def match_recursion(self, first, match, second, i, j, x, y, backtrace):
        if i > 0 and j > 0:
            match_mismatch = match[i-1][j-1] + self.scoring_function.score(x, y)
            
            val = max(first[i][j], second[i][j], match_mismatch)
            
            if (val == match_mismatch):
                backtrace.set_pointer("diag", i, j, "diag", i-1, j-1)
                return val, backtrace
            elif val == first[i][j]:
                backtrace.set_pointer("diag", i, j, "right", i, j)
                return val, backtrace
            elif val == second[i][j]:
                backtrace.set_pointer("diag", i, j, "down", i, j)          
                return val, backtrace
        elif j > 0:
            backtrace.set_pointer("diag", i, j, "right", i, j)
            return first[i][j], backtrace
        elif i > 0:
            backtrace.set_pointer("diag", i, j, "down", i, j)
            return second[i][j], backtrace
        

    def second_recursion(self, first, match, second, i, j, backtrace):
        if i > 1:
            extension_val = second[i-1][j] - self.scoring_function.gap_extension_penalty
            opening_val = match[i-1][j] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)
            if extension_val > opening_val:
                backtrace.set_pointer("down", i, j, "down", i-1, j)
                return extension_val, backtrace
            else:
                backtrace.set_pointer("down", i, j, "diag", i-1, j)
                return opening_val, backtrace
        elif i > 0:
            backtrace.set_pointer("down", i, j, "diag", i-1, j)
            return match[i-1][j] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty), backtrace



    def align(self, v, w):
        first_sequence_gap_matrix = [[float('-inf') for j in range(len(w)+1)] for i in range(len(v)+1)]
        match_mismatch_matrix = [[float('-inf') for j in range(len(w)+1)] for i in range(len(v)+1)]
        second_sequence_gap_matrix = [[float('-inf') for j in range(len(w)+1)] for i in range(len(v)+1)]
        
        match_mismatch_matrix[0][0] = 0

        backtrace = BacktrackingPointers(v, w)

        for i in range(1, len(v)+1):
            if (i == 1):
                second_sequence_gap_matrix[1][0] = -1*(self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)
                #backtrace.set_pointer("down", 1, 0, "diag", 0, 0)
            else:
                second_sequence_gap_matrix[i][0] = max(second_sequence_gap_matrix[i-1][0] - self.scoring_function.gap_extension_penalty, match_mismatch_matrix[i-1][0] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty))
                #backtrace.set_pointer("down", i, 0, "down", i-1, 0)

            match_mismatch_matrix[i][0] = second_sequence_gap_matrix[i][0]
            backtrace.set_pointer("down", i, 0, "down", i-1, 0)
            backtrace.set_pointer("diag", i, 0, "down", i-1, 0)
        
        for j in range(1, len(w)+1):
            if j == 1:
                first_sequence_gap_matrix[0][j] = -1*(self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty)
                #backtrace.set_pointer("right", 0, j, "diag", 0, 0)
            else:
                first_sequence_gap_matrix[0][j] = max(first_sequence_gap_matrix[0][j-1] - self.scoring_function.gap_extension_penalty, match_mismatch_matrix[0][j-1] - (self.scoring_function.gap_extension_penalty + self.scoring_function.gap_opening_penalty))
                #backtrace.set_pointer("right", 0, j, "right", 0, j-1)
            match_mismatch_matrix[0][j] = first_sequence_gap_matrix[0][j]
            backtrace.set_pointer("diag", 0, j, "right", 0, j-1)
            backtrace.set_pointer("right", 0, j, "right", 0, j-1)

        for i in range(1, len(v)+1):
            for j in range(1, len(w)+1):
                first = self.first_recursion(first_sequence_gap_matrix, match_mismatch_matrix, second_sequence_gap_matrix, i, j, backtrace)
                first_sequence_gap_matrix[i][j] = first[0]
                backtrace = first[1]
                second = self.second_recursion(first_sequence_gap_matrix, match_mismatch_matrix, second_sequence_gap_matrix, i, j, backtrace)
                second_sequence_gap_matrix[i][j] = second[0]
                backtrace = second[1]
                match = self.match_recursion(first_sequence_gap_matrix, match_mismatch_matrix, second_sequence_gap_matrix, i, j, v[i-1], w[j-1], backtrace)
                match_mismatch_matrix[i][j] = match[0]
                backtrace = match[1]
        alignment_score = max(first_sequence_gap_matrix[len(v)][len(w)], second_sequence_gap_matrix[len(v)][len(w)], match_mismatch_matrix[len(v)][len(w)])
        if (alignment_score == match_mismatch_matrix[len(v)][len(w)]):
            v_align, w_align = backtrace.backtrace("diag")
        elif alignment_score == first_sequence_gap_matrix[len(v)][len(w)]:
            v_align, w_align = backtrace.backtrace("right")
        elif alignment_score == second_sequence_gap_matrix[len(v)][len(w)]:
            v_align, w_align = backtrace.backtrace("down")

        return (alignment_score, v_align, w_align)
 

def lecture_example_test():
    s = ScoringFunction(1, 10, 1, -1)
    alignment = AffineAlignment(s).align("AAC", "ACAAC")
    assert alignment[0]  == -9
    assert alignment[1] == "--AAC"
    assert alignment[2] == "ACAAC"




if __name__ == "__main__":
    lecture_example_test()
    s = ScoringFunction(1, 3, 1, -1)
    alignment = AffineAlignment(s).align("AAT", "ACACT")
    print(alignment)
                    
                

