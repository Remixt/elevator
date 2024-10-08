import sys
from enum import Enum

FLOOR_TRAVEL_TIME = 10  # seconds

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    def __init__(self, start_floor):
        self.current_floor = start_floor
        self.direction = Direction.IDLE
        self.destinations = set()

    def add_destination(self, floor):
        self.destinations.add(floor)
        if self.direction == Direction.IDLE:
            self._set_initial_direction(floor)

    def _set_initial_direction(self, first_destination):
        if first_destination > self.current_floor:
            self.direction = Direction.UP
        elif first_destination < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

    def move(self):
        if not self.destinations:
            self.direction = Direction.IDLE
            return False

        # Handle same-floor destination without moving
        if self.current_floor in self.destinations:
            self.destinations.remove(self.current_floor)
            return True  # Doors open; elevator doesn't move.

        next_floor = None
        if self.direction == Direction.UP:
            # Select the closest floor above the current floor
            floors_in_direction = [floor for floor in self.destinations if floor > self.current_floor]
            if floors_in_direction:
                next_floor = min(floors_in_direction, key=lambda f: f - self.current_floor)
            else:
                self.direction = Direction.DOWN
                return self.move()
        elif self.direction == Direction.DOWN:
            # Select the closest floor below the current floor
            floors_in_direction = [floor for floor in self.destinations if floor < self.current_floor]
            if floors_in_direction:
                next_floor = max(floors_in_direction, key=lambda f: f - self.current_floor)
            else:
                self.direction = Direction.UP
                return self.move()
        else:
            # Elevator is idle but has destinations
            # Decide new direction based on the closest destination
            closest_floor = min(self.destinations, key=lambda f: abs(f - self.current_floor))
            self.direction = Direction.UP if closest_floor > self.current_floor else Direction.DOWN
            return self.move()

        # Move to the next floor
        self.current_floor = next_floor
        self.destinations.remove(next_floor)
        return True

def simulate_elevator(start_floor, floors_to_visit):
    elevator = Elevator(start_floor)
    total_time = 0
    visited_floors = [start_floor]

    # Add destinations in the order provided
    for floor in floors_to_visit:
        elevator.add_destination(floor)

    while elevator.move():
        if elevator.current_floor != visited_floors[-1]:
            total_time += abs(elevator.current_floor - visited_floors[-1]) * FLOOR_TRAVEL_TIME
            visited_floors.append(elevator.current_floor)
        else:
            # Handle same-floor stop without movement
            visited_floors.append(elevator.current_floor)

    return total_time, visited_floors

def parse_input(input_str):
    parts = input_str.strip().split()
    start_floor = None
    floors_to_visit = []

    for part in parts:
        if part.startswith("start="):
            try:
                start_floor = int(part.split("=")[1])
            except ValueError:
                raise ValueError("Invalid start floor value.")
        elif part.startswith("floor="):
            try:
                floors_to_visit = [int(f) for f in part.split("=")[1].split(",")]
            except ValueError:
                raise ValueError("Invalid floor numbers in floors to visit.")

    if start_floor is None or not floors_to_visit:
        raise ValueError("Invalid input. Please provide start floor and floors to visit.")

    return start_floor, floors_to_visit

def process_input(input_str):
    start_floor, floors_to_visit = parse_input(input_str)
    total_time, visited_floors = simulate_elevator(start_floor, floors_to_visit)
    return f"{total_time} {','.join(map(str, visited_floors))}"

def main():
    if len(sys.argv) > 1:
        # Command-line input
        input_str = ' '.join(sys.argv[1:])
        try:
            result = process_input(input_str)
            print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")
    else:
        # File input/output
        with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
            for line in infile:
                try:
                    result = process_input(line)
                    outfile.write(result + '\n')
                except ValueError as e:
                    outfile.write(f"Error: {str(e)}\n")

if __name__ == "__main__":
    main()
