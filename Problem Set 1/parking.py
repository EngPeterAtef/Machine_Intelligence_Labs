from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# TODO: (Optional) Instead of Any, you can define a type for the parking state
# 2d matrix of chars
ParkingState = List[List[str]]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]


# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[
        Point
    ]  # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]  # A tuple of points where state[i] is the position of car 'i'.
    slots: Dict[
        Point, int
    ]  # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the slot of car 'i') for every position.
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int  # The width of the parking lot.
    height: int  # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        initState = [["#" for i in range(self.width)] for j in range(self.height)]
        # loop over the passage
        for p in self.passages:
            # check if this point is a parking slot
            if p in self.slots.keys():
                initState[p.y][p.x] = self.slots[p]
            elif p in self.cars:  # check if this point is a car
                initState[p.y][p.x] = chr(self.cars.index(p) + ord("A"))
            else:  # this point is an empty slot
                initState[p.y][p.x] = "."
        return initState

    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # TODO: ADD YOUR CODE HERE
        for i in range(len(self.cars)):
            # get the car character
            car_letter = chr(i + ord("A"))
            # get the current position of the car
            car_coordinates = self.find_element_indices(state, car_letter)
            car_position = Point(car_coordinates[1], car_coordinates[0])
            if car_position not in self.slots.keys() or (
                car_position in self.slots.keys()
                and state[car_position.y][car_position.x]
                != chr(self.slots[car_position] + ord("A"))
            ):
                return False
        return True

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # TODO: ADD YOUR CODE HERE
        actions = []
        for i in range(len(self.cars)):
            car_letter = chr(i + ord("A"))
            # get the current position of the car
            car_coordinates = self.find_element_indices(state, car_letter)
            car_position = Point(car_coordinates[1], car_coordinates[0])
            for direction in Direction:
                new_position = car_position + direction.to_vector()
                if (
                    state[new_position.y][new_position.x] == "."
                    or state[new_position.y][new_position.x] == 0
                    or state[new_position.y][new_position.x] == 1
                    or state[new_position.y][new_position.x] == 2
                    or state[new_position.y][new_position.x] == 3
                    or state[new_position.y][new_position.x] == 4
                    or state[new_position.y][new_position.x] == 5
                    or state[new_position.y][new_position.x] == 6
                    or state[new_position.y][new_position.x] == 7
                    or state[new_position.y][new_position.x] == 8
                    or state[new_position.y][new_position.x] == 9
                ):
                    actions.append((i, direction))
        return actions

    # this a utility function to get the index of an char in 2D list
    def find_element_indices(self, my_list, element):
        for i, row in enumerate(my_list):
            for j, value in enumerate(row):
                if value == element:
                    return (i, j)
        return None

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        # get the car character
        car_letter = chr(action[0] + ord("A"))
        # get the current position of the car
        car_coordinates = self.find_element_indices(state, car_letter)
        car_position = Point(car_coordinates[1], car_coordinates[0])
        new_position = car_position + action[1].to_vector()
        # check if the car_position was in the slot dictionary to
        if car_position in self.slots.keys():
            state[car_position.y][car_position.x] = self.slots[car_position]
        else:
            state[car_position.y][car_position.x] = "."
        state[new_position.y][new_position.x] = chr(action[0] + ord("A"))
        return state

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # TODO: ADD YOUR CODE HERE
        # get the car character
        car_letter = chr(action[0] + ord("A"))
        # calc the cost depending on the rank
        cost = 91 - ord(car_letter)
        # get the current position of the car
        car_coordinates = self.find_element_indices(state, car_letter)
        car_position = Point(car_coordinates[1], car_coordinates[0])
        # get the new position of the car
        new_position = car_position + action[1].to_vector()
        # check if this new position is a slot and if it is not the same slot of the car
        if new_position in self.slots.keys() and action[0] != self.slots[new_position]:
            cost += 100
        return cost

    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> "ParkingProblem":
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            # print("line: ",line)
            for x, char in enumerate(line):
                # print("x = ",x,"y = ",y)
                if char != "#":
                    passages.add(Point(x, y))
                    if char == ".":
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord("A")] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> "ParkingProblem":
        with open(path, "r") as f:
            return ParkingProblem.from_text(f.read())


obj = ParkingProblem.from_file("./parks/park1.txt")
s = obj.get_initial_state()
print(s)
# print(obj.slots)
print(obj.get_actions(s))
cost = obj.get_cost(s, (0, Direction(1)))
# cost += obj.get_cost(s, (1, Direction(0)))
print(cost)
s1 = obj.get_successor(s, (0, Direction(0)))
print(s1)
print(obj.is_goal(s1))
print(obj.get_actions(s1))
s2 = obj.get_successor(s1, (0, Direction(0)))
print(s2)

# while not obj.is_goal(s):
#     print(s)
#     print("-------------------------------------")
