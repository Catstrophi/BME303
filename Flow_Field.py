"""
Flow field works by defining a position as goal and sets the value to 0. Then it expands to the neighbor cell and checks it
    and adds 1. It continues to do this until every cell is checked. Once complete, you will have a grid which each cell having
    a value based on how far it is from the goal.

        ex. 2 represents 2 cells away from goal, 1 is 1 cell, etc.
              2 2 2 2 2
              2 1 1 1 2
              2 1 0 1 2
              2 1 1 1 2
              2 2 2 2 2

create_flow_field:
    Defines a 2x2 square at the center of the grid (coordinates 49-50) as the target destination and assigns
        these cells a distance of 0. These coordinates serve as the starting cell.

    Then it scans the grid outward from the goal to calculate the step-distance for every reachable cell:
            - Checks the four adjacent neighbors (Up, Down, Left, Right) of the current cell.

            - For each neighbor, it performs a 3x3 clearance check. If any cell within that 3x3 radius contains a wall,
                    the neighbor is marked to ensure a 2x2 enemy never collides with it.

                        - If a neighbor is not a wall and hasn't been checked,
                            it is assigned a value of current_distance + 1 and added to the list to continue the flow.
"""

def create_flow_field(walls, grid_size):
    # Flow field, key is cell, value is distance
    flow_field = {}

    # Creates of cells that needs to be checked
    unchecked_cells = []

    # We define a 2x2 square in the middle as the goal
    for cell_x in range(49, 51):
        for cell_y in range(49, 51):

            # The goal is 0 steps away from itself
            flow_field[(cell_x, cell_y)] = 0

            # Add these starting cells to our unchecked cells
            unchecked_cells.append((cell_x, cell_y))

    # Gives condition that if its a wall, you cant go there
    def is_cell_safe(check_x, check_y):
        # Because the enemy is a 2x2 , we check the 3x3 area around this point to make sure no part
        # of the enemy will ever touch a black wall.
        for offset_x in [-1, 0, 1]:
            for offset_y in [-1, 0, 1]:
                neighbor_x = check_x + offset_x
                neighbor_y = check_y + offset_y

                # If any neighbor in this 3x3 block is a wall, this cell is unsafe
                if (neighbor_x, neighbor_y) in walls:
                    return False
        return True

    # Main loop that checks each cell, and adds its neighbor cell
    while len(unchecked_cells) > 0:

        # Get the first cell from the unchecked cell list

        current_cell = unchecked_cells.pop(0)
        current_cell_x = current_cell[0]
        current_cell_y = current_cell[1]

        # How far this cell is from the center
        current_distance = flow_field[(current_cell_x, current_cell_y)]

        # Check the 4 neighbors (Up, Down, Left, Right)

        # Up
        neighbor_x = current_cell_x
        neighbor_y = current_cell_y - 1
        if neighbor_y >= 0:  # Make sure we stay in the grid
            if (neighbor_x, neighbor_y) not in flow_field:  # double checks that the cell is not checked
                if is_cell_safe(neighbor_x, neighbor_y):  # If it's not a wall
                    flow_field[(neighbor_x, neighbor_y)] = current_distance + 1
                    unchecked_cells.append((neighbor_x, neighbor_y)) # we add to the unchecked cell list

        # Repeat the same algorithm for down, left, and right
        # down
        neighbor_x = current_cell_x
        neighbor_y = current_cell_y + 1
        if neighbor_y < grid_size:
            if (neighbor_x, neighbor_y) not in flow_field:
                if is_cell_safe(neighbor_x, neighbor_y):
                    flow_field[(neighbor_x, neighbor_y)] = current_distance + 1
                    unchecked_cells.append((neighbor_x, neighbor_y))

        # left
        neighbor_x = current_cell_x - 1
        neighbor_y = current_cell_y
        if neighbor_x >= 0:
            if (neighbor_x, neighbor_y) not in flow_field:
                if is_cell_safe(neighbor_x, neighbor_y):
                    flow_field[(neighbor_x, neighbor_y)] = current_distance + 1
                    unchecked_cells.append((neighbor_x, neighbor_y))

        # right
        neighbor_x = current_cell_x + 1
        neighbor_y = current_cell_y
        if neighbor_x < grid_size:
            if (neighbor_x, neighbor_y) not in flow_field:
                if is_cell_safe(neighbor_x, neighbor_y):
                    flow_field[(neighbor_x, neighbor_y)] = current_distance + 1
                    unchecked_cells.append((neighbor_x, neighbor_y))

    return flow_field