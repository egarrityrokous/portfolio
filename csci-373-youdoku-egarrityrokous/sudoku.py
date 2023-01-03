import math
import cnf
import copy
import math
from dpll import dpll

class SudokuBoard:
    """Representation of a Sudoku board."""

    def __init__(self, matrix):
        """
        Parameters
        ----------
        matrix : list[list[int]]
            A two-dimensional array, providing the initial values of each cell.
            Zero represents an empty cell.
        """
        self.matrix = matrix

    def __str__(self):
        """A simple string representation of the board.

        See TestSudokuBoard.test_board_str and TestSudokuBoard.test_board_str2
        in test.py for examples of expected output.
        """
        result = []
        for row in self.matrix:
            stringList = []
            for item in row:
                stringList.append(str(item))
            result.append("".join(stringList))
        return "\n".join(result)

    def rows(self):
        """Returns the row addresses of the board.

        Specifically, this returns a list of sets, where each set corresponds to
        the addresses of a single row. For a 2x2 Sudoku board, this would be:

        [{(1, 1), (1, 2), (1, 3), (1, 4)},
         {(2, 1), (2, 2), (2, 3), (2, 4)},
         {(3, 1), (3, 2), (3, 3), (3, 4)},
         {(4, 1), (4, 2), (4, 3), (4, 4)}]

        The order of the rows in the list should be top-to-bottom.
        """
        result = []
        for i in range(1, len(self.matrix)+1):
            result.append({(i,j) for j in range(1, len(self.matrix[0])+1)})
        return result

    def columns(self):
        """Returns the column addresses of the board.

        Specifically, this returns a list of sets, where each set corresponds to
        the addresses of a single column. For a 2x2 Sudoku board, this would be:

        [{(1, 1), (2, 1), (3, 1), (4, 1)},
         {(1, 2), (2, 2), (3, 2), (4, 2)},
         {(1, 3), (2, 3), (3, 3), (4, 3)},
         {(1, 4), (2, 4), (3, 4), (4, 4)}]

        The order of the columns in the list should be left-to-right.
        """
        result = []
        for i in range(1, len(self.matrix)+1):
            result.append({(j,i) for j in range(1, len(self.matrix[0])+1)})
        return result

    def boxes(self):
        """Returns the addresses of each box of the board.

        Specifically, this returns a list of sets, where each set corresponds to
        the addresses of a single box. For a 2x2 Sudoku board, this would be:

        [{(1, 1), (1, 2), (2, 1), (2, 2)},
         {(1, 3), (1, 4), (2, 3), (2, 4)},
         {(3, 1), (3, 2), (4, 1), (4, 2)},
         {(3, 3), (3, 4), (4, 3), (4, 4)}]

        The order of the columns in the list should be left-to-right, then
        top-to-bottom.
        """
        result = []
        width = int(len(self.matrix)**(1/2))
        for i in range(0,len(self.matrix),width):
            for j in range(0,len(self.matrix),width):
                result.append(self.boxHelper(width,i,j))
        return result

    def boxHelper(self, width, rowOffset, colOffset):
        result = set()
        for row in range(1, width+1):
            for col in range(1, width+1):
                result.add((row+rowOffset,col+colOffset))
        return result

    def contents(self):
        """Computes a set of clauses that describe the current board state.

        In other words, this creates clauses that describe the numbers have already
        been filled in. For instance, if the board were:

        board = SudokuBoard([ [0, 0, 0, 3],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 1, 0, 0] ])

        then ```board.contents()``` should return a set of Clauses equivalent to:

        { cnf.c('d3_1_4'), cnf.c('d1_4_2') }

        The first clause (```cnf.c('d3_1_4')```) asserts that the digit 3 must appear
        at address (1,4), whereas the second clause asserts that the digit 1 must
        appear at address (4,2).

        Returns
        -------
        set[Clause]
            the set of clauses that describe the current board state
        """
        result = set()
        cells = self.matrix
        for cell in cells:
            for num in cell:
                if num != 0:
                    result.add(cnf.c("d" + str(num)
                        + f"_{cells.index(cell) + 1}_{cell.index(num) + 1}"))
        return result

    def cnf(self):
        """Constructs a cnf.Cnf instance that fully describes this SudokuBoard.

        Note that the CNF sentence should express both the rules of Sudoku (each zone
        contains exactly one of each digit, no cell is empty) and the current board
        state (which cells have already been filled in by particular digits).

        Returns
        -------
        Cnf
            a CNF sentence describing this sudoku board
        """
        result = []
        rows = self.rows()
        columns = self.columns()
        boxes = self.boxes()
        zones = rows + columns + boxes
        board_len = len(self.matrix[0])

        clauses = set()
        for zone in zones:
            for d in range(1, board_len + 1):
                exactlyOne = at_most_clauses(zone, d) + [at_least_clause(zone, d)]
                for clause in exactlyOne:
                    clauses.add(cnf.c(clause))

        box_width = int(math.sqrt(board_len))
        allClauses = clauses.union(nonempty_clauses(box_width)).union(self.contents())
        return cnf.Cnf(allClauses)

    def solve(self):
        """Constructs a new Sudokuboard corresponding to a valid puzzle completion.

        For instance, if

            board = SudokuBoard([[4, 1, 2, 3],
                                 [3, 4, 1, 2],
                                 [2, 3, 4, 1],
                                 [0, 0, 0, 0]])

        Then board.solve() should return a new SudokuBoard instance equivalent to:

            SudokuBoard([[4, 1, 2, 3],
                         [3, 4, 1, 2],
                         [2, 3, 4, 1],
                         [1, 2, 3, 4]])

        If there are no valid completions, then this should return None.
        If there are multiple valid completions, then any may be returned.
        """
        def interpret_lit(l):
            negate = (l[0] == "!")
            if negate:
                l = l[2:]
            else:
                l = l[1:]
            d, i, j = l.split("_")
            return d, i, j, negate
        model = dpll(self.cnf())
        if model is None:
            return None
        matrix = copy.deepcopy(self.matrix)
        positive_literals = [l for l in model if model[l] == 1]
        for l in positive_literals:
            d, i, j, _ = interpret_lit(l)
            matrix[int(i)-1][int(j)-1] = int(d)
        return SudokuBoard(matrix)

