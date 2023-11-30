from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented


# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {
            value for value in problem.domains[variable] if constraint.condition(value)
        }
        problem.domains[variable] = new_domain
        if not new_domain:
            solvable = False
            break
    problem.constraints = remaining_constraints
    return solvable


# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic,
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min(
        (len(domains[variable]), index, variable)
        for index, variable in enumerate(problem.variables)
        if variable in domains
    )
    return variable


# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned variables.
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.
def forward_checking(
    problem: Problem,
    assigned_variable: str,
    assigned_value: Any,
    domains: Dict[str, set],
) -> bool:
    # TODO: Write this function
    solvable = True
    for constraint in problem.constraints:
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:

            # get the other variable
            other_variable = constraint.get_other(assigned_variable)

            # if the the other varaible is assigned so it will not be inside the domains so continue
            if other_variable not in domains.keys():
                continue

            # update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
            new_domain = {
                value
                for value in domains[other_variable]
                if constraint.condition(assigned_value, value)
            }
            domains[other_variable] = new_domain

            # if the domain of the other variable is empty, return False => the problem is not solvable 
            if not new_domain:
                solvable = False
                break
    return solvable


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic,
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(
    problem: Problem, variable_to_assign: str, domains: Dict[str, set]
) -> List[Any]:
    # TODO: Write this function
    # keep the count of the removed values for each value in the domain of the variable to assign
    removed_values = {}

    # initialize the removed values to 0
    for value in domains[variable_to_assign]:
        removed_values[value] = 0

    # loop over the values in the domain of the variable to assign to count the removed values for each value
    for value in domains[variable_to_assign]:
        # loop over the constraints to apply binary constraints for each value
        for constraint in problem.constraints:
            # check only for binary constraints and the variable to assign is in this constraint
            if (
                isinstance(constraint, BinaryConstraint)
                and variable_to_assign in constraint.variables
            ):
                # get the other variable that is involved in this constraint
                other_variable = constraint.get_other(variable_to_assign)

                # if the other variable has no domain (it is already assigned), skip this constraint
                if other_variable not in domains:
                    continue

                # loop over the values in the domain of the other variable
                for other_value in domains[other_variable]:
                    # create an assignment that includes the variable to assign with the value from its domain
                    # and the other variable with the value from its domain
                    assignment = {
                        variable_to_assign: value,
                        other_variable: other_value,
                    }

                    # check if the assignment satisfies the binary constraint
                    if not constraint.is_satisfied(assignment):
                        # if it does not, increase the count of the removed values for this value
                        removed_values[value] += 1

    # sort values by number of removed values in ascending order and by alphabetical order in case of tie
    return sorted(removed_values, key=lambda x: (removed_values[x], x))


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    # TODO: Write this function
    # create initial empty assignment for the variables
    assignment = {}

    # do the 1-consistency check
    if not one_consistency(problem):
        # if the problem is not 1-consistent, return None
        return None

    def recursive_search(
        assignment: Assignment, domains: Dict[str, set]
    ) -> Optional[Assignment]:
        # check if the assignment is complete
        if problem.is_complete(assignment):
            # if it is, return the assignment
            return assignment

        # get the next variable to assign using the MRV heuristic
        variable = minimum_remaining_values(problem, domains)

        # get the values for this variable in the domain using the least restraining value heuristic
        for value in least_restraining_values(problem, variable, domains):
            # create a copy of the assignment to not modify the original assignment as it is passed by reference
            new_assignmet = assignment.copy()

            # add the value to to the variable in the new assignment
            new_assignmet[variable] = value

            # create a copy of the domains to use in the forward checking because it will be passed by reference
            new_domains = domains.copy()

            # delete the varaible from the domains copy as it is assigned
            del new_domains[variable]

            # check if the forward checking is satisfied
            if forward_checking(problem, variable, value, new_domains):
                # if it is, call the recursive search with the new assignment and the new domains
                result = recursive_search(new_assignmet, new_domains)

                # check if the result is not None
                if result is not None:
                    # if it is not, return the result as it is the first solution found
                    return result

        # if no solution was found, return None
        return None

    # call the recursive search with the initial empty assignment and the domains
    return recursive_search(assignment, problem.domains)
