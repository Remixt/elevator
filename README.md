# Elevator Simulation

This elevator simulation program models the operation of a single elevator serving multiple floors in a building. It calculates the total time taken and provides the sequence of floors visited based on user-provided inputs.

## Table of Contents

- [Introduction](#introduction)
- [Elevator Logic](#elevator-logic)
  - [Initial Direction Determination](#initial-direction-determination)
  - [Movement Strategy](#movement-strategy)
  - [Direction Changes](#direction-changes)
- [Usage Instructions](#usage-instructions)
  - [Running the Simulation](#running-the-simulation)
  - [Input Format](#input-format)
  - [Output Format](#output-format)
- [Edge Cases and Handling](#edge-cases-and-handling)
  - [Same Floor Destinations](#same-floor-destinations)
  - [Duplicate Floor Requests](#duplicate-floor-requests)
  - [Invalid Inputs](#invalid-inputs)
- [Assumptions](#assumptions)
- [Extensibility and Modifications](#extensibility-and-modifications)
- [Running Unit Tests](#running-unit-tests)
- [Code Structure Overview](#code-structure-overview)

---

## Introduction

The elevator simulation is designed to mimic the behavior of a real-world elevator in a multi-story building. It processes floor requests and determines the most efficient path to serve all requests, considering the initial direction and optimizing movement within the current direction before changing direction as needed.

---

## Elevator Logic

### Initial Direction Determination

- **Based on First Destination**: The elevator's initial direction is set according to the first floor request relative to its starting floor.
  - If the first requested floor is **above** the starting floor, the elevator moves **upward**.
  - If the first requested floor is **below** the starting floor, the elevator moves **downward**.
  - If the first requested floor is the **same** as the starting floor, the elevator opens its doors without moving and then determines the next direction based on remaining requests.

### Movement Strategy

- **Closest Floor in Current Direction**: While moving in a given direction, the elevator always proceeds to the closest floor in that direction from its current position.
  - **Moving Up**: Selects the lowest floor above the current floor.
  - **Moving Down**: Selects the highest floor below the current floor.
- **Order of Requests Ignored After Initial Direction**: After determining the initial direction, the elevator prioritizes proximity over the order in which floor requests were made.

### Direction Changes

- **When No Destinations Remain in Current Direction**: The elevator changes direction only when there are no more pending requests in the current direction.
- **New Direction Strategy**: Upon changing direction, the elevator again moves to the closest floor in the new direction.

---

## Usage Instructions

### Running the Simulation

You can run the elevator simulation either via command-line arguments or by using input and output files.

#### 1. Command-Line Input

Execute the script with the required parameters:

```bash
python elevator_simulation.py start=<starting_floor> floor=<floor1>,<floor2>,...
```

**Example**:

```bash
python elevator_simulation.py start=3 floor=1,2,5,9,15
```

**Sample Output**:

```
160 3,2,1,5,9,15
```

#### 2. File Input/Output

- Create an `input.txt` file in the same directory as the script.
- Add input lines in the specified format.
- Run the script without any arguments:

  ```bash
  python elevator_simulation.py
  ```

- The results will be written to `output.txt`.

### Input Format

- **Start Floor**: Specified with `start=<integer>`.
- **Floors to Visit**: Specified with `floor=<int1>,<int2>,...`.
- **Multiple Inputs**: Each line in `input.txt` represents a separate simulation run.

**Example**:

```
start=3 floor=1,2,5,9,15
```

### Output Format

- **Total Time**: The total time taken for the elevator to serve all floor requests.
- **Visited Floors**: A comma-separated sequence of floors the elevator stops at, including the starting floor.

**Example Output**:

```
160 3,2,1,5,9,15
```

---

## Edge Cases and Handling

### Same Floor Destinations

- **Behavior**: If the elevator is already on a floor that is requested, it processes the request by opening the doors without moving.
- **Handling**: The elevator removes the current floor from the list of pending destinations and then proceeds based on remaining requests.

### Duplicate Floor Requests

- **Behavior**: If the same floor number appears multiple times in the list of destinations, the elevator treats it as a single request.
- **Handling**: The destinations are stored in a set, which automatically eliminates duplicates. Therefore, the elevator will stop at each floor only once.

### Invalid Inputs

- **Missing Parameters**: If the `start` or `floor` parameters are missing, the simulation will display an error message.
- **Non-integer Values**: If the start floor or any of the floor requests are not integers, the simulation will display an error message.
- **Error Messages**: The program provides clear error messages to help correct the input.

**Example Error Output**:

```
Error: Invalid input. Please provide start floor and floors to visit.
```

---

## Assumptions

- **Fixed Travel Time Between Floors**: The elevator takes 10 seconds to travel between any two adjacent floors.
- **No Door Operation Time**: The time for opening and closing doors is not considered in the total time calculation.
- **Immediate Direction Change**: The elevator changes direction immediately when there are no more requests in the current direction.
- **Single Elevator**: The simulation models only one elevator.
- **Floor Numbers**: Floors are identified by positive integers.

---

## Extensibility and Modifications

- **Handling Multiple Stops at the Same Floor**: If required to handle multiple stops at the same floor (e.g., for different passengers), modify the code to store destinations in a list instead of a set.
- **Door Operation Time**: To include door operation time, adjust the total time calculation in the simulation.
- **Variable Travel Time**: For variable travel times between floors, modify the calculation logic to account for different times.
- **Elevator Capacity**: Implement capacity constraints if simulating passenger loads.
- **Priority Handling**: Introduce priority rules for certain floor requests (e.g., emergency stops).

---

## Running Unit Tests

Unit tests are provided to verify the correctness of the elevator simulation.

### Requirements

- The tests use Python's built-in `unittest` framework; no additional packages are required.

### Executing Tests

Run the following command in the terminal:

```bash
python -m unittest test_elevator_simulation.py
```

### Test Coverage

- **Direction Determination Tests**: Validate the initial direction based on the first floor request.
- **Movement Tests**: Ensure the elevator moves to the closest floor in the current direction.
- **Direction Change Tests**: Confirm the elevator changes direction appropriately when needed.
- **Edge Case Tests**: Cover scenarios like same-floor requests and duplicate floor requests.
- **Input Parsing Tests**: Check for correct parsing and proper error handling of invalid inputs.

---

# Additional Information

## Example Simulation Walkthrough

**Input**:

```
start=5 floor=8,2,10,3
```

**Simulation Steps**:

1. **Initial Direction Determination**:
   - Starting Floor: 5
   - First Destination: 8
   - Since 8 > 5, the initial direction is **UP**.

2. **First Movement (Upwards)**:
   - Possible Destinations Above 5: 8, 10
   - **First Stop**: Floor 8 (closest above 5)
   - **Second Stop**: Floor 10 (next closest above 8)
   - Remove floors 8 and 10 from pending destinations.

3. **Direction Change to Downwards**:
   - Remaining Destinations Below 10: 2, 3
   - Change direction to **DOWN**.

4. **Second Movement (Downwards)**:
   - **First Stop**: Floor 3 (closest below 10)
   - **Second Stop**: Floor 2 (next closest below 3)
   - Remove floors 3 and 2 from pending destinations.

5. **Simulation Ends**:
   - All floor requests have been served.

**Total Time Calculation**:

- 5 to 8: `(8 - 5) * 10 = 30` seconds
- 8 to 10: `(10 - 8) * 10 = 20` seconds
- 10 to 3: `(10 - 3) * 10 = 70` seconds
- 3 to 2: `(3 - 2) * 10 = 10` seconds
- **Total Time**: `30 + 20 + 70 + 10 = 130` seconds

**Output**:

```
130 5,8,10,3,2
```

---

# Code Structure Overview

- **`elevator_simulation.py`**: Main script containing the elevator logic and simulation functions.
- **`test_elevator_simulation.py`**: Contains unit tests to validate the elevator's behavior.

### Key Components in `elevator_simulation.py`

- **Classes**:
  - `Elevator`: Represents the elevator, including its current floor, direction, and destinations.
  - `Direction`: An enumeration (`Enum`) to represent the elevator's possible directions (`UP`, `DOWN`, `IDLE`).

- **Functions**:
  - `simulate_elevator(start_floor, floors_to_visit)`: Runs the simulation and returns total time and visited floors.
  - `parse_input(input_str)`: Parses the user input and extracts the start floor and list of destinations.
  - `process_input(input_str)`: Integrates parsing and simulation, and formats the output.

---