def at_least_clause(zone, d):
    """Creates clauses for the constraint "this zone must contain digit d at least once".

    Specificially, this takes a set `zone` of cell addresses and a digit `d`.
    It should produce a string representation of the clause corresponding to the
    constraint "digit `d` should appear at least once among the addresses in
    `zone`". For instance:

        at_least_clause({(1, 3), (1, 4), (2, 3), (2, 4)}, d=2)

    should return the string:

        'd2_1_3 || d2_1_4 || d2_2_3 || d2_2_4'

    For this string, the literals are expected to be listed in alphabetical
    order (according to a string comparison).

    Parameters
    ----------
    zone : set[tuple[int]]
        a set of cell addresses
    d : int
        a digit of the Sudoku puzzle

    Returns
    -------
    str
        a string representation of the clause corresponding to the constraint
        "this zone must contain digit d at least once"
    """
    result = []
    for cell in zone:
        result.append("d" + str(d))
        for num in cell:
            result.append(str(num))
    N = 3
    resultList = [result[n:n+N] for n in range(0, len(result), N)]
    resultCopy = []
    for subList in resultList:
        resultCopy+=["_".join(subList)]
    finalResult = sorted(resultCopy)
    return " || ".join(finalResult)


def at_most_clauses(cells, d):
    """Creates clauses for the constraint "this zone must contain digit d at most once".

    Specificially, this takes a set `zone` of cell addresses and a digit `d`.
    It should produce a string representation of the clause corresponding to the
    constraint "digit `d` should appear at most once among the addresses in
    `zone`". For instance:

        at_most_clauses({(1, 3), (1, 4), (2, 3), (2, 4)}, d=2)

    should return the list:

        ['!d2_1_3 || !d2_1_4',
         '!d2_1_3 || !d2_2_3',
         '!d2_1_3 || !d2_2_4',
         '!d2_1_4 || !d2_2_3',
         '!d2_1_4 || !d2_2_4',
         '!d2_2_3 || !d2_2_4']

    For this string, the literals are expected to be listed in alphabetical
    order (according to a string comparison).

    Parameters
    ----------
    zone : set[tuple[int]]
        a set of cell addresses
    d : int
        a digit of the Sudoku puzzle

    Returns
    -------
    str
        a string representation of the clause corresponding to the constraint
        "this zone must contain digit d at most once"
    """
    sortedCells = sorted(cells)
    result = ""
    resultList = []
    for i in range(len(sortedCells)):
        result = "!d" + str(d) + formatCells(i, sortedCells)
        for j in range(i+1, len(sortedCells)):
            resultTemp = result + " || " + "!d" + str(d) + formatCells(j, sortedCells)
            resultList.append(resultTemp)
            resultTemp = ""
    return resultList

