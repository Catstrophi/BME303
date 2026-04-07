"""
The draw_bone algorithm works in two phases:
    1. Defines the shape of an unbroken bone (a rectangular shaft with circular knobs) and generates a randomized,
    jagged gap down the center to represent the fracture with a set distance.

    2. Scans every single cell on the window grid
       - If a cell is part of the bone, it is painted white.

       - If a white bone cell touches empty space on any of its four sides (up, down, left, right), it is painted black.

       - If a cell is empty space or inside the break, it draws a completely transparent box with a
         light gray border. Creates the visual illusion of a grid
"""

import random

def draw_bone(window, grid_size, cell_size, fracture_gap):
    walls = set()  # Tried using list, way to slow

    # is_bone function checks if the cell at (x,y) is a bone
    def is_bone(cell_x, cell_y):

        # Sets up which cells will be a bone
        shaft_left, shaft_right = 24, 75
        shaft_top, shaft_bottom = 46, 53
        knobs = [(24, 43), (24, 56), (75, 43), (75, 56)]
        knob_size = 20

        # If the (x,y) is in the shaft part of the bone
        if shaft_left <= cell_x <= shaft_right and shaft_top <= cell_y <= shaft_bottom:
            return True

        # If the (x,y) is in the knob part of the bone
        for knob_x, knob_y in knobs:
            if (cell_x - knob_x) ** 2 + (cell_y - knob_y) ** 2 <= knob_size:
                return True

        # Else it is not a bone
        return False

    # create_fracture creates a randomized fracture pattern that has a set distance of "gap"
    def create_fracture(gap):

        # finds center of the grid
        center_x = (24 + 75) // 2

        left_edges = {}
        right_edges = {}

        # Creates the left side fracture and right side fracture by adding/subtracting random number of cells
        for y in range(46, 54):
            left_edges[y] = center_x - (gap // 2) + random.randint(-3, 3)
            right_edges[y] = center_x + (gap // 2) + random.randint(-3, 3)

        return left_edges, right_edges

    # Unpacks the left and right edge
    left_piece_edge, right_piece_edge = create_fracture(fracture_gap)

    # Starts to draw the bone, fracture, and grid
    for x in range(grid_size):
        for y in range(grid_size):

            # Gets the (x,y) pair for the cell
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Checks if each cell is a fracture
            is_fractured = left_piece_edge.get(y, 0) < x < right_piece_edge.get(y, 0)

            # If it is a fracture, add gray outline
            if is_fractured == True:
                window.create_rectangle(x1, y1, x2, y2, fill="", outline="lightgray", tags="grid_line")

            # If it is a bone, the cell becomes white
            elif is_bone(x, y) == True:
                window.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="")

                # Checks the four surrounding cells
                left_is_bone = is_bone(x - 1, y)
                right_is_bone = is_bone(x + 1, y)
                up_is_bone = is_bone(x, y - 1)
                down_is_bone = is_bone(x, y + 1)

                # If one of the 4 cells it is not a bone cell, it is a edge cell and set it to black
                if left_is_bone == False or right_is_bone == False or up_is_bone == False or down_is_bone == False:
                    cell_x = x1 // cell_size
                    cell_y = y1 // cell_size
                    walls.add((cell_x, cell_y))
                    window.create_rectangle(x1, y1, x2, y2, fill="black", outline="")

            # Default of gray outline
            else:
                window.create_rectangle(x1, y1, x2, y2, fill="", outline="lightgray", tags="grid_line")

    return walls, left_piece_edge, right_piece_edge
