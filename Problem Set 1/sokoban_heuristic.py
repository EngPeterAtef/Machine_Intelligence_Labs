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
		print(problem.cache()["count"])
		return 0
	if state == problem.initial_state:
		problem.cache()["count"] = 0
        
	if sokoban_deadlock_heuristic(state):
		problem.cache()["count"] += 1
		print(problem.cache()["count"])
		# print("Deadlock")
		# print(state.__str__())
		return float("inf")

	# Calculate heuristic as the distance between crates and goals
	return min(
		manhattan_distance(crate, goal)
		for crate in state.crates
		for goal in problem.layout.goals
	) + min(manhattan_distance(crate, state.player) for crate in state.crates)


def sokoban_deadlock_heuristic(state: SokobanState) -> bool:
    """
    A heuristic function to detect deadlocks in a Sokoban game.
    INPUT: a sokoban state
    OUTPUT: True if the state is a deadlock, False otherwise.
    """
    # deadlock on corners
    for crate in state.crates:
        x, y = crate.x, crate.y
        if (Point(x, y - 1) not in state.layout.walkable) and (
            Point(x + 1, y) not in state.layout.walkable
        ):
            # print("Deadlock on corners")
            return True
        if (Point(x, y + 1) not in state.layout.walkable) and (
            Point(x + 1, y) not in state.layout.walkable
        ):
            # print("Deadlock on corners")
            return True
        if (Point(x, y - 1) not in state.layout.walkable) and (
            Point(x - 1, y) not in state.layout.walkable
        ):
            # print("Deadlock on corners")
            return True
        if (Point(x, y + 1) not in state.layout.walkable) and (
            Point(x - 1, y) not in state.layout.walkable
        ):
            # print("Deadlock on corners")
            return True

    # check on deadlock if there is a wall at any side of the box and the nearest goal is not in the same row or column so the box can't be pushed to the goal
    for crate in state.crates:
        x, y = crate.x, crate.y
        if (
            Point(x, y - 1) not in state.layout.walkable
            or Point(x, y + 1) not in state.layout.walkable
        ):
            # print("can't go the goal")
            return all(goal.y != y for goal in state.layout.goals)
        if (
            Point(x - 1, y) not in state.layout.walkable
            or Point(x + 1, y) not in state.layout.walkable
        ):
            # print("can't go the goal")
            return all(goal.x != x for goal in state.layout.goals)

    # imagine there are 4 2x2 squares of 4 cells around each crate
    # if all 4 cells are walls or boxes, then the crate is in a deadlock
    for crate in state.crates:
        x, y = crate.x, crate.y
        # the crate is at the buttom right of the box and check on the 3 other locations
        if (
            (
                Point(x - 1, y) not in state.layout.walkable
                or Point(x - 1, y) in state.crates
            )
            and (
                Point(x - 1, y + 1) not in state.layout.walkable
                or Point(x - 1, y + 1) in state.crates
            )
            and (
                Point(x, y + 1) not in state.layout.walkable
                or Point(x, y + 1) in state.crates
            )
        ):
            # print("buttom right")
            return True
            # the crate is at the buttom left of the box and check on the 3 other locations
        if (
            (
                Point(x + 1, y) not in state.layout.walkable
                or Point(x + 1, y) in state.crates
            )
            and (
                Point(x + 1, y + 1) not in state.layout.walkable
                or Point(x + 1, y + 1) in state.crates
            )
            and (
                Point(x, y + 1) not in state.layout.walkable
                or Point(x, y + 1) in state.crates
            )
        ):
            # print("buttom left")
            return True
            # the crate is at the top right of the box and check on the 3 other locations
        if (
            (
                Point(x - 1, y) not in state.layout.walkable
                or Point(x - 1, y) in state.crates
            )
            and (
                Point(x - 1, y - 1) not in state.layout.walkable
                or Point(x - 1, y - 1) in state.crates
            )
            and (
                Point(x, y - 1) not in state.layout.walkable
                or Point(x, y - 1) in state.crates
            )
        ):
            # print("top right")
            return True
            # the crate is at the top left of the box and check on the 3 other locations
        if (
            (
                Point(x + 1, y) not in state.layout.walkable
                or Point(x + 1, y) in state.crates
            )
            and (
                Point(x + 1, y - 1) not in state.layout.walkable
                or Point(x + 1, y - 1) in state.crates
            )
            and (
                Point(x, y - 1) not in state.layout.walkable
                or Point(x, y - 1) in state.crates
            )
        ):
            # print("top left")
            return True

    # deadlock on walls	or boxes
    for crate in state.crates:
        x, y = crate.x, crate.y
        if (
            (
                Point(x, y - 1) not in state.layout.walkable
                or Point(x, y - 1) in state.crates
            )
            and (
                Point(x, y + 1) not in state.layout.walkable
                or Point(x, y + 1) in state.crates
            )
            and (
                Point(x + 1, y) not in state.layout.walkable
                or Point(x + 1, y) in state.crates
            )
            and (
                Point(x - 1, y) not in state.layout.walkable
                or Point(x - 1, y) in state.crates
            )
        ):
            # print("Deadlock on walls or boxes")
            return True

    return False

