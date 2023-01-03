from abc import ABC, abstractmethod
import random


class MinesweeperMove(ABC):
    """Abstract base class for moves that a MinesweeperAgent can make during a game."""


class RandomReveal(MinesweeperMove):
    """Requests the Minesweeper game to press the parachute button, i.e. reveal a non-mine cell at random.

    You should not change the code for this class.

    """

    def __init__(self):
        pass

    def __eq__(self, other):
        return type(other) == RandomReveal


class Reveal(MinesweeperMove):
    """Requests the Minesweeper game to reveal the cell in the specified row and column.

    Rows and columns are specified counting from zero. The upper left cell of the Minesweeper board
    is in row 0 and column 0.

    You should not change the code for this class.

    """

    def __init__(self, row, column):
        self.row, self.column = row, column

    def __eq__(self, other):
        return (type(other).__name__ == Reveal
                and self.row == other.row
                and self.column == other.column)


class MinesweeperAgent(ABC):

    def __init__(self, num_rows, num_columns, num_mines):
        """Constructs a MinesweeperAgent designed to play a game with the specified grid.

        Parameters
        ----------
        num_rows : int
            The number of rows in the Minesweeper grid
        num_columns : int
            The number of columns in the Minesweeper grid
        num_mines : int
            The number of mines in the Minesweeper grid

        """
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_mines = num_mines

    @abstractmethod
    def report(self, row, column, num_mine_neighbors):
        """Informs the agent about the number of cell neighbors containing a mine.

        The cell is specified by its (row, column) coordinates, counting from 0.
        For instance, (0, 0) is the upper left cell of the Minesweeper board.

        A neighbor is any cell that is adjacent (including diagonally adjacent).
        Therefore, a cell can have up to 8 neighbors.

        Parameters
        ----------
        row : int
            The cell's row (counting from 0)
        column : int
            The cell's column (counting from 0)
        num_mine_neighbors : int
            The number of neighbors of the cell containing a mine

        """

    @abstractmethod
    def next_move(self):
        """Returns the next cell to reveal on a given Minesweeper board.

        Returns
        ----------
        (int, int)
            The (row, column) coordinates of the next cell that the agent wants to reveal.

        """

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    def __init__(self, cells, count_mines):
        self.cells = set(cells)
        self.count_mines = count_mines

    def __eq__(self, other):
        return self.cells == other.cells and self.count_mines == other.count_mines

    def __str__(self):
        return f"{self.cells} = {self.count_mines}"

    def known_mine_cells(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If count of mines is equal to number of cells (and > 0), all cells are mines:
        if len(self.cells) == self.count_mines and self.count_mines != 0:
            return self.cells
        else:
            return set()

    def known_safe_cells(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If count of mines is zero then all cells in the sentence are safe:
        if self.count_mines == 0:
            return self.cells
        else:
            return set()

    def mark_cell_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is in the sentence, remove it and decrement count by one
        if cell in self.cells:
            self.cells.remove(cell)
            self.count_mines -= 1

    def mark_cell_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell is in the sentence, remove it, but do not decrement count
        if cell in self.cells:
            self.cells.remove(cell)

class MyImrovedMinesweeperAgent(MinesweeperAgent):
    def __init__(self, num_rows, num_columns, num_mines):
        """Constructs a MinesweeperAgent designed to play a game with the specified grid.

        Parameters
        ----------
        num_rows : int
            The number of rows in the Minesweeper grid
        num_columns : int
            The number of columns in the Minesweeper grid
        num_mines : int
            The number of mines in the Minesweeper grid

        """
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_mines = num_mines

        # Keep track of which cells have been clicked on
        self.revealed_cells = set()

        # Keep track of cells known to be safe or mines
        self.mine_cells = set()
        self.safe_cells = set()

        # List of sentences about the game known to be true
        self.feedback = []

    def mark_cell_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mine_cells.add(cell)
        for sentence in self.feedback:
            sentence.mark_cell_mine(cell)

    def mark_cell_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safe_cells.add(cell)
        for sentence in self.feedback:
            sentence.mark_cell_safe(cell)

    
    def report(self, row, column, num_mine_neighbors):
        """Informs the agent about the number of cell neighbors containing a mine.

        The cell is specified by its (row, column) coordinates, counting from 0.
        For instance, (0, 0) is the upper left cell of the Minesweeper board.

        A neighbor is any cell that is adjacent (including diagonally adjacent).
        Therefore, a cell can have up to 8 neighbors.

        Parameters
        ----------
        row : int
            The cell's row (counting from 0)
        column : int
            The cell's column (counting from 0)
        num_mine_neighbors : int
            The number of neighbors of the cell containing a mine

        """
        # define what a cell is: i.e. a specific row, column
        cell = (row, column)

        # Mark the cell as a move that has been made, and mark as safe:
        self.revealed_cells.add(cell)
        self.mark_cell_safe(cell)

        # Create set to store undecided cells for feedback:
        new_sentence_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # If cells are already safe, ignore them:
                if (i, j) in self.safe_cells:
                    continue

                # If cells are known to be mines, reduce count by 1 and ignore them:
                if (i, j) in self.mine_cells:
                    num_mine_neighbors = num_mine_neighbors - 1
                    continue

                # Otherwise add them to sentence if they are in the game board:
                if 0 <= i < self.num_rows and 0 <= j < self.num_columns:
                    new_sentence_cells.add((i, j))

        # Add the new sentence to the AI agent's feedback:
        self.feedback.append(Sentence(new_sentence_cells, num_mine_neighbors))

        # Iteratively mark guaranteed mines and safes, and infer new feedback:
        feedback_changed = True

        while feedback_changed:
            feedback_changed = False

            safe_cells = set()
            mine_cells = set()

            # Get set of safe spaces and mines from feedback
            for sentence in self.feedback:
                safe_cells = safe_cells.union(sentence.known_safe_cells())
                mine_cells = mine_cells.union(sentence.known_mine_cells())

            # Mark any safe spaces or mines:
            if safe_cells:
                feedback_changed = True
                for safe in safe_cells:
                    self.mark_cell_safe(safe)
            if mine_cells:
                feedback_changed = True
                for mine in mine_cells:
                    self.mark_cell_mine(mine)

            # Remove any empty sentences from feedback:
            empty = Sentence(set(), 0)

            self.feedback[:] = [x for x in self.feedback if x != empty]

            # Try to infer new sentences from the current ones:
            for sentence_1 in self.feedback:
                for sentence_2 in self.feedback:

                    # Ignore when sentences are identical
                    if sentence_1.cells == sentence_2.cells:
                        continue

                    # Raise a ValueError if a sentence with no cells and a nonzero number of mines is created
                    if sentence_1.cells == set() and sentence_1.count_mines > 0:
                        print('Error: sentence with no cells and a nonzero number of mines was created')
                        raise ValueError

                    # Create a new sentence if 1 is subset of 2 and is not in feedback:
                    if sentence_1.cells.issubset(sentence_2.cells):
                        new_sentence_cells = sentence_2.cells - sentence_1.cells
                        new_sentence_count = sentence_2.count_mines - sentence_1.count_mines

                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                        # Add to feedback if not already in feedback:
                        if new_sentence not in self.feedback:
                            feedback_changed = True
                            self.feedback.append(new_sentence)
    
    def next_move(self):
        """Returns the next cell to reveal on a given Minesweeper board.

        Returns
        ----------
        (int, int)
            The (row, column) coordinates of the next cell that the agent wants to reveal.

        """
        # Create a set of all safe moves available and then Reveal() one of those safe cells if they're still available
        safe_moves = self.safe_cells - self.revealed_cells - self.mine_cells
        if safe_moves:
            safeMoveRow, safeMoveCol = random.choice(list(safe_moves))
            safeMove = Reveal(safeMoveRow, safeMoveCol)
            return safeMove
        
        # Return a random choice from the best moves list
        return RandomReveal()

class NotSoGoodAgent(MinesweeperAgent):
    """A MinesweeperAgent who plays rather poorly.

    90% of the time, this agent just pushes the parachute button. The other 10% of the time,
    the agent reveals the unrevealed cell that is closest to the upper left (i.e. proceeding
    left-to-right through each row, until an unrevealed cell is found).

    """
    def __init__(self, num_rows, num_columns, num_mines):
        super().__init__(num_rows, num_columns, num_mines)
        self.unrevealed = set()
        for row in range(num_rows):
            for col in range(num_columns):
                self.unrevealed.add((row, col))

    def report(self, row, column, num_mine_neighbors):
        """Removes the reported cell from the agent's list of unrevealed cells."""
        self.unrevealed.remove((row, column))

    def next_move(self):
        """Executes the agent's not so good strategy."""
        if random.random() < 0.1 and len(self.unrevealed) > 0:
            row, col = sorted(self.unrevealed)[0]
            return Reveal(row, col)
        else:
            return RandomReveal()


def initialize_agent(num_rows, num_columns, num_mines):
    """Initializes the agent who will play Minesweeper.

    Change this function to initialize your own MinesweeperAgent (instead of the
    default NotSoGoodAgent).

    """
    return MyImrovedMinesweeperAgent(num_rows, num_columns, num_mines)
