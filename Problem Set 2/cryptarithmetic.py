from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

# TODO (Optional): Import any builtin library or define any helper function you want to use


# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> "CryptArithmeticProblem":
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i + 1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        problem.variables = []
        for letter in LHS0 + LHS1 + RHS:
            if letter not in problem.variables:
                problem.variables.append(letter)

        # the number of carries is the number of letters in the longer string
        for i in range(len(RHS) - 1):
            problem.variables.append("C" + str(i))

        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        problem.domains = {}
        for letter in problem.variables:
            problem.domains[letter] = set(range(10))

        # the domain of the carry variables should be {0, 1}
        for i in range(len(RHS) - 1):
            problem.domains["C" + str(i)] = set(range(2))

        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        problem.constraints = []
        # The first letter in each string cannot be 0
        problem.constraints.append(UnaryConstraint(LHS0[0], lambda x: x != 0))
        problem.constraints.append(UnaryConstraint(LHS1[0], lambda x: x != 0))
        problem.constraints.append(UnaryConstraint(RHS[0], lambda x: x != 0))

        # Each letter is assigned a unique number (no two letters are assigned the same number).
        for i in range(len(problem.variables)):
            for j in range(i + 1, len(problem.variables)):
                problem.constraints.append(
                    BinaryConstraint(
                        (problem.variables[i], problem.variables[j]),
                        lambda x, y: x != y,
                    )
                )
        # the equations are constructed by adding the corresponding letters and carry variables
        # the carry variables are added to the front of the list
        # reverse the lists so that the first letter is the last element in the list
        LHS0 = list(LHS0)
        LHS0.reverse()
        LHS1 = list(LHS1)
        LHS1.reverse()
        RHS = list(RHS)
        RHS.reverse()

        # IMPORTANT NOTE: You can only add unary and binary constraints. So, you are allowed to add auxiliary
        # variables to solve this problem. But make sure the there is a variable for each letter in the puzzle. So if you
        # combine the letters A and B into an auxiliary variable AB, you still have to include A and B in your variables list.

        # add the first two letters together (no carry)
        problem.constraints.append(
            BinaryConstraint((LHS0[0], LHS1[0]), lambda x, y: x + y == RHS[0])
        )
        # add the rest of the letters together (with carry)
        # loop over the shorter string
        for i in range(1, min(len(LHS0), len(LHS1))):
            problem.constraints.append(
                BinaryConstraint((LHS0[i], LHS1[i]), lambda x, y: x + y == RHS[i])
            )

        # loop over the difference between the lengths of the two strings
        for i in range(min(len(LHS0), len(LHS1)), max(len(LHS0), len(LHS1))):
            problem.constraints.append(
                BinaryConstraint(
                    (LHS1[i], "C" + str(i - 1)), lambda x, y: x + y == RHS[i]
                )
            )

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, "r") as f:
            return CryptArithmeticProblem.from_text(f.read())
