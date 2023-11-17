from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance, euclidean_distance
from helpers.utils import NotImplemented


# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1


# TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # The heuristic is the distance between crates and goals

    if problem.is_goal(state):
        # print("All crates are in goals")
        return 0

    if sokoban_deadlock_heuristic(state):
        # print("Deadlock")
        return weak_heuristic(problem, state)

    # Calculate heuristic as the distance between crates and goals
    return (
        max(
            manhattan_distance(crate, goal)
            for crate in state.crates
            for goal in problem.layout.goals
        )
        - 1
    )


def sokoban_deadlock_heuristic(state: SokobanState) -> bool:
    """
    A heuristic function to detect deadlocks in a Sokoban game.
    INPUT: a sokoban state
    OUTPUT: True if the state is a deadlock, False otherwise.
    """
    for crate in state.crates:
        x, y = crate.x, crate.y
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (
                Point(x + dx, y + dy) not in state.layout.goals
                and Point(x + dx, y + dy) not in state.layout.walkable
                and Point(x + dx, y + dy) in state.crates
                and Point(x + dx, y + dy) != state.player
                and x + dx >= 0
                and x + dx < state.layout.width
                and y + dy >= 0
                and y + dy < state.layout.height
            ):
                return True
    return False
