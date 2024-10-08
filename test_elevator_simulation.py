import unittest
from elevator_simulation import Elevator, simulate_elevator, parse_input, process_input, Direction, FLOOR_TRAVEL_TIME

class TestElevatorSimulation(unittest.TestCase):
    def test_elevator_move_up(self):
        elevator = Elevator(start_floor=1)
        elevator.add_destination(3)
        elevator.add_destination(5)
        steps = []
        while elevator.move():
            steps.append(elevator.current_floor)
        self.assertEqual(steps, [3, 5])

    def test_elevator_move_down(self):
        elevator = Elevator(start_floor=5)
        elevator.add_destination(3)
        elevator.add_destination(1)
        steps = []
        while elevator.move():
            steps.append(elevator.current_floor)
        self.assertEqual(steps, [3, 1])

    def test_elevator_change_direction(self):
        elevator = Elevator(start_floor=3)
        elevator.add_destination(5)
        elevator.add_destination(1)
        steps = []
        while elevator.move():
            steps.append(elevator.current_floor)
        self.assertEqual(steps, [5, 1])

    def test_simulate_elevator(self):
        total_time, visited_floors = simulate_elevator(1, [2, 3, 5])
        expected_total_time = (abs(1 - 2) + abs(2 - 3) + abs(3 - 5)) * FLOOR_TRAVEL_TIME  # 10 + 10 + 20 = 40
        self.assertEqual(total_time, expected_total_time)
        self.assertEqual(visited_floors, [1, 2, 3, 5])

    def test_parse_input_valid(self):
        input_str = "start=1 floor=2,3,5"
        start_floor, floors_to_visit = parse_input(input_str)
        self.assertEqual(start_floor, 1)
        self.assertEqual(floors_to_visit, [2, 3, 5])

    def test_parse_input_invalid_start(self):
        input_str = "start=a floor=2,3,5"
        with self.assertRaises(ValueError):
            parse_input(input_str)

    def test_parse_input_invalid_floors(self):
        input_str = "start=1 floor=2,b,5"
        with self.assertRaises(ValueError):
            parse_input(input_str)

    def test_process_input(self):
        input_str = "start=1 floor=2,3,5"
        result = process_input(input_str)
        self.assertEqual(result, "40 1,2,3,5")

    def test_process_input_error(self):
        input_str = "floor=2,3,5"
        with self.assertRaises(ValueError):
            process_input(input_str)

    def test_elevator_idle(self):
        elevator = Elevator(start_floor=1)
        moved = elevator.move()
        self.assertFalse(moved)
        self.assertEqual(elevator.direction, Direction.IDLE)

    def test_elevator_same_floor_destination(self):
        elevator = Elevator(start_floor=3)
        elevator.add_destination(3)
        steps = []
        while elevator.move():
            steps.append(elevator.current_floor)
        self.assertEqual(steps, [3])
        self.assertEqual(elevator.current_floor, 3)

    def test_elevator_closest_floor_in_direction(self):
        start_floor = 3
        floors_to_visit = [1, 2, 5, 9, 15]
        total_time, visited_floors = simulate_elevator(start_floor, floors_to_visit)
        expected_visited_floors = [3, 2, 1, 5, 9, 15]
        expected_total_time = (
            abs(3 - 2) + abs(2 - 1) + abs(1 - 5) + abs(5 - 9) + abs(9 - 15)
        ) * FLOOR_TRAVEL_TIME
        self.assertEqual(visited_floors, expected_visited_floors)
        self.assertEqual(total_time, expected_total_time)

    def test_elevator_multiple_direction_changes(self):
        start_floor = 5
        floors_to_visit = [8, 2, 10, 3]
        total_time, visited_floors = simulate_elevator(start_floor, floors_to_visit)
        expected_visited_floors = [5, 8, 10, 3, 2]
        expected_total_time = (
            abs(5 - 8) + abs(8 - 10) + abs(10 - 3) + abs(3 - 2)
        ) * FLOOR_TRAVEL_TIME
        self.assertEqual(visited_floors, expected_visited_floors)
        self.assertEqual(total_time, expected_total_time)

    def test_elevator_include_15(self):
        start_floor = 3
        floors_to_visit = [1, 2, 5, 9, 15]
        total_time, visited_floors = simulate_elevator(start_floor, floors_to_visit)
        expected_visited_floors = [3, 2, 1, 5, 9, 15]
        expected_total_time = 160
        self.assertEqual(visited_floors, expected_visited_floors)
        self.assertEqual(total_time, expected_total_time)

    def test_elevator_direction_based_on_first_destination(self):
        start_floor = 3
        floors_to_visit = [5, 2, 6]
        total_time, visited_floors = simulate_elevator(start_floor, floors_to_visit)
        expected_visited_floors = [3, 5, 6, 2]
        expected_total_time = (
            abs(3 - 5) + abs(5 - 6) + abs(6 - 2)
        ) * FLOOR_TRAVEL_TIME
        self.assertEqual(visited_floors, expected_visited_floors)
        self.assertEqual(total_time, expected_total_time)

    def test_elevator_correct_direction_change(self):
        start_floor = 5
        floors_to_visit = [2, 8, 3, 10]
        total_time, visited_floors = simulate_elevator(start_floor, floors_to_visit)
        expected_visited_floors = [5, 3, 2, 8, 10]
        expected_total_time = (
            abs(5 - 3) + abs(3 - 2) + abs(2 - 8) + abs(8 - 10)
        ) * FLOOR_TRAVEL_TIME
        self.assertEqual(visited_floors, expected_visited_floors)
        self.assertEqual(total_time, expected_total_time)


if __name__ == '__main__':
    unittest.main()
