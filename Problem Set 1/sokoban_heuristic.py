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
    flag = True
    for crate in state.crates:
        if crate not in state.layout.goals:
            flag = False

    if flag:
        # print("All crates are in goals")
        return 0

    if sokoban_deadlock_heuristic(state):
        # print("Deadlock")
        weak_heuristic(problem, state)

    # Calculate heuristic as the distance between crates and goals
    return (
        max(
            manhattan_distance(crate, goal)
            for crate in state.crates
            for goal in problem.layout.goals
        )
        - 1
    )


def sokoban_deadlock_heuristic(state: SokobanState):
    """
    A heuristic function to detect deadlocks in a Sokoban game.
    INPUT: a sokoban state
    OUTPUT: True if the state is a deadlock, False otherwise.
    """
    # Check for dead square deadlocks
    for box in state.crates:
        if (
            (box.x + 1, box.y) not in state.layout.walkable
            and (box.x, box.y + 1) not in state.layout.walkable
            and (box.x + 1, box.y + 1) not in state.layout.walkable
        ):
            return True
        if (
            (box.x - 1, box.y) not in state.layout.walkable
            and (box.x, box.y + 1) not in state.layout.walkable
            and (box.x - 1, box.y + 1) not in state.layout.walkable
        ):
            return True
        if (
            (box.x + 1, box.y) not in state.layout.walkable
            and (box.x, box.y - 1) not in state.layout.walkable
            and (box.x + 1, box.y - 1) not in state.layout.walkable
        ):
            return True
        if (
            (box.x - 1, box.y) not in state.layout.walkable
            and (box.x, box.y - 1) not in state.layout.walkable
            and (box.x - 1, box.y - 1) not in state.layout.walkable
        ):
            return True
    # Check for freeze deadlocks
    if box not in state.layout.goals and all(
        (box.x + dx, box.y + dy) not in state.layout.walkable
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
    ):
        return True
    # Check for corral deadlocks
    if box not in state.layout.goals and all(
        (box.x + dx, box.y + dy) not in state.layout.walkable
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
    ):
        if all(
            any(
                (box.x + dx, box.y + dy) in state.layout.goals
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
            )
            for box in state.crates
        ):
            return True

    # Check for closed diagonal deadlocks
    if box not in state.layout.goals and all(
        (box.x + dx, box.y + dy) not in state.layout.walkable
        for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1))
    ):
        if all(
            (box.x + dx, box.y) not in state.layout.walkable
            and (box.x, box.y + dy) not in state.layout.walkable
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ):
            return True

    # Check for bipartite deadlocks
    if box not in state.layout.goals:
        if all(
            (box.x + dx, box.y + dy) not in state.layout.walkable
            for dx, dy in ((0, 1), (0, -1))
        ):
            if any((box.x + dx, box.y) in state.layout.goals for dx in (-1, 1)):
                return True
        if all(
            (box.x + dx, box.y + dy) not in state.layout.walkable
            for dx, dy in ((1, 0), (-1, 0))
        ):
            if any((box.x, box.y + dy) in state.layout.goals for dy in (-1, 1)):
                return True
