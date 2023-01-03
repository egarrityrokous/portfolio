from search import SearchSpace, dfs, bfs

class PuzzleSearchSpace(SearchSpace):
    def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes #where inflection points are
        self.start_state = self.get_state(["U", "E"]) #state always is [U, U, U, E, E, S, ...]
        self.width = int((sum(self.nodes) + 1) ** (1/3))
        self.vecs = {"N" : (0,1,0), "S" : (0,-1,0), "E" : (1,0,0),
                    "W" : (-1,0,0), "U": (0,0,1), "D" : (0,0,-1)}

    def get_state(self, state):
        final = []
        for i in range(len(state)):
            final.extend([state[i]] * self.nodes[i])
        return final

    def get_start_state(self):
        """Returns the start state."""
        return self.start_state

    def is_goal_state(self, state):
        """Checks whether a given state is a goal state.

        Parameters
        ----------
        state
            A valid state of the search space

        Returns
        -------
        bool
            True iff the state is a goal state
        """
        return len(state) == sum(self.nodes)

    def helper(self, state, coords):
        """ Takes a state and returns cartesian coordinates
        corresponding to the state """
        min_x, max_x, min_y, max_y, min_z, max_z = 0,0,0,0,0,0
        for i in range(len(state)):
            (a_0,b_0,c_0) = coords[-1]
            (a_1,b_1,c_1) = self.vecs[state[i]]
            (a,b,c) = (a_0 + a_1, b_0 + b_1, c_0 + c_1)
            if a < min_x : min_x = a
            if a > max_x : max_x = a
            if b > max_y : max_y = b
            if b < min_y : min_y = b
            if c > max_z : max_z = c
            if c < min_z : min_z = c
            if max_x - min_x >= self.width or max_y - min_y >= self.width or max_z - min_z >= self.width:
                return False
            coords.append((a,b,c))
        return len(set(coords)) == len(coords)

    def is_valid(self, state):
        return self.helper(state, [(0,0,0)])

    def perp(self, dir):
        """ returns list of directions perp to dir"""
        (a_0, b_0, c_0) = self.vecs[dir]
        par = [(a_0, b_0, c_0), (-a_0, -b_0, -c_0)]
        return [d for d in self.vecs if self.vecs[d] not in par]

    def get_successors(self, state):
        """Determines the possible successors of a state.

        For efficiency, it is important to try to only generate successors that
        can possibly lead to a goal state.

        Parameters
        ----------
        state
            A state of the search space

        Returns
        -------
        list
            The list of valid successor states.
        """
        poss = self.perp(state[-1])
        index = 1
        for i in range(len(state) - 1):
            if state[i] != state[i + 1]: index += 1
        candidates = [state + [dir] * self.nodes[index] for dir in poss]
        return [can for can in candidates if self.is_valid(can)]

class SnakePuzzle(PuzzleSearchSpace):
    def __init__(self):
        super().__init__([2,2,2,2,1,1,1,2,2,1,1,2,1,2,1,1,2])

class SnakePuzzleB(PuzzleSearchSpace):
    def __init__(self):
        super().__init__([2,2,2,1,1,1,1,1,2,2,2,1,2,1,2,1,2])

class SnakePuzzleC(PuzzleSearchSpace):
    def __init__(self):
        super().__init__([1,1,1,2,2,1,2,2,1,1,1,1,2,2,1,2,1,2])

def puzzle_solution():
    """Computes a solution to the block puzzle distributed in class.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """
    return dfs(SnakePuzzle())


def solution_b():
    """Computes a solution to block puzzle B from the assignment.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """

    return dfs(SnakePuzzleB())

def solution_c():
    """Computes a solution to block puzzle C from the assignment.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """
    return dfs(SnakePuzzleC())

if __name__ == '__main__':
    print(puzzle_solution())
    print("____")
    print(solution_b())
    print("-------")
    print(solution_c())
