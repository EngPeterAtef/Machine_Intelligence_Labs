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

        LHS0_REVERSED = LHS0[::-1]
        LHS1_REVERSED = LHS1[::-1]
        RHS_REVERSED = RHS[::-1]

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        problem.variables = []
        for letter in LHS0_REVERSED + LHS1_REVERSED + RHS_REVERSED:
            if letter not in problem.variables:
                problem.variables.append(letter)

        # the number of carries is the number of letters in the longer string
        for i in range(len(RHS) - 1):
            # add the carry variables
            problem.variables.append("C" + str(i))
            # add auxiliary variables consisting of the RHS letters and carry variables
            problem.variables.append("C" + str(i) + RHS_REVERSED[i])

        # IMPORTANT NOTE: You can only add unary and binary constraints. So, you are allowed to add auxiliary
        # variables to solve this problem. But make sure the there is a variable for each letter in the puzzle. So if you
        # combine the letters A and B into an auxiliary variable AB, you still have to include A and B in your variables list.

        # adding auxiliary variables
        problem.variables.append(
            LHS0_REVERSED[0] + LHS1_REVERSED[0]
        )  # combine the first letters of the two strings without carry
        for i in range(1, min(len(LHS0), len(LHS1))):
            # combine the letters of the two strings without carry
            problem.variables.append(LHS0_REVERSED[i] + LHS1_REVERSED[i])
            # combine the letters of the two strings with carry
            problem.variables.append(
                LHS0_REVERSED[i] + LHS1_REVERSED[i] + "C" + str(i - 1)
            )

        if len(LHS0) > len(LHS1):
            # combine the letters of the two strings with carry
            problem.variables.append(LHS0_REVERSED[-1] + "C" + str(len(LHS1) - 1))
        elif len(LHS0) < len(LHS1):
            # combine the letters of the two strings with carry
            problem.variables.append(LHS1_REVERSED[-1] + "C" + str(len(LHS0) - 1))

        # print("problem.variables", problem.variables)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        problem.domains = {}
        for letter in problem.variables:
            # domian of carries Ci should be {0, 1}
            if letter[0] == "C" and len(letter) == 2 and letter[1].isnumeric():
                problem.domains[letter] = set(range(2))
                continue
            elif len(letter) == 1:  # domain of letters should be {0, 1, ..., 9}
                problem.domains[letter] = set(range(10))
                continue
            # add domain for the auxiliary variables. it should be pairs of the domain of the two letters
            # the domain of the auxiliary AB should be {domain of A, domain of B}
            if len(letter) > 2:  # BDC0 / C1H / AC1
                problem.domains[letter] = set()
                max_value_in_domain = ""
                for i in range(len(letter)):
                    # character 3adi
                    if (
                        letter[i].isalpha()
                        and i < len(letter) - 1
                        and letter[i + 1].isalpha()
                    ):
                        max_value_in_domain += str(max(problem.domains[letter[i]]))
                        # character bs fe a5er al letter
                    elif letter[i].isalpha() and i == len(letter) - 1:
                        max_value_in_domain += str(max(problem.domains[letter[i]]))
                    # if carry
                    elif (
                        letter[i].isalpha()
                        and i < len(letter) - 1
                        and letter[i + 1].isnumeric()
                    ):
                        max_value_in_domain += str(
                            max(problem.domains[letter[i] + letter[i + 1]])
                        )  # Carry inside auxiliary variable
                problem.domains[letter] = set(range(int(max_value_in_domain) + 1))
            elif len(letter) == 2:
                problem.domains[letter] = set()
                max_value_in_domain = ""
                for i in range(len(letter)):
                    if letter[i].isalpha():
                        max_value_in_domain += str(max(problem.domains[letter[i]]))
                problem.domains[letter] = set(range(int(max_value_in_domain) + 1))

        # for k, v in problem.domains.items():
        #     print(k, max(v))
        #     print("domain size",len(v))
        #     # print("the domain",v)
        #     print("-----------------------------------------------")
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        problem.constraints = []
        """
        Example:
            A B C
        +     D E
        ---------
        F G H I
        ---------
        C + E = I + 10 * C0
        B + D + C0 = H + 10 * C1
        A + C1 = G + 10 * C2
        F = C2
        """
        # The first letter in each string cannot be 0
        problem.constraints.append(
            UnaryConstraint(LHS0_REVERSED[-1], lambda x: x != 0)
        )  # A != 0
        problem.constraints.append(
            UnaryConstraint(LHS1_REVERSED[-1], lambda x: x != 0)
        )  # D != 0
        problem.constraints.append(
            UnaryConstraint(RHS_REVERSED[-1], lambda x: x != 0)
        )  # F != 0

        # Each letter is assigned a unique number (no two letters are assigned the same number).
        for i in range(len(problem.variables)):
            for j in range(i + 1, len(problem.variables)):
                if len(problem.variables[i]) == 1 and len(problem.variables[j]) == 1:
                    problem.constraints.append(
                        BinaryConstraint(
                            (problem.variables[i], problem.variables[j]),
                            lambda x, y: x != y,
                        )
                    )

        # constraints for the auxiliary variables
        problem.constraints.append(
            BinaryConstraint(
                (LHS0_REVERSED[0], LHS0_REVERSED[0] + LHS1_REVERSED[0]),  # C = CE[0]
                lambda x, y: x == y // 10,
            )
        )
        problem.constraints.append(
            BinaryConstraint(
                (LHS1_REVERSED[0], LHS0_REVERSED[0] + LHS1_REVERSED[0]),  # E = CE[1]
                lambda x, y: x == y % 10,
            )
        )
        problem.constraints.append(
            BinaryConstraint(
                (
                    RHS_REVERSED[0],
                    "C" + str(0) + RHS_REVERSED[0],
                ),
                lambda x, y: x == y % 10,
            )
        )
        # C1 = C1H // 10
        problem.constraints.append(
            BinaryConstraint(
                (
                    "C" + str(0),
                    "C" + str(0) + RHS_REVERSED[0],
                ),
                lambda x, y: x == y // 10,
            )
        )
        # CE == C0I
        problem.constraints.append(
            BinaryConstraint(
                (
                    LHS0_REVERSED[0] + LHS1_REVERSED[0],
                    "C" + str(0) + RHS_REVERSED[0],
                ),
                lambda x, y: ((x // 10) + (x % 10)) == ((y // 10) * 10 + (y % 10)),
            )
        )

        for i in range(
            1, min(len(LHS0), len(LHS1))
        ):  # loop over the shorter string (range(1, 2))
            # B = BD // 10
            problem.constraints.append(
                BinaryConstraint(
                    (
                        LHS0_REVERSED[i],
                        LHS0_REVERSED[i] + LHS1_REVERSED[i],
                    ),
                    lambda x, y: x == y // 10,
                )
            )
            # D = BD % 10
            problem.constraints.append(
                BinaryConstraint(
                    (
                        LHS1_REVERSED[i],
                        LHS0_REVERSED[i] + LHS1_REVERSED[i],
                    ),
                    lambda x, y: x == y % 10,
                )
            )
            # BD = BDC0 // 10
            problem.constraints.append(
                BinaryConstraint(
                    (
                        LHS0_REVERSED[i] + LHS1_REVERSED[i],
                        LHS0_REVERSED[i] + LHS1_REVERSED[i] + "C" + str(i - 1),
                    ),
                    lambda x, y: x == y // 10,
                )
            )
            # C0 = BDC0 % 10
            problem.constraints.append(
                BinaryConstraint(
                    (
                        "C" + str(i - 1),
                        LHS0_REVERSED[i] + LHS1_REVERSED[i] + "C" + str(i - 1),
                    ),
                    lambda x, y: x == y % 10,
                )
            )
            # H =  C1H % 10
            problem.constraints.append(
                BinaryConstraint(
                    (
                        RHS_REVERSED[i],
                        "C" + str(i) + RHS_REVERSED[i],
                    ),
                    lambda x, y: x == y % 10,
                )
            )
            # C1 = C1H // 10
            problem.constraints.append(
                BinaryConstraint(
                    (
                        "C" + str(i),
                        "C" + str(i) + RHS_REVERSED[i],
                    ),
                    lambda x, y: x == y // 10,
                )
            )
            # BDC0 == C1H
            problem.constraints.append(
                BinaryConstraint(
                    (
                        LHS0_REVERSED[i] + LHS1_REVERSED[i] + "C" + str(i - 1),
                        "C" + str(i) + RHS_REVERSED[i],
                    ),
                    lambda x, y: (
                        (x // 100) + ((x - (x // 100) * 100) // 10) + (x % 10)
                    )
                    == ((y // 10) * 10 + (y % 10)),
                )
            )

        # A + C1 = G + 10 * C2
        for i in range(min(len(LHS0), len(LHS1)), max(len(LHS0), len(LHS1))):
            if len(LHS0) > len(LHS1):
                # A = AC1 // 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            LHS0_REVERSED[i],
                            LHS0_REVERSED[i] + "C" + str(i - 1),
                        ),
                        lambda x, y: x == y // 10,
                    )
                )
                # C1 = AC1 % 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            "C" + str(i - 1),
                            LHS0_REVERSED[i] + "C" + str(i - 1),
                        ),
                        lambda x, y: x == y % 10,
                    )
                )
                # G = C2G % 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            RHS_REVERSED[i],
                            "C" + str(i) + RHS_REVERSED[i],
                        ),
                        lambda x, y: x == y % 10,
                    )
                )
                # C2 = C2G // 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            "C" + str(i),
                            "C" + str(i) + RHS_REVERSED[i],
                        ),
                        lambda x, y: x == y // 10,
                    )
                )
                # AC1 == C2G
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            LHS0_REVERSED[i] + "C" + str(i - 1),
                            "C" + str(i) + RHS_REVERSED[i],
                        ),
                        lambda x, y: ((x // 10) + (x % 10))
                        == ((y // 10) * 10 + (y % 10)),
                    )
                )
            else:
                # A = AC1 // 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            LHS1_REVERSED[i],
                            LHS1_REVERSED[i] + "C" + str(i - 1),
                        ),
                        lambda x, y: x == y // 10,
                    )
                )
                # C1 = AC1 % 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            "C" + str(i - 1),
                            LHS1_REVERSED[i] + "C" + str(i - 1),
                        ),
                        lambda x, y: x == y % 10,
                    )
                )
                # G = C2G % 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            RHS_REVERSED[i],
                            "C" + str(i) + RHS_REVERSED[i],
                        ),
                        lambda x, y: x == y % 10,
                    )
                )
                # C2 = C2G // 10
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            "C" + str(i),
                            "C" + str(i) + RHS_REVERSED[i],
                        ),
                        lambda x, y: x == y // 10,
                    )
                )
                # AC1 == C2G
                problem.constraints.append(
                    BinaryConstraint(
                        (
                            LHS1_REVERSED[i] + "C" + str(i - 1),
                            "C" + str(i) + RHS_REVERSED[i],
                        ),
                        lambda x, y: ((x // 10) + (x % 10))
                        == ((y // 10) * 10 + (y % 10)),
                    )
                )

        # F = C2
        problem.constraints.append(
            BinaryConstraint(
                (
                    RHS_REVERSED[-1],
                    "C" + str(len(RHS) - 2),
                ),
                lambda x, y: x == y,
            )
        )
        # for c in problem.constraints:
        #     # if unary constraint
        #     if isinstance(c, UnaryConstraint):
        #         print("UnaryConstraint", c.variable)

        #     # if binary constraint
        #     elif isinstance(c, BinaryConstraint):
        #         print("BinaryConstraint", c.variables)

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, "r") as f:
            return CryptArithmeticProblem.from_text(f.read())