def formatCells(cell, cells):
    cellsCopy = list(cells)
    a,b = cellsCopy[cell]
    result = f"_{a}_{b}"
    return result


def nonempty_clauses(box_width):
    """Creates clauses for the constraint "no cell can be empty".

    Specificially, this takes as argument the width of a box on your Sudoku board.
    It should produce a list of the string representations of the clauses
    corresponding to the constraint "no cell can be empty". For instance,
    the call nonempty_clauses(2)

    should return the list:
        Y { d:(1,2,3,4), A(i,j):((1,1), (1,2), ..., (4,3), (4,4)) }
        ['d1_1_1 || d2_1_1 || d3_1_1 || d4_1_1',
         'd1_1_2 || d2_1_2 || d3_1_2 || d4_1_2',
         'd1_1_3 || d2_1_3 || d3_1_3 || d4_1_3',
         'd1_1_4 || d2_1_4 || d3_1_4 || d4_1_4',
         'd1_2_1 || d2_2_1 || d3_2_1 || d4_2_1',
         'd1_2_2 || d2_2_2 || d3_2_2 || d4_2_2',
         'd1_2_3 || d2_2_3 || d3_2_3 || d4_2_3',
         'd1_2_4 || d2_2_4 || d3_2_4 || d4_2_4',
         'd1_3_1 || d2_3_1 || d3_3_1 || d4_3_1',
         'd1_3_2 || d2_3_2 || d3_3_2 || d4_3_2',
         'd1_3_3 || d2_3_3 || d3_3_3 || d4_3_3',
         'd1_3_4 || d2_3_4 || d3_3_4 || d4_3_4',
         'd1_4_1 || d2_4_1 || d3_4_1 || d4_4_1',
         'd1_4_2 || d2_4_2 || d3_4_2 || d4_4_2',
         'd1_4_3 || d2_4_3 || d3_4_3 || d4_4_3',
         'd1_4_4 || d2_4_4 || d3_4_4 || d4_4_4']

    For this string, the literals are expected to be listed in alphabetical
    order (according to a string comparison).

    Parameters
    ----------
    box_width : int
        the width of a box of the Sudoku board

    Returns
    -------
    str
        a string representation of the clause corresponding to the constraint
        "no cell can be empty"
    """
    board_nums = list(range(1, pow(box_width, 2) + 1))
    board_len = len(board_nums)
    result = []
    for i in range(board_len): #traverse the i coordinate positions
        for j in range(board_len): #traverse the j coordinate positions
            temp = []
            for d in board_nums: #traverse the j coordinate positions
                d_s = "d" + str(d) + f"_{i + 1}_{j + 1}"
                temp.append(d_s)
            result.append(' || '.join(temp))
    return result
