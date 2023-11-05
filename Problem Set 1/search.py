from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    node = initial_state
    if problem.is_goal(node):
        return []
    # List of actions
    actions = []
    # Queue of nodes
    frontier = deque()
    frontier.append(node)
    # Set of explored nodes
    explored = set()
    explored.add(node)
    # While there are nodes to explore
    while frontier:
        # Get the next node
        node = frontier.popleft()
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # If the child is not explored
            if child not in explored:
                # If the child is the goal
                if problem.is_goal(child):
                    actions.append(action)
                    return actions
                # Add the child to the frontier and explored
                frontier.append(child)
                explored.add(child)
                actions.append(action)
    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    node = initial_state
    if problem.is_goal(node):
        return []
    # List of actions
    actions = []
    # Stack of nodes
    frontier = deque()
    frontier.append(node)
    # Set of explored nodes
    explored = set()
    explored.add(node)
    # While there are nodes to explore
    while frontier:
        # Get the next node
        node = frontier.pop()
        # For each action in the problem
        for action in problem.get_actions(node):
            # Get the child node
            child = problem.get_successor(node, action)
            # If the child is not explored
            if child not in explored:
                # If the child is the goal
                if problem.is_goal(child):
                    actions.append(action)
                    return actions
                # Add the child to the frontier and explored
                frontier.append(child)
                explored.add(child)
                actions.append(action)
    return None



def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()


def AStarSearch(
    problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction
) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()


def BestFirstSearch(
    problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction
) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()
