from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import heapq


class CustomPriorityQueue:
    def __init__(self):
        self.elements = []
        self.counter = 0  # Used to break ties in priorities

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, self.counter, item))
        self.counter += 1

    def pop(self):
        if not self.is_empty():
            return heapq.heappop(self.elements)

    def pushpop(self, item, priority):
        return heapq.heappushpop(self.elements, (priority, self.counter, item))

    def is_empty(self):
        return len(self.elements) == 0

    def getItem(self, item):
        for i in self.elements:
            if i[2] == item:
                return i
        return None


# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    if problem.is_goal(initial_state):
        return []
    # Queue of nodes and the actions needed to reach them
    frontier = deque()
    frontier.append((initial_state, []))
    # Set of explored nodes
    explored = set()
    # While there are nodes to explore
    while frontier:
        # Get the next node
        node, actions = frontier.popleft()
        # add to the explored set
        explored.add(node)
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # If the child is not explored and not in the frontier
            if child not in explored and child not in [i[0] for i in frontier]:
                # If the child is the goal
                if problem.is_goal(child):
                    return actions + [action]
                # Add the child to the frontier and actions needed to reach it
                frontier.append((child, actions + [action]))
    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    if problem.is_goal(initial_state):
        return []
    # Stack of nodes and the actions needed to reach them
    frontier = deque()
    frontier.append((initial_state, []))
    # Set of explored nodes
    explored = set()
    # While there are nodes to explore
    while frontier:
        # Get the next node
        node, actions = frontier.pop()
        # If the node is the goal
        if problem.is_goal(node):
            return actions
        # add to the explored set
        explored.add(node)
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # If the child is not explored and not in the frontier
            if child not in explored and child not in [i[0] for i in frontier]:
                # Add the child to the frontier and actions needed to reach it
                frontier.append((child, actions + [action]))
    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    if problem.is_goal(initial_state):
        return []
    # Queue of nodes and the actions needed to reach them
    frontier = CustomPriorityQueue()
    frontier.push((initial_state, []), 0)
    # Set of explored nodes
    explored = set()
    # While there are nodes to explore
    while frontier:
        # Get the next node
        res = frontier.pop()
        if not res:
            return None
        (c, _, (node, actions)) = res
        # If the node is the goal
        if problem.is_goal(node):
            return actions
        # add to the explored set
        explored.add(node)
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # calculate the action cost
            action_cost = problem.get_cost(node, action)
            # search for the child in the frontier
            old_child = None
            for i in frontier.elements:
                if i[2][0] == child:
                    old_child = i  # (cost , counter , (node, actions))
                    break
            # If the child is not explored and not in the frontier
            if child not in explored and not old_child:
                # Add the child to the frontier and actions needed to reach it
                frontier.push(
                    (child, actions + [action]),
                    action_cost + c,
                )
            elif old_child:
                if old_child[0] > action_cost + c:
                    frontier.elements.remove(old_child)
                    heapq.heapify(frontier.elements)
                    frontier.push(
                        (child, actions + [action]),
                        action_cost + c,
                    )
    return None


def AStarSearch(
    problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction
) -> Solution:
    # TODO: ADD YOUR CODE HERE
    if problem.is_goal(initial_state):
        return []
    # Queue of nodes and the actions needed to reach them
    frontier = CustomPriorityQueue()
    frontier.push((initial_state, []), 0 + heuristic(problem, initial_state))
    # Set of explored nodes
    explored = set()
    # While there are nodes to explore
    while frontier:
        # Get the next node
        res = frontier.pop()
        if not res:
            return None
        (c, _, (node, actions)) = res
        # If the node is the goal
        if problem.is_goal(node):
            return actions
        # add to the explored set
        explored.add(node)
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # calculate the action cost
            action_cost = problem.get_cost(node, action)
            # search for the child in the frontier
            old_child = None
            for i in frontier.elements:
                if i[2][0] == child:
                    old_child = i  # (cost , counter , (node, actions))
                    break
            # calculate the child cost = action cost + cost to reach the child + heuristic
            child_cost = action_cost + c + heuristic(problem, child) - heuristic(problem, node)
            # If the child is not explored and not in the frontier
            if child not in explored and not old_child:
                # Add the child to the frontier and actions needed to reach it
                frontier.push(
                    (child, actions + [action]),
                    child_cost,
                )
            elif old_child:
                if old_child[0] > child_cost:
                    frontier.elements.remove(old_child)
                    heapq.heapify(frontier.elements)
                    frontier.push(
                        (child, actions + [action]),
                        child_cost,
                    )
    return None


def BestFirstSearch(
    problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction
) -> Solution:
    # TODO: ADD YOUR CODE HERE
    if problem.is_goal(initial_state):
        return []
    # Queue of nodes and the actions needed to reach them
    frontier = CustomPriorityQueue()
    frontier.push((initial_state, []), heuristic(problem, initial_state))
    # Set of explored nodes
    explored = set()
    # While there are nodes to explore
    while frontier:
        # Get the next node
        res = frontier.pop()
        if not res:
            return None
        (_, _, (node, actions)) = res
        # If the node is the goal
        if problem.is_goal(node):
            return actions
        # add to the explored set
        explored.add(node)
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # calculate the heuristic cost
            child_cost = heuristic(problem, child)
            # search for the child in the frontier
            old_child = None
            for i in frontier.elements:
                if i[2][0] == child:
                    old_child = i  # (cost , counter , (node, actions))
                    break
            # If the child is not explored and not in the frontier
            if child not in explored and not old_child:
                # Add the child to the frontier and actions needed to reach it
                frontier.push(
                    (child, actions + [action]),
                    child_cost,
                )
            elif old_child:
                if old_child[0] > child_cost:
                    frontier.elements.remove(old_child)
                    heapq.heapify(frontier.elements)
                    frontier.push(
                        (child, actions + [action]),
                        child_cost,
                    )
    return None

