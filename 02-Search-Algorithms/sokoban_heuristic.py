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
        return 0
    # if state == problem.initial_state:
        # problem.cache()["count"] = 0
        # problem.cache()["is_deadlock"] = False

    if sokoban_deadlock_heuristic(state):
        # problem.cache()["count"] += 1
        # print(problem.cache()["count"])
        # print(state.__str__())
        return float("inf")
    # Calculate heuristic as the distance between crates and goals
    return min(
        manhattan_distance(crate, goal)
        for crate in state.crates
        for goal in problem.layout.goals
    ) + min(manhattan_distance(crate, state.player) for crate in state.crates)


def deadlock_on_corners(state: SokobanState):
    # deadlock on corners
    for crate in state.crates:
        x, y = crate.x, crate.y
        case1 = (
            Point(x, y - 1)
            not in state.layout.walkable
            # and Point(x, y - 1) not in state.layout.goals
        ) and (
            Point(x + 1, y)
            not in state.layout.walkable
            # and Point(x + 1, y) not in state.layout.goals
        )

        case2 = (
            Point(x, y + 1)
            not in state.layout.walkable
            # and Point(x, y + 1) not in state.layout.goals
        ) and (
            Point(x + 1, y)
            not in state.layout.walkable
            # and Point(x + 1, y) not in state.layout.goals
        )
        case3 = (
            Point(x, y - 1)
            not in state.layout.walkable
            # and Point(x, y - 1) not in state.layout.goals
        ) and (
            Point(x - 1, y)
            not in state.layout.walkable
            # and Point(x - 1, y) not in state.layout.goals
        )
        case4 = (
            Point(x, y + 1)
            not in state.layout.walkable
            # and Point(x, y + 1) not in state.layout.goals
        ) and (
            Point(x - 1, y)
            not in state.layout.walkable
            # and Point(x - 1, y) not in state.layout.goals
        )
        if case1 or case2 or case3 or case4:
            # print("Deadlock on corners")
            return True
    return False


def deadlock_on_wall(state: SokobanState):
    # check on deadlock if there is a wall at any side of the box and the nearest goal is not in the same row or column so the box can't be pushed to the goal
    for crate in state.crates:
        if crate in state.layout.goals:
            continue
        x, y = crate.x, crate.y
        # if there is a wall above or below the box
        if y == 1 or y == state.layout.height - 2:
            flag = True  # deadlock
            # loop through all the goals to check if there is a goal in the same row
            for goal in state.layout.goals:
                if goal.y == y and goal not in state.crates:
                    if flag and abs(goal.x - x) == 1:
                        flag = False
                        break
                    for i in range(min(x, goal.x) + 1, max(x, goal.x)):
                        if (
                            Point(i, y) in state.layout.walkable
                            or Point(i, y) in state.layout.goals
                        ) and Point(i, y) not in state.crates:
                            flag = False  # no deadlock
                        else:
                            flag = True  # deadlock
                            # break
            # print("can't go the goal1")
            return flag
            # if there is a wall on the left or right of the box
        if x == 1 or x == state.layout.width - 2:
            flag = True  # deadlock
            for goal in state.layout.goals:
                if goal.x == x and goal not in state.crates:
                    if flag and abs(goal.y - y) == 1:
                        flag = False
                        break
                    for i in range(min(y, goal.y) + 1, max(y, goal.y)):
                        if (
                            Point(x, i) in state.layout.walkable
                            or Point(x, i) in state.layout.goals
                        ) and Point(x, i) not in state.crates:
                            flag = False
                        else:
                            flag = True
                            # break
            # print("can't go the goal2")
            return flag
    return False


def deadlock_on_2x2(state: SokobanState):
    # imagine there are 4 2x2 squares of 4 cells around each crate
    # if all 4 cells are walls or boxes, then the crate is in a deadlock
    for crate in state.crates:
        for i in range(4):
            x0, y0, x1, y1 = crate.x, crate.y, crate.x, crate.y
            if i == 0:
                x0 -= 1
                y0 -= 1
            elif i == 1:
                x1 += 1
                y0 -= 1
            elif i == 2:
                x0 -= 1
                y1 += 1
            else:
                x1 += 1
                y1 += 1
            number_of_walls_and_boxes = 0
            # loop to count the number of walls and boxes in the 4 2x2 squares
            for i in range(x0, x1 + 1):
                for j in range(y0, y1 + 1):
                    if (
                        Point(i, j) not in state.layout.walkable
                        or Point(i, j) in state.crates
                    ):
                        number_of_walls_and_boxes += 1
            if number_of_walls_and_boxes >= 4:
                # print("Deadlock on 2x2")
                return True
    return False


def sokoban_deadlock_heuristic(state: SokobanState) -> bool:
    """
    A heuristic function to detect deadlocks in a Sokoban game.
    INPUT: a sokoban state
    OUTPUT: True if the state is a deadlock, False otherwise.
    """
    return (
        deadlock_on_corners(state) or deadlock_on_wall(state) or deadlock_on_2x2(state)
    )
